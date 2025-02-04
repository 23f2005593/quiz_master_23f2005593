from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

class QuizForm(FlaskForm):
    chapter = SelectField('Chapter', coerce=int, validators=[DataRequired()])
    date_of_quiz = DateField('Date', format='%Y-%m-%d')
    time_duration = StringField('Duration (HH:MM)')
    remarks = TextAreaField('Remarks')
    submit = SubmitField('Save')

class QuestionForm(FlaskForm):
    question_statement = TextAreaField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = RadioField('Correct Option', choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], validators=[DataRequired()])
    submit = SubmitField('Save')