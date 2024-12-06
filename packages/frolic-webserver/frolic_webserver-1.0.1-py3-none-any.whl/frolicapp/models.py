from collections.abc import Sequence
import datetime
from enum import StrEnum, auto
import os
from pathlib import Path, PurePath
import string
from typing import Annotated, Any, NoReturn, Optional, Self, Set, TypeVar
from flask import current_app
import nh3
from sqlalchemy import Dialect, ForeignKey, String, create_engine, event, Connection
from sqlalchemy.orm import MappedAsDataclass, sessionmaker, Mapped, mapped_column, validates, Mapper, relationship
import sqlalchemy.types as types
from sqlalchemy.ext.hybrid import hybrid_property
from pydantic import BaseModel, ConfigDict, FilePath, PositiveInt, TypeAdapter, ValidationError, model_validator
from email_validator import validate_email
import re
from dataclasses import KW_ONLY
from frolicapp import db, assets_dir


MB = int(1e+6)
KB = int(1e+3)
T = TypeVar('T')
Seq = TypeVar('Seq', bound=Sequence[Any])
IMAGE_EXTENSIONS = tuple('jpg jpeg png '.split())
NO_SIDE_SPACE = r'^\S.*\S$|^\S$'

PrimaryKey = Mapped[Annotated[int, mapped_column(primary_key=True, autoincrement=True)]]


def validate_type(ta: TypeAdapter[T], obj: T) -> T:
    """Validates an object against a specified type adapter.

    This function uses a `TypeAdapter` to validate that the provided object
    matches the expected type. If validation fails, it raises a `ValueError`
    with the validation error message.

    Args:
        ta (TypeAdapter[T]): A TypeAdapter instance representing the expected type.
        obj (T): The object to validate against the specified type adapter.

    Returns:
        T: The validated object if it meets the expected type requirements.

    Raises:
        ValueError: If the object does not match the expected type, a `ValueError`
            is raised with details from the underlying `ValidationError`.
    """
    try:
        ta.validate_python(obj)
    except ValidationError as e:
        raise ValueError(str(e))
    return obj


def validate_range(obj: Seq, rng: tuple[int, int], obj_name: Optional[str] = None) -> Seq:
    """Validates that the length of a sequence is within a specified range.

    Checks if the length of the given sequence falls within the provided inclusive range. 
    If the length is out of range, raises a `ValueError` with a descriptive message.

    Args:
        obj (Seq): The sequence (e.g., list, tuple, or string) to validate.
        rng (tuple[int, int]): A tuple representing the inclusive minimum and maximum length 
            bounds as `(min_length, max_length)`.
        obj_name (Optional[str]): An optional name for the sequence, used in the error 
            message if validation fails.

    Returns:
        Seq: The original sequence if its length is within the specified range.

    Raises:
        ValueError: If the length of `obj` is outside the range specified by `rng`. 
            Includes `obj_name` in the error message if provided.
    """
    if len(obj) not in range(rng[0], rng[1] + 1):
        if obj_name is not None: raise ValueError(f'The length of {obj_name} must be between {rng[0]} to {rng[1]}')    
        else: raise ValueError(f'The length of given sequence must be between {rng[0]} to {rng[1]}')
    return obj


