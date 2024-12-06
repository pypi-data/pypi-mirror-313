from dataclasses import KW_ONLY, dataclass
import datetime
import importlib.resources
import os
import shutil
import string
import time
import click
from flask import current_app
from flask.testing import FlaskCliRunner
from frolicapp import db, assets_dir, profile_pictures_dir, thumbnails_dir
from frolicapp.models import BranchAdmin, Coordinator, Event, EventThumbnail, Organizer, Participant, Branch, Team, UserWiseProfilePicture, User as SQLAUser, TeamWiseParticipants
from faker import Faker
import random
import importlib
from frolicapp.mock_assets import thumbnails, profile_pictures


fake = Faker()
runner = FlaskCliRunner(current_app)
thumbnail_resource = importlib.resources.files(thumbnails) 
profile_picture_resource = importlib.resources.files(profile_pictures)


@dataclass
class User:
    _: KW_ONLY
    fname: str
    lname: str
    email: str


def generate_mock_user() -> User:
    fname = fake.first_name()
    lname = fake.last_name()
    email = fname + str(time.time_ns()) + '@gmail.com'
    return User(fname=fname, lname=lname, email=email)


@click.command()
def test() -> None:
    """Run tests."""        
    from frolicapp.tests import test as t
    t.run()


@click.command()
def clean() -> None:
    """Delete `db` file from instance directory defined by SQLALCHEMY_DATABASE_URI."""
    db_file = current_app.config["SQLALCHEMY_DATABASE_URI"].split('///')[-1]
    path = os.path.join(current_app.instance_path, db_file)
    try:
        os.remove(path)
        click.echo(click.style("Deleted: ", fg="red", bold=True), nl=False)
        click.echo(click.style(path, fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"Error deleting {path}: {e}", fg="red"))
    path = os.path.join(current_app.instance_path, assets_dir)
    try:
    
        shutil.rmtree(path)
        click.echo(click.style("Deleted: ", fg="red", bold=True), nl=False)
        click.echo(click.style(path, fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"Error deleting {path}: {e}", fg="red"))
    click.echo(click.style(f"File system is clean at {current_app.instance_path}.", fg="green", bold=True))


@click.command()
def create() -> None:
    """Create all tables."""
    from frolicapp.models import User, Coordinator, Organizer, BranchAdmin, Participant, Team, TeamWiseParticipants, Event, EventThumbnail, UserWiseProfilePicture
    click.echo(click.style("************************ Started Creating Tables ************************", fg="bright_blue", bold=True))
    db.create_all()
    click.echo(click.style("All tables are created successfully.", fg="green", bold=True))
    os.makedirs(os.path.join(current_app.instance_path, profile_pictures_dir), exist_ok=True)
    os.makedirs(os.path.join(current_app.instance_path, thumbnails_dir), exist_ok=True)
    fs_path = os.path.join(current_app.instance_path, assets_dir)
    click.echo(click.style(f"File system is ready to store data at {fs_path}.", fg="green", bold=True))
    dp_name = 'admin.png'
    dp = str(profile_picture_resource.joinpath(dp_name))
    dir = os.path.join(current_app.instance_path, profile_pictures_dir)
    shutil.copy(dp, dir)
    dp_path = os.path.join(dir, dp_name)
    admin = SQLAUser(email='sohamjobanputra7@gmail.com', fname='soham', lname='jobanputra', 
    profile_picture=UserWiseProfilePicture(path=dp_path))
    db.session.add(admin)
    db.session.commit()
    click.echo(click.style("Admin user has been initialized.", fg="green", bold=True))


def participant() -> None:
    """Create 500 mock participants."""    
    participants: list[Participant] = []
    for i in range(500):
        user = generate_mock_user()
        dp_name = 'pic' + str(i)+'.jpg'
        dp = str(profile_picture_resource.joinpath(dp_name))
        dir = os.path.join(current_app.instance_path, profile_pictures_dir)
        shutil.copy(dp, dir)
        dp_path = os.path.join(dir, dp_name)
        college_name = fake.word() + ' ' + fake.word()
        branch = random.choice([*Branch])
        participants.append(Participant(college_name=college_name, branch=branch, email=user.email, fname=user.fname, lname=user.lname, profile_picture=UserWiseProfilePicture(dp_path)))
    db.session.add_all(participants)
    db.session.commit()
    click.echo(click.style("Generated 500 mock participants.", fg="green", bold=True))


