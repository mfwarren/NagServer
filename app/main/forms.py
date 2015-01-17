from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import Required, Optional
from flask.ext.login import current_user
from wtforms import ValidationError
from ..models import Nag


class NagForm(Form):
    name = StringField('Name', validators=[Required()])
    frequency = IntegerField('Number of Days', validators=[Required()])
    message_to_send = TextAreaField("Message to Send", validators=[Optional()])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Nag.query.filter_by(user_id=current_user.id, name=field.data).first():
            raise ValidationError('You have a Nag with this name already.')


class QuickCheckinForm(Form):
    submit = SubmitField('Quick Checkin')
