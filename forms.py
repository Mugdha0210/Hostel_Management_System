from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo

class PersonalForm(FlaskForm) :
    #username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=50)])
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    middle_name = StringField('Middle Name', validators=[Length(max=20)])
    last_name = StringField('Last Name', validators=[Length(max=20)])
    student_address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=20)])
    isNRI = BooleanField('Do you belong to NRI quota?')
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Update')

class LoginForm(FlaskForm) :
    #username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=50)])
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm) :
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AcadForm(FlaskForm) :
    year = StringField('Year (Eg : First Year B.Tech)', validators=[DataRequired(), Length(max=30)])
    branch = StringField('Branch', validators=[DataRequired()])
    CGPA = FloatField('CGPA (enter 0.0 if not applicable)', default=0.00)
    submit = SubmitField('Update')

class CETForm(FlaskForm) :
    CET_rank = FloatField('CET rank (enter 0 if not applicable)', validators=[DataRequired()])
    submit = SubmitField('Update')

class BPForm(FlaskForm) :
    board_percentage = FloatField('Board Percentage', validators=[DataRequired()])
    submit = SubmitField('Update')

class HostelBlocks(FlaskForm) :
    block_code = StringField('Hostel  Block Code', validators=[DataRequired(), Length(max=3)])
    block_name = StringField('Name of the block')
    mess_name = StringField('Name of the associated mess')
    num_floors = IntegerField('Number of floors')
    num_rooms = IntegerField('Number of total rooms')
    submit = SubmitField('Add')

class MessForm(FlaskForm) :
    MIS = StringField('Student MIS', validators=[DataRequired(), Length(min=9, max=9)])
    num_meals = IntegerField('Number of meals this month', default=16)
    month_bill = IntegerField('This month\'s bill')
    has_paid = BooleanField('Is the total bill paid?')
    submit = SubmitField('Update record')

class HostelForm(FlaskForm) :
    room_number = IntegerField('Room number')
    transaction_id = StringField('Transaction ID')
    date = DateField('Payment Date (YYYY-MM-DD)')
    submit = SubmitField('Update')

class StaffForm(FlaskForm) :
    ID = StringField('Staff ID')
    first_name = StringField('First Name', validators=[Length(max=20)])
    middle_name = StringField('Middle Name', validators=[Length(max=20)])
    last_name = StringField('Last Name', validators=[Length(max=20)])
    job = StringField('Job', validators=[Length(max=20)])
    salary = FloatField('Salary in INR')
    block_code = StringField('Works for which hostel block (Enter block-code)', validators=[Length(max=3)])
    isOutsourced = BooleanField('Is the staff member outsourced?')
    submit = SubmitField('Update')
    