DETAILS_MARKUP = '''
    <h1>Welcome to the Annual <u>Code-a-Thon</u>!</h1>

    <p>The <strong>Code-a-Thon</strong> is an exciting 48-hour event where developers, designers, and tech enthusiasts collaborate to build innovative projects. Join us and showcase your skills, creativity, and teamwork!</p>

    <h2>Event Details</h2>
    <table border="1">
        <tbody>
            <tr>
                <td><strong>Date</strong></td>
                <td>December 15 - December 17, 2024</td>
            </tr>
            <tr>
                <td><strong>Time</strong></td>
                <td>Starts at 9:00 AM</td>
            </tr>
            <tr>
                <td><strong>Location</strong></td>
                <td>TechHub Auditorium, San Francisco</td>
            </tr>
        </tbody>
    </table>

    <h2>Rules and Guidelines</h2>
    <ol>
        <li>Participants must form teams of <em>3-5 members</em>.</li>
        <li>All projects must be started and completed within the event duration.</li>
        <li>Use of third-party APIs and libraries is allowed but must be credited.</li>
        <li>Plagiarism or pre-existing projects are strictly prohibited.</li>
        <li>Teams must submit their code via the provided portal by the deadline.</li>
    </ol>

    <h2>Judging Criteria</h2>
    <ul>
        <li><strong>Innovation</strong> - Originality of the idea.</li>
        <li><strong>Functionality</strong> - Working features of the project.</li>
        <li><strong>Design</strong> - User interface and user experience.</li>
        <li><strong>Presentation</strong> - Clarity and effectiveness of the project demo.</li>
    </ul>

    <h2>Prizes</h2>
    <table border="1">
        <tbody>
            <tr>
                <td><strong>Position</strong></td>
                <td><strong>Prize</strong></td>
            </tr>
            <tr>
                <td>1st Place</td>
                <td>$5000 + Trophy</td>
            </tr>
            <tr>
                <td>2nd Place</td>
                <td>$3000</td>
            </tr>
            <tr>
                <td>3rd Place</td>
                <td>$1000</td>
            </tr>
        </tbody>
    </table>

    <h2>Registration</h2>
    <p>Ready to join? Register your team today by clicking the link below:</p>
    <p><a href="https://google.com" target="_blank">Register for Code-a-Thon 2024</a></p>

    <p>For any queries, feel free to contact us at <strong>info@codeathon2024.com</strong>.</p>
'''
def event() -> None:
    """Create 30 mock events."""
    admin = SQLAUser.query.get(1)
    events: list[Event] = []
    for i in range(1, 30 + 1):
        name = ' '.join(fake.words(nb=5, unique=True))
        branch = random.choice([*Branch])
        description = fake.paragraph(nb_sentences=4)
        min_team_size = 2
        max_team_size = 5
        max_teams = random.randint(25, 50)
        start_time = datetime.datetime.now().replace(second=0, microsecond=0).time()
        thumbnail_name = 'w' + str(i)+'.png'
        thumbnail = str(thumbnail_resource.joinpath(thumbnail_name))
        dir = os.path.join(current_app.instance_path, thumbnails_dir)
        shutil.copy(thumbnail, dir)
        thumbnail_path = os.path.join(dir, thumbnail_name)
        events.append(Event(name=name, branch=branch, description=description, min_team_size=min_team_size, max_team_size=max_team_size, max_teams=max_teams, start_time=start_time, created_by=admin, thumbnail=EventThumbnail(path=thumbnail_path), details=DETAILS_MARKUP))
    db.session.add_all(events)
    db.session.commit()
    click.echo(click.style("Generated 30 mock events.", fg='green', bold=True))
        

def branchadmin() -> None:
    """Create a branchadmin for each branch."""
    branchadmins: list[BranchAdmin] = []
    for idx, branch in enumerate([*Branch]):
        user = generate_mock_user()
        dp_name = 'pic' + str(999-idx)+'.jpg'
        dp = str(profile_picture_resource.joinpath(dp_name))
        dir = os.path.join(current_app.instance_path, profile_pictures_dir)
        shutil.copy(dp, dir)
        dp_path = os.path.join(dir, dp_name)
        branchadmins.append(BranchAdmin(branch=branch, fname=user.fname, lname=user.lname, email=user.email, profile_picture=UserWiseProfilePicture(path=dp_path))) 
    db.session.add_all(branchadmins)
    db.session.commit()
    click.echo(click.style("Generated a mock branchadmin for each branch.", fg='green', bold=True))


