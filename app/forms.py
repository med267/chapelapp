from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Authuser, Couple

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Authuser.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Authuser.query.filter_by(email=email.data).first()
        if user is not None:
          raise ValidationError('Please use a different email address.')


class CoupleForm(FlaskForm):
    p1_first_name = StringField('Client 1 First Name: ', validators=[DataRequired()])
    p1_surname = StringField('Client 1 Last/Family/Surname Name: ', validators=[DataRequired()])
    p2_first_name = StringField('Client 2 First Name: ', validators=[DataRequired()])
    p2_surname = StringField('Client 2 Last/Family/Surname Name: ', validators=[DataRequired()])
    email_p1 = StringField('Primary Email', validators=[DataRequired(), Email()])
    email_p2 = StringField('Alternate Email', validators=[Email()])
    mail_street_address_1 = StringField('Street Address 1: ')
    mail_street_address_2 = StringField('Street Address 2: ')
    mail_city = StringField('City/Town/Village: ')
    mail_state_province = StringField('State/Province/Region: ')
    mail_country = StringField('Country: ')
    mail_postal_code = StringField('Postal Code: ')
    telephone_number = StringField('Telephone Number: ')
    note = TextAreaField('Note: ')
    submit = SubmitField('Register')


    def validate_email(self, email):
        user = Authuser.query.filter_by(email=email_p1.data).first()
        if user is not None:
          raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = Authuser.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
