from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

from wtforms import DateTimeLocalField

class QuizForm(FlaskForm):
    date_of_quiz = DateField('Date of Quiz', validators=[DataRequired()])
    time_duration = StringField('Time Duration (HH:MM)', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    submit = SubmitField('Save')
    
    def validate_end_time(self, end_time):
        if end_time.data <= self.start_time.data:
            raise ValidationError('End time must be after start time')

class QuestionForm(FlaskForm):
    question_statement = TextAreaField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = RadioField('Correct Option', choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

class QuizAttemptForm(FlaskForm):
    submit = SubmitField('Submit Quiz')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    is_admin = RadioField('User Role', choices=[(False, 'Regular User'), (True, 'Administrator')], 
                         coerce=lambda x: x == 'True', default=False)
    submit = SubmitField('Save User')
    
    def validate_dob(self, dob):
        if dob.data and dob.data > date.today():
            raise ValidationError('Date of birth cannot be in the future')    