def organizer() -> None:
    """Generate an organizer for each event."""
    organizers: list[Organizer] = []
    events = Event.query.all()
    for event in events:
        user = generate_mock_user()
        dp_name = 'pic' + str(499+event.event_id)+'.jpg'
        dp = str(profile_picture_resource.joinpath(dp_name))
        dir = os.path.join(current_app.instance_path, profile_pictures_dir)
        shutil.copy(dp, dir)
        dp_path = os.path.join(dir, dp_name)
        organizers.append(Organizer(event=event, fname=user.fname, lname=user.lname, email=user.email, profile_picture=UserWiseProfilePicture(path=dp_path)))
    db.session.add_all(organizers)
    db.session.commit()
    click.echo(click.style("Generated a mock organizer for each event.", fg='green', bold=True))


def coordinator() -> None:
    """Generate 2 coordinators for each event."""
    coordinators: list[Coordinator] = []
    events = Event.query.all()
    for event in events:
        user1, user2 = generate_mock_user(), generate_mock_user()
        dp1_name = 'pic' + str(599+event.event_id)+'.jpg'
        dp2_name = 'pic' + str(899+event.event_id)+'.jpg'
        dp1 = str(profile_picture_resource.joinpath(dp1_name))
        dp2 = str(profile_picture_resource.joinpath(dp2_name))
        dir = os.path.join(current_app.instance_path, profile_pictures_dir)
        shutil.copy(dp1, dir)
        shutil.copy(dp2, dir)
        dp1_path = os.path.join(dir, dp1_name)
        dp2_path = os.path.join(dir, dp2_name)
        coordinators.append(Coordinator(event=event, fname=user1.fname, lname=user1.lname, email=user1.email, profile_picture=UserWiseProfilePicture(path=dp1_path)))
        coordinators.append(Coordinator(event=event, fname=user2.fname, lname=user2.lname, email=user2.email, profile_picture=UserWiseProfilePicture(path=dp2_path)))
    db.session.add_all(coordinators)
    db.session.commit()
    click.echo(click.style("Generated 2 mock coordinators for each event.", fg='green', bold=True))


def team() -> None:
    """Generate 3 teams of 5 participants for each event."""
    teams: list[Team] = []
    team_wise_participants: list[TeamWiseParticipants] = []
    events = Event.query.all()
    participants = Participant.query.all()
    i = 0
    for event in events:
        team_members = participants[i : i+5]
        i += 5
        t = Team(leader=team_members[0], event=event, name=''.join(map(lambda c : string.ascii_lowercase[int(c)-1], ''.join(str(time.time()).split('.')))))
        teams.append(t)
        for member in team_members[1:]:
            team_wise_participants.append(TeamWiseParticipants(team=t, participant=member))

        team_members = participants[i : i+5]
        i += 5
        t = Team(leader=team_members[0], event=event, name=''.join(map(lambda c : string.ascii_lowercase[int(c)-1], ''.join(str(time.time()).split('.')))))
        teams.append(t)
        for member in team_members[1:]:
            team_wise_participants.append(TeamWiseParticipants(team=t, participant=member))

        team_members = participants[i : i+5]
        i += 5
        t = Team(leader=team_members[0], event=event, name=''.join(map(lambda c : string.ascii_lowercase[int(c)-1], ''.join(str(time.time()).split('.')))))
        teams.append(t)
        for member in team_members[1:]:
            team_wise_participants.append(TeamWiseParticipants(team=t, participant=member))
    db.session.add_all(teams)
    db.session.add_all(team_wise_participants)
    db.session.commit()
    click.echo(click.style("Generated 3 mock teams of 5 mock participants for each mock event.", fg='green', bold=True))


def all_() -> None:
    """Generate mock data for all ORM objects."""
    participant()
    event()
    team()
    organizer()
    coordinator()
    branchadmin()
    click.echo(click.style("Generated mock data for all ORM objects.", fg='green', bold=True))


@click.command()
def mock() -> None:
    """Clean the database, create the schema, generate and store the mock data. Makes the application ready to run with mock data."""
    click.echo(click.style("Cleaning the database...", fg='green', bold=True))
    runner.invoke(clean)
    click.echo(click.style("Creating database schema as per ORM mapped classes...", fg='green', bold=True))
    runner.invoke(create)
    click.echo(click.style("Generating mock data...", fg='green', bold=True))
    all_()
    click.echo(click.style("Application is ready to run.", fg='green', bold=True))