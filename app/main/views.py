from flask import render_template, flash, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from .forms import NagForm, QuickCheckinForm
from ..models import Nag, NagEntry


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/nags', methods=['GET', 'POST'])
@login_required
def nags():
    nags = current_user.nags
    return render_template('nags.html', nags=nags)


@main.route('/nags/new', methods=['GET', 'POST'])
def nag_new():
    form = NagForm()
    if form.validate_on_submit():
        nag = Nag.query.filter_by(user_id=current_user.id, name=form.name.data).first()
        if nag is None:
            nag = Nag(name=form.name.data,
                      frequency=form.frequency.data,
                      message_to_send=form.message_to_send.data,
                      user_id=current_user.id)
            db.session.add(nag)
            db.session.commit()
            flash('A new Nag email has been started.')
            return redirect(url_for('main.nags'))
    return render_template('nag_new.html', form=form)


@main.route('/nags/<int:id>/', methods=['GET', 'POST'])
def nag_edit(id):
    nag = Nag.query.get_or_404(id)
    if nag.user_id != current_user.id:
        abort(404)
    form = NagForm()
    if form.validate_on_submit():
        nag.name = form.name.data
        nag.frequency = form.frequency.data
        nag.message_to_send = form.message_to_send.data
        db.session.add(nag)
        flash('Nag email has been updated.')
        return redirect(url_for('main.nags'))
    form.name.data = nag.name
    form.frequency.data = nag.frequency
    form.message_to_send.data = nag.message_to_send
    return render_template('nag_edit.html', nag=nag, form=form)


@main.route('/nags/<int:id>/checkin/', methods=['POST'])
def quick_checkin(id):
    nag = Nag.query.get_or_404(id)
    if nag.user_id != current_user.id:
        abort(404)
    form = QuickCheckinForm()
    if form.validate_on_submit():
        entry = NagEntry(nag_id=nag.id, note=form.note.data)
        db.session.add(entry)
        return redirect(url_for('main.nags'))

    abort(404)
