import os
import time
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from frolicapp.models import BranchAdmin, Coordinator, Event, Organizer, Participant, Role, Team, User, EventThumbnail, MinGreaterThanMaxError
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug import exceptions
from frolicapp.blueprints.admin.forms import SearchForm, EventForm, evt_consts
from frolicapp import db, thumbnails_dir, FlashCategory, assets_dir
from werkzeug import Response


bp = Blueprint(
    'Admin',
    __name__,
    url_prefix='/admin',
    static_folder='static',
    template_folder='templates'
)

@bp.route('/', methods=['GET', 'POST'])
def home() -> str:
    form = SearchForm()
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    if form.validate_on_submit() and not (query:=form.search.data) == '':
        events = Event.query.filter(
            or_(
                Event.name.ilike(f'%{query}%'),
                Event.description.ilike(f'%{query}%'+'%'*5)
            )
        ).all()
    else:
        events = Event.query.all()
    return render_template('admin/events.html', events=events, user=admin, form=form)


@bp.get('/event')
def get_event() -> str:
    event = Event.query.get(request.args.get('id'))
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    if event is not None:
        return render_template('admin/event.html', event=event, user=admin, branchadmin=BranchAdmin.query.filter_by(branch=event.branch).one_or_none())
    raise exceptions.NotFound()

   
@bp.route('/create-event', methods=['GET', 'POST'])
def create_event() -> str | Response:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    form = EventForm()
    if form.validate_on_submit():
        try:
            db.session.add(
                evt:=Event(
                    name=form.name.data, # type: ignore
                    description=form.description.data, # type: ignore
                    branch=form.branch.data,
                    start_time=form.start_time.data, # type: ignore
                    max_teams=form.max_teams.data, # type: ignore
                    max_team_size=form.max_team_size.data, # type: ignore
                    min_team_size=form.min_team_size.data, # type: ignore
                    details=form.details.data,
                    created_by=admin
                )
            )
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            url = url_for("Admin.get_event", id=Event.query.filter_by(name=form.name.data).one().event_id)
            flash(f"Event with name <strong>{form.name.data}</strong> already exists, <a href={url}>see it</a>.", FlashCategory.DANGER.value)
            return render_template('admin/create_event.html', user=admin, form=form, consts=evt_consts)
        except MinGreaterThanMaxError as e:
            flash(str(e), FlashCategory.DANGER.value)
            return render_template('admin/create_event.html', user=admin, form=form, consts=evt_consts)

        form.thumbnail.data.save(
            thumbnail_path:=os.path.join(
                current_app.instance_path, 
                thumbnails_dir,
                ''.join(str(time.time()).split('.'))+'.'+form.thumbnail.data.filename.split('.')[-1]
            )
        )
        evt.thumbnail = EventThumbnail(path=thumbnail_path)
        db.session.commit()

        flash(f"Event '{evt.name}' has been successfully created.", FlashCategory.SUCCESS.value)
        return redirect(url_for('Admin.get_event', id=evt.event_id))

    return render_template('admin/create_event.html', user=admin, form=form, consts=evt_consts)


@bp.get('/delete-event')
def delete_event() -> Response:
    event = Event.query.get(request.args.get('id'))
    if event is not None:
        db.session.delete(event)
        db.session.commit()
        if (thumbnail_path:=event.thumbnail.path) is not None:
            os.remove(os.path.join(current_app.instance_path, assets_dir, thumbnail_path))
        flash("The event has been deleted successfully.", FlashCategory.SUCCESS.value)
        return redirect(url_for('Admin.home'))
    raise exceptions.NotFound()


@bp.get('/team')
def get_team() -> str:
    team = Team.query.get(request.args.get('id'))
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    if team is not None:
        return render_template('admin/team.html', team=team, user=admin)
    raise exceptions.NotFound()


@bp.get('/teams')
def teams() -> str:
    teams = Team.query.all()
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    return render_template('admin/teams.html', teams=teams, user=admin)


@bp.get('/delete-team')
def delete_team() -> Response:
    team = Team.query.get(request.args.get('id'))
    if team is not None:
        db.session.delete(team)
        db.session.commit()
        flash("The team has been eliminated successfully.", FlashCategory.SUCCESS.value)
        return redirect(url_for('Admin.home'))
    raise exceptions.NotFound()


@bp.get('/get_user')
def get_user() -> str | Response:
    user = User.query.get(request.args.get('id'))
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    if user is not None:
        if user.user_id == admin.user_id:
            return redirect(url_for('Admin.profile'))
        role = user.role
        role_info = None
        match role:
            case Role.PARTICIPANT:
                role_info = Participant.query.get(user.user_id)
            case Role.COORDINATOR:
                role_info = Coordinator.query.get(user.user_id)
            case Role.ORGANIZER:
                role_info = Organizer.query.get(user.user_id)
            case Role.BRANCHADMIN:
                u = BranchAdmin.query.get(user.user_id)
                role_info = (u, Event.query.filter_by(branch=u.branch).all())
        return render_template('admin/user.html', user=admin, target=user, role_info=role_info, role=Role)
    raise exceptions.NotFound()


@bp.get('/users')
def users() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    users = User.query.filter(User.user_id != admin.user_id)
    return render_template('admin/users.html', user=admin, users=users)


@bp.get('/delete-user')
def delete_user() -> Response:
    user = User.query.get(request.args.get('id'))
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    if user is not None:
        if user.user_id == admin.user_id:
            flash("You cannot delete yourself.", FlashCategory.INFO.value)
            return redirect(url_for('Admin.home'))
        dp_path = user.profile_picture.path
        db.session.delete(user)
        db.session.commit()
        if dp_path is not None:
            os.remove(os.path.join(current_app.instance_path, assets_dir, dp_path))
        flash("The user has been deleted successfully.", FlashCategory.SUCCESS.value)
        return redirect(url_for('Admin.home'))
    raise exceptions.NotFound()


@bp.get('/profile')
def profile() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    return render_template('admin/user.html', user=admin, target=admin, profile=True, role=Role, role_info=admin)


@bp.get('/participants')
def participants() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    participants = Participant.query.all()
    return render_template('admin/participants.html', participants=participants, user=admin)


@bp.get('/coordinators')
def coordinators() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    coordinators = Coordinator.query.all()
    return render_template('admin/coordinators.html', user=admin, coordinators=coordinators)


@bp.get('/organizers')
def organizers() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    organizers = Organizer.query.all()
    return render_template('admin/organizers.html', user=admin, organizers=organizers)


@bp.get('/branchadmins')
def branchadmins() -> str:
    admin = User.query.filter_by(email='sohamjobanputra7@gmail.com').one()
    branchadmins = BranchAdmin.query.all()
    return render_template('admin/branchadmins.html', user=admin, branchadmins=branchadmins)
