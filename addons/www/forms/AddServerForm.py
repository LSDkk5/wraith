from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddServerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': 'Server name/description'})
    ipAddress = StringField('Ip Adress', validators=[DataRequired()], render_kw={'placeholder': 'Server ip adress e.g. 192.168.0.1'})
    rconPassword = PasswordField('RCON password', validators=[DataRequired()], render_kw={'placeholder': 'Password for rcon protocol'})
    rconPort = StringField('RCON port', validators=[DataRequired()], render_kw={'placeholder': 'Rcon port'})
    gameType = SelectField('Game type',choices=[('Minecraft'), ('Rust')])
    submit = SubmitField('Add server')