def validate_str(obj: str, rng: tuple[int, int], allowed_chars: str, pattern: Optional[str] = None,  obj_name: Optional[str] = None) -> str:
    """Validates a string based on length, allowed characters, and an optional pattern.

    This function checks that a string meets specified constraints:
    - The length must fall within a given inclusive range.
    - All characters in the string must be in a set of allowed characters.
    - The string must optionally match a regular expression pattern.

    Args:
        obj (str): The string to validate.
        rng (tuple[int, int]): A tuple specifying the minimum and maximum allowable length 
            as `(min_length, max_length)`.
        allowed_chars (str): A string containing all characters allowed in `obj`.
        pattern (Optional[str]): A regular expression pattern that `obj` must match, if provided.
        obj_name (Optional[str]): An optional name for the string, used in error messages.

    Returns:
        str: The validated string if it meets all constraints.

    Raises:
        ValueError: If the length of `obj` is outside `rng`, if `obj` contains characters 
            outside `allowed_chars`, or if `obj` does not match the specified `pattern`.
    """
    obj = validate_range(obj, rng, obj_name or "string")
    for char in allowed_chars:
        if char not in allowed_chars:
            if obj_name is not None: raise ValueError(f'{obj_name} can only contain following characters: "{allowed_chars}".')
            else: raise ValueError(f'Given string can only contain following characters: "{allowed_chars}".')
    if pattern is not None and re.match(pattern, obj) is None:
        raise ValueError(f'{obj_name} must follow the pattern: "{pattern}".')
    return obj


class Role(StrEnum):
    ADMIN = auto()
    BRANCHADMIN = auto()
    ORGANIZER = auto()
    COORDINATOR = auto()
    PARTICIPANT = auto()


class Branch(StrEnum):
    BCA = auto()
    BBA = auto()
    CSE = auto()
    MBA = auto()
    BSC = auto()
    DIPLOMA = auto()


class CustomPydanticBase(BaseModel):
    model_config = ConfigDict(
        strict=True,
        frozen=True,
        extra='forbid',
        from_attributes=True,
        revalidate_instances='always',
        validate_default=True,
        validate_return=True,
        validate_assignment=True,
    )


class ConstrainedImagePathModel(CustomPydanticBase):
    """Model to validate an image file's path, size, and extension constraints.

    This model validates that a file path points to an image file meeting specific requirements:
    - The file must have an allowed image file extension.
    - The file size must not exceed a specified maximum byte size.

    Attributes:
        path (FilePath): The file path to the image, validated to be a file and to meet 
            extension requirements.
        max_bytes (PositiveInt): The maximum allowable file size in bytes.
        allowed_extensions (tuple[str, ...]): A tuple of allowed file extensions for the image.
            Defaults to `IMAGE_EXTENSIONS`, which should be predefined with supported image extensions.
    """
    path: FilePath
    max_bytes: PositiveInt
    allowed_extensions: tuple[str, ...] = IMAGE_EXTENSIONS

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        for ext in self.allowed_extensions:
            if self.path.name.endswith('.'+ext):
                break
        else:
            raise ValueError(f'The file must have one of these extension: {list(IMAGE_EXTENSIONS)}.')

        if self.path.stat().st_size > self.max_bytes:
            raise ValueError(f'The file size must be less than ~{str(int(round(self.max_bytes/1000, 1))) + "kb" if self.max_bytes >= 1000 else str(self.max_bytes) + " bytes"}.')

        return self


class ConstrainedImagePath(types.TypeDecorator[str]):
    """A custom SQLAlchemy type for validating image file paths with constraints.

    This type decorator ensures that a file path meets specific constraints before
    storing it in the database. The file must:
    - Be under the specified directory
    - Be a valid image path.
    - Adhere to a specified maximum size limit (in bytes).
    """
    impl = types.String

    cache_ok = True

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if value is None : return None
        abs_path = PurePath(str(ConstrainedImagePathModel(path=Path(value), max_bytes=self.max_bytes).path.resolve()))
        root_dir = PurePath(os.path.join(current_app.instance_path, assets_dir))
        if not abs_path.is_relative_to(root_dir):
            raise ValueError(f'The file must be under {str(Path(root_dir).resolve())} but located at {str(Path(abs_path).resolve())}.') 
        return str(abs_path.relative_to(root_dir))
    
    def __init__(self, max_bytes: int) -> None:
        self.max_bytes = max_bytes
        super().__init__(512)


class EmailString(types.TypeDecorator[str]):
    """A custom SQLAlchemy type for validating and normalizing email addresses.

    This type decorator ensures that an email address is valid and normalizes it before
    storing it in the database. Validation includes basic format checks but skips 
    deliverability verification.
    """
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect: Dialect) -> Any:
        if value is None : return None
        return validate_email(value, check_deliverability=False).normalized

    def __init__(self) -> None:
        super().__init__(320)


class ConstrainedString(types.TypeDecorator[str]):
    """A custom SQLAlchemy type for validating and constraining string values.

    This type decorator ensures that a string meets specified constraints before storing 
    it in the database. Constraints include:
    - Minimum and maximum length.
    - Allowed characters.
    - Optional regular expression pattern matching.
    """
    impl = types.String

    def process_bind_param(self, value: str | None, dialect: Dialect) -> Any:
        if value is None : return None
        return validate_str(value, (self.min, self.max), self.allowed_chars, self.pattern)

    def __init__(self, min: int, max: int, allowed_chars: str, pattern: Optional[str] = None):
        self.min = min
        self.max = max
        self.allowed_chars = allowed_chars
        self.pattern = pattern
        super().__init__(max)


class ConstrainedInteger(types.TypeDecorator[int]):
    """A custom SQLAlchemy type for validating integer values within a specified range.

    This type decorator ensures that an integer falls within a defined inclusive range 
    before storing it in the database.
    """
    impl = types.Integer

    def process_bind_param(self, value: int | None, dialect: Dialect) -> Any:
        if value is None : return None
        if value not in range(self.min, self.max + 1) : raise ValueError('Integer went out of bounds.') 
        return value   

    def __init__(self, min: int, max: int) -> None:
        if min > max : raise ValueError('Non-compitable parameter values for min and max.')
        self.min = min
        self.max = max
        super().__init__()
        

# class Base(MappedAsDataclass, DeclarativeBase):
#     pass


class TimestampMixin(MappedAsDataclass):
    """A mixin class that adds timestamp fields and immutability constraints to SQLAlchemy models.

    This mixin provides `created_at` and `updated_at` timestamp fields for tracking the creation
    and modification times of database records. Both fields are immutable after initial creation.
    """
    created_at: Mapped[datetime.datetime] = mapped_column(init=False, insert_default=datetime.datetime.now().replace(microsecond=0))
    updated_at: Mapped[datetime.datetime] = mapped_column(init=False, insert_default=datetime.datetime.now().replace(microsecond=0))

    @validates('created_at')
    def validator(self, key: str, val: datetime.datetime) -> NoReturn:
        raise AttributeError(f"Cannot modify constant field '{key}'.")


class MinGreaterThanMaxError(ValueError):
    """Custom exception raised when the minimum value is greater than the maximum value."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(engine)
session = Session()


class TeamWiseParticipants(db.Model): # type: ignore
    """SQLAlchemy ORM model representing the association between a team and its participants.

    This class maps to the `team_wise_participants` table and serves as an association table 
    to link participants to the teams they belong to. Each record in this table represents 
    a participant being part of a specific team.

    Attributes:
        team_id (Mapped[int]): The foreign key linking to the `team` table, representing the team.
        participant_id (Mapped[int]): The foreign key linking to the `participant` table, representing the participant.

    Relationships:
        team (Mapped["Team"]): A relationship to the `Team` model, allowing access to the associated team.
        participant (Mapped["Participant"]): A relationship to the `Participant` model, allowing access to the associated participant.
    """
    team_id: Mapped[int] = mapped_column(ForeignKey('team.team_id'), primary_key=True, init=False)
    participant_id: Mapped[int] = mapped_column(ForeignKey('participant.participant_id'), primary_key=True, init=False)

    team: Mapped["Team"] = relationship(init=True, back_populates='participants') 
    participant: Mapped["Participant"] = relationship(init=True, back_populates='teams')

    def __hash__(self) -> int:
        return hash((self.team, self.participant))


class UserWiseProfilePicture(db.Model): # type: ignore
    """SQLAlchemy ORM model for storing user-specific profile pictures.

    This class maps to the `user_wise_profile_picture` table and stores information 
    about the profile picture associated with a specific user. It includes the user ID 
    (as a foreign key to the `user` table) and the file path to the profile picture, 
    constrained by size.

    Attributes:
        user_wise_profile_picture_id (PrimaryKey): The primary key for the profile picture record.
        user_id (Mapped[int]): The foreign key linking the profile picture to the `user` table, 
            ensuring a one-to-one relationship between user and profile picture.
        path (Mapped[str]): The file path to the profile picture, validated with `ConstrainedImagePath`, 
            which enforces file size restrictions (in this case, a 5 KB maximum size).

    Relationships:
        user: This model has an implicit relationship to the `User` model via the `user_id` foreign key.
    """
    user_wise_profile_picture_id: PrimaryKey = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), init=False, unique=True)
    path: Mapped[str] = mapped_column(ConstrainedImagePath(max_bytes=500*KB), init=True, unique=True)


class User(db.Model, TimestampMixin): # type: ignore
    """SQLAlchemy ORM model representing a user with specific constraints and properties.

    This class maps to a `user` table in the database and includes basic user details 
    like `email`, `first name`, `last name`, and `role`. It also includes automatic 
    timestamp management and a method for managing the user's full name. The class also 
    supports polymorphic inheritance based on the `role` field.

    Attributes:
        user_id (PrimaryKey): The primary key for the user record (auto-generated).
        email (Mapped[str]): The user's email address, stored using the `EmailString` 
            type with a unique constraint.
        fname (Mapped[str]): The user's first name, constrained to a specified length 
            and allowed characters.
        lname (Mapped[str]): The user's last name, constrained to a specified length 
            and allowed characters.
        role (Mapped[Role]): The role of the user, which determines their access level 
            or behavior within the application.
        fullname (hybrid_property): A computed property combining the user's first and 
            last name to generate a full name.
        profile_picture (Mapped[Optional[UserWiseProfilePicture]]): A one-to-one 
            relationship to the `UserWiseProfilePicture` model, allowing the user to 
            have an associated profile picture.

    Relationships:
        profile_picture: Defines a one-to-one relationship with `UserWiseProfilePicture`, 
            with cascading behavior on delete.

    Polymorphic Behavior:
        The model supports polymorphic inheritance based on the `role` field. The 
        `polymorphic_identity` is set to `"user"`, and the `polymorphic_on` column 
        is `"role"`, allowing for different user roles to be mapped to subclasses.
    """
    _: KW_ONLY
    user_id: PrimaryKey = mapped_column(init=False)
    email: Mapped[str] = mapped_column(EmailString(), unique=True, init=True)
    fname: Mapped[str] = mapped_column(ConstrainedString(min=2, max=32, allowed_chars=string.ascii_lowercase, pattern=NO_SIDE_SPACE), init=True)
    lname: Mapped[str] = mapped_column(ConstrainedString(min=2, max=32, allowed_chars=string.ascii_lowercase, pattern=NO_SIDE_SPACE), init=True)
    role: Mapped[Role] = mapped_column(init=False)

    @hybrid_property
    def fullname(self) -> str:
        return self.fname + " " + self.lname

    profile_picture: Mapped[Optional[UserWiseProfilePicture]] = relationship(init=True, default=None, cascade='all, delete')

    __mapper_args__ = {
        "polymorphic_identity": Role.ADMIN.value,
        "polymorphic_on": "role",
    }

    def __hash__(self) -> int:
        return hash(self.email)


class Coordinator(User):
    """SQLAlchemy ORM model representing a coordinator, inherited from `User`.

    This class maps to the `coordinator` table and extends the `User` model by adding a 
    reference to an `event` and a `coordinator_id` which links to the `user` table. The `role` 
    for this class is set to `COORDINATOR` via polymorphic inheritance.

    Attributes:
        coordinator_id (Mapped[int]): The foreign key linking to the `user` table, acting as the primary key.
        event_id (Mapped[int]): The foreign key linking to the `event` table, ensuring a one-to-one relationship.
        event (Mapped["Event"]): The relationship to the `Event` model.
    
    Relationships:
        event: Defines one-to-one relationship with `Event`.

    Polymorphic Behavior:
        The `role` for this model is set to `COORDINATOR`, which determines its polymorphic identity.
    """
    coordinator_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), init=False)

    event: Mapped["Event"] = relationship(init=True, back_populates='coordinators')

    __mapper_args__ = {
        "polymorphic_identity": Role.COORDINATOR.value,
    }

    def __hash__(self) -> int:
        return super().__hash__()


class Organizer(User):
    """SQLAlchemy ORM model representing an organizer, inherited from `User`.

    This class maps to the `organizer` table and extends the `User` model by adding a 
    reference to an `event` and an `organizer_id` which links to the `user` table. The `role` 
    for this class is set to `ORGANIZER` via polymorphic inheritance.

    Attributes:
        organizer_id (Mapped[int]): The foreign key linking to the `user` table, acting as the primary key.
        event_id (Mapped[int]): The foreign key linking to the `event` table, ensuring a one-to-one relationship.
        event (Mapped["Event"]): The relationship to the `Event` model.

    Relationships:
        event: Defines one-to-one relationship with `Event`.

    Polymorphic Behavior:
        The `role` for this model is set to `ORGANIZER`, which determines its polymorphic identity.
    """
    organizer_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), init=False, unique=True)

    event: Mapped["Event"] = relationship(init=True, back_populates='organizers')

    __mapper_args__ = {
        "polymorphic_identity": Role.ORGANIZER.value,
    }

    def __hash__(self) -> int:
        return super().__hash__()


class Participant(User):
    """SQLAlchemy ORM model representing a participant, inherited from `User`.

    This class maps to the `participant` table and extends the `User` model by adding 
    a reference to the participant's college name, branch, and a relationship to `TeamWiseParticipants`. 
    The `role` for this class is set to `PARTICIPANT` via polymorphic inheritance.

    Attributes:
        participant_id (Mapped[int]): The foreign key linking to the `user` table, acting as the primary key.
        college_name (Mapped[str]): The name of the college the participant belongs to, constrained by length and allowed characters.
        branch (Mapped[Branch]): The branch the participant is associated with.
        teams (Mapped[Set[TeamWiseParticipants]]): A relationship to the `TeamWiseParticipants` model, linking the participant to multiple teams.

    Relationships:
        teams (Mapped[Set[TeamWiseParticipants]]): Defines a one-to-many relationship with `TeamWiseParticipants`, 
            allowing a participant to be part of multiple teams.
        leaderships: Mapped[Set["Team"]]: Defines a one-to-many relationship with `Team` is set of teams created by this participant.

    Polymorphic Behavior:
        The `role` for this model is set to `PARTICIPANT`, which determines its polymorphic identity.
    """
    participant_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True, init=False)
    college_name: Mapped[str] = mapped_column(ConstrainedString(min=2, max=64, allowed_chars=string.ascii_letters, pattern=NO_SIDE_SPACE), init=True)
    branch: Mapped[Branch] = mapped_column(init=True)

    teams: Mapped[Set[TeamWiseParticipants]] = relationship(init=False, back_populates='participant', cascade='all, delete')
    leaderships: Mapped[Set["Team"]] = relationship(init=False, back_populates='leader', cascade='all, delete')

    __mapper_args__ = {
        "polymorphic_identity": Role.PARTICIPANT.value,
    }

    def __hash__(self) -> int:
        return super().__hash__()


class BranchAdmin(User):
    """SQLAlchemy ORM model representing a branch admin, inherited from `User`.

    This class maps to the `branch_admin` table and extends the `User` model by adding 
    a reference to a `branch` and a `branch_admin_id` which links to the `user` table. The `role` 
    for this class is set to `BRANCHADMIN` via polymorphic inheritance.

    Attributes:
        branch_admin_id (Mapped[int]): The foreign key linking to the `user` table, acting as the primary key.
        branch (Mapped[Branch]): The reference to the `Branch` enum, which is unique for each admin.

    Polymorphic Behavior:
        The `role` for this model is set to `BRANCHADMIN`, which determines its polymorphic identity.
    """
    branch_admin_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True, init=False)
    branch: Mapped[Branch] = mapped_column(init=True, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": Role.BRANCHADMIN.value,
    }

    def __hash__(self) -> int:
        return super().__hash__()
    
    
EVT_ALLOWED_TEAM_SIZE_CONSTRAIN = ConstrainedInteger(min=1, max=7)
EVT_NAME_LEN = (2, 64)
EVT_DESCRIPTION_LEN = (8, 512)
EVT_THUMBNAIL_MAX_SIZE = 5 * MB
EVT_MAX_TEAMS_CONSTRAIN = ConstrainedInteger(min=1, max=50)
EVT_DETAILS_SIZE = 9000
class Event(db.Model, TimestampMixin): # type: ignore
    """SQLAlchemy ORM model representing an event.

    This class maps to the `event` table and represents an event in the system. Each event has
    details like its name, description, team size constraints, associated branch, and the users 
    who created and modified it. The event can also have an associated thumbnail. It also includes automatic 
    timestamp management.

    Attributes:
        event_id (PrimaryKey): The primary key for the event.
        name (Mapped[str]): The name of the event, constrained by length and allowed characters.
        branch (Mapped[Branch]): The branch associated with the event.
        description (Mapped[str]): A description of the event, constrained by length and allowed characters.
        min_team_size (Mapped[int]): The minimum number of participants allowed per team.
        max_team_size (Mapped[int]): The maximum number of participants allowed per team.
        max_teams (Mapped[int]): The maximum number of teams that can participate in the event.
        start_time (Mapped[datetime.time]): The start time of the event.
        created_by_id (Mapped[int]): The foreign key linking to the `user` table, representing the user who created the event.
        modified_by_id (Mapped[int]): The foreign key linking to the `user` table, representing the user who last modified the event.

    Relationships:
        created_by (Mapped[User]): The user who created the event.
        modified_by (Mapped[User]): The user who last modified the event.
        thumbnail (Mapped[Optional["EventThumbnail"]]): The thumbnail image associated with the event.
    """
    _: KW_ONLY
    event_id: PrimaryKey = mapped_column(init=False)
    name: Mapped[str] = mapped_column(ConstrainedString(min=EVT_NAME_LEN[0], max=EVT_NAME_LEN[1], allowed_chars=string.ascii_lowercase+' ', pattern=NO_SIDE_SPACE), init=True, unique=True)
    branch: Mapped[Branch] = mapped_column(init=True)
    description: Mapped[str] = mapped_column(ConstrainedString(min=EVT_DESCRIPTION_LEN[0], max=EVT_DESCRIPTION_LEN[1], allowed_chars=string.ascii_letters+' '+string.punctuation, pattern=NO_SIDE_SPACE), init=True)
    min_team_size: Mapped[int] = mapped_column(EVT_ALLOWED_TEAM_SIZE_CONSTRAIN, init=True)
    max_team_size: Mapped[int] = mapped_column(EVT_ALLOWED_TEAM_SIZE_CONSTRAIN, init=True)
    max_teams: Mapped[int] = mapped_column(EVT_MAX_TEAMS_CONSTRAIN,  init=True)
    start_time: Mapped[datetime.time] = mapped_column(init=True)
    details: Mapped[Optional[str]] = mapped_column(String(EVT_DETAILS_SIZE), init=True, default=None)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), init=False)
    modified_by_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), init=False)

    created_by: Mapped[User] = relationship(init=True, foreign_keys=[created_by_id])
    modified_by: Mapped[User] = relationship(init=False, foreign_keys=[modified_by_id])
    thumbnail: Mapped[Optional["EventThumbnail"]] = relationship(init=True, default=None, cascade='all, delete')
    teams: Mapped[Set["Team"]] = relationship(init=False, back_populates='event', cascade='all, delete')
    coordinators: Mapped[Set["Coordinator"]] = relationship(init=False, back_populates='event', cascade='all, delete', foreign_keys=[Coordinator.event_id])
    organizers: Mapped[Set["Organizer"]] = relationship(init=False, back_populates='event', cascade='all, delete', foreign_keys=[Organizer.event_id])

    def __post_init__(self) -> None:
        if self.min_team_size > self.max_team_size : raise MinGreaterThanMaxError('Minimum team size must be less than or equal to maximum team size.')
        self.modified_by = self.created_by

    @validates('details')
    def senitize_details_markup(self, key: str, value: str | None) -> str | None:
        if value is None: return None
        return nh3.clean(value, tags={"strong", "em", "h1", "h2", "p", "u", "ol", "ul", "li", "a", "table", "tbody", "thead", "th", "tr", "td"}, url_schemes={'https'})


class EventThumbnail(db.Model): # type: ignore
    """SQLAlchemy ORM model representing the thumbnail image for an event.

    This class maps to the `event_thumbnail` table and stores the thumbnail image for a specific event.
    Each thumbnail is associated with a particular event and is constrained by size.

    Attributes:
        event_thumbnail_id (PrimaryKey): The primary key for the event thumbnail.
        event_id (Mapped[int]): The foreign key linking to the `event` table, associating the thumbnail with an event.
        path (Mapped[str]): The file path of the thumbnail image, constrained by file size and uniqueness.
    """
    event_thumbnail_id: PrimaryKey = mapped_column(init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), init=False, unique=True)
    path: Mapped[str] = mapped_column(ConstrainedImagePath(max_bytes=EVT_THUMBNAIL_MAX_SIZE), unique=True, init=True)


class Team(db.Model): # type: ignore
    """SQLAlchemy ORM model representing a team.

    This class maps to the `team` table and represents a team in the system. Each team has 
    a leader (linked to a `Participant`), an associated event, and a set of participants 
    (linked through the `TeamWiseParticipants` association table).

    Attributes:
        team_id (PrimaryKey): The primary key for the team.
        leader_id (Mapped[int]): The foreign key linking to the `participant` table, indicating the leader of the team.
        event_id (Mapped[int]): The foreign key linking to the `event` table, indicating the event the team is participating in.

    Relationships:
        leader (Mapped[Participant]): The leader of the team, represented as a `Participant`.
        participants (Mapped[Set[TeamWiseParticipants]]): A one-to-many relationship with `TeamWiseParticipants`, 
            linking multiple participants to the team.
        event (Mapped[Event]): The event associated with the team, represented as an `Event`.
    """
    team_id: PrimaryKey = mapped_column(init=False)
    leader_id: Mapped[int] = mapped_column(ForeignKey('participant.participant_id'), init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), init=False)
    name: Mapped[str] = mapped_column(ConstrainedString(min=EVT_NAME_LEN[0], max=EVT_NAME_LEN[1], allowed_chars=string.ascii_lowercase+' ', pattern=NO_SIDE_SPACE), init=True, unique=True)

    leader: Mapped[Participant] = relationship(init=True, back_populates='leaderships')
    participants: Mapped[Set[TeamWiseParticipants]] = relationship(init=False, back_populates='team', cascade='all, delete')
    event: Mapped[Event] = relationship(init=True, back_populates='teams')

    def __hash__(self) -> int:
        return hash(self.name)


@event.listens_for(Event, 'before_update')
@event.listens_for(User, 'before_update')
def receive_before_update(mapper: Mapper[User | Event], connection: Connection, target: User | Event) -> None:
    target.updated_at = datetime.datetime.now().replace(microsecond=0)
