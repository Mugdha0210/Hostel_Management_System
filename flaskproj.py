from flask import Flask, render_template, flash, redirect, request, session
from flask_mysqldb import MySQLdb
from flask_mysqldb import MySQL
from forms import *
import MySQLdb.cursors

import re
import hashlib
import string

app = Flask(__name__)
# app instance of flask

# static templates sathi render_template karu shKTO
app.config['SECRET_KEY'] = '4e9c884a5a717a5980682d23c6cbf27c'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password@123'
app.config['MYSQL_DB'] = 'Hostel'

info_list = [
    {
        'Student': '',
        'MIS': '',
        'Address': '',
        'Gender': '',
        'Contact': ''
    }
]

mysql = MySQL(app)


@app.route('/')
@app.route('/home')
# 2 paths handled by same home() function
def home():
    try:
        if session['loggedin']:
            pass

    except:
        info_list = [
            {
                'Student': '',
                'MIS': '',
                'Address': '',
                'Gender': '',
                'Contact': ''
            }
        ]
        flash("Log in to see your profile page", 'warning')
        return render_template('home.html', title='Home', posts=info_list)

    MIS = session['username']

    if MIS == '999999999':
        info_list = [{
            'Student': 'Administrator',
            'MIS': '999999999',
            'Address': 'COEP Hostel, Shivajinagar.',
            'Gender': 'Female',
            'Contact': '9867543210'
        }]
        return render_template('home.html', title='Home', posts=info_list)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Student_Info WHERE MIS = %s', (MIS, ))
    a = cursor.fetchone()
    if not a:
        info_list = [
            {
                'Student': '',
                'MIS': MIS,
                'Address': '',
                'Gender': '',
                'Contact': ''
            }
        ]
    else:
        info_list = [
            {
                'Student': f"{a[1]}  {a[2]}  {a[3]}",
                'MIS': a[0],
                'Address': a[4],
                'Gender': a[5],
                'Contact': a[7]
            }
        ]
    return render_template('home.html', title='Home', posts=info_list)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # check if validated

    msg = ''
    if request.method == 'POST' and form.validate_on_submit() and form.MIS.data and form.password.data:
        MIS = form.MIS.data
        password = form.password.data
        salt = "5gz"
        db_password = password+salt
        h = hashlib.md5(db_password.encode())
        password = h.hexdigest()
        
        cursor = mysql.connection.cursor()
        #cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Login WHERE MIS = % s', (MIS, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            flash(msg, 'danger')
            return render_template('register.html', title='Register', form=form)
        if not form.MIS.data.isnumeric():
            flash("MIS should contain digits only.", 'danger')
            return render_template('register', title='Register', form=form)
        else:
            #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
            cursor.execute(
                'INSERT INTO Login(MIS, password) VALUES (% s, % s)', (MIS, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            # print(msg)
            flash(msg, 'success')
            return redirect('home')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        flash(msg, 'warning')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['loggedin']:
            flash(
                f"You are already logged in as {session['username']}", 'danger')
            return redirect('home')
    except:
        pass
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and form.MIS.data and form.password.data and form.validate_on_submit():
        MIS = form.MIS.data
        password = form.password.data

        salt = "5gz"
        db_password = password+salt
        h = hashlib.md5(db_password.encode())
        password = h.hexdigest()
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM Login WHERE MIS = % s AND password = % s', (MIS, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[0]
            msg = 'Logged in successfully !'
            flash(msg, 'success')
            cursor.execute(
                'SELECT MIS, first_name, middle_name, last_name, student_address FROM Student_Info WHERE MIS = % s', (MIS,))
            stud_data = cursor.fetchone()
            if stud_data:
                global info_list
                info_list[0]['Student'] = f"{stud_data[1]}  {stud_data[2]}  {stud_data[3]}"
                info_list[0]['MIS'] = stud_data[0]
                info_list[0]['Address'] = stud_data[4]
            else:
                info_list[0]['MIS'] = account[0]
                info_list[0]['Student'] = "Full Name"
                flash("Please enter your details.", 'success')
            return redirect('home')
        else:
            msg = 'Incorrect username / password !'
            flash(msg, 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    form = PersonalForm()
    try:
        if session['loggedin']:
            pass

    except:
        flash("Log in to edit personal information", 'warning')
        return render_template('personal.html', title='Personal Details', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        MIS = session['username']
        if not form.contact_no.data.isnumeric():
            flash("Contact should contain digits only.", 'danger')
            return render_template('personal.html', title='Personal Details', form=form)
        try:
            cursor.execute(
                'SELECT * FROM Student_Info WHERE MIS = %s', (MIS, ))
            a = cursor.fetchone()
            print("0")
            if not a:
                cursor.execute('INSERT INTO Student_Info VALUES(% s, % s, %s, %s, %s, %s, %s, %s)', (
                    MIS, form.first_name.data, form.middle_name.data, form.last_name.data, form.student_address.data, form.gender.data.capitalize(), form.isNRI.data, form.contact_no.data))
                mysql.connection.commit()
                print("1")
            else:
                cursor.execute('UPDATE Student_Info SET first_name = %s, middle_name = %s, last_name = %s, student_address = %s, gender = %s, isNRI = %s, contact_no = %s where MIS = %s',
                               (form.first_name.data, form.middle_name.data, form.last_name.data, form.student_address.data, form.gender.data.capitalize(), form.isNRI.data, form.contact_no.data, MIS))
                #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
                print("2")
                mysql.connection.commit()
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('personal.html', title='Personal Details', form=form)

        cursor.execute(
            'SELECT * FROM Student_Info WHERE MIS = % s', (form.MIS.data,))
        stud_data = cursor.fetchone()
        if stud_data:
            global info_list
            info_list = [
                {
                    'Student': f"{stud_data[1]}  {stud_data[2]}  {stud_data[3]}",
                    'MIS': stud_data[0],
                    'Address': stud_data[4],
                    'Gender': stud_data[5],
                    'Contact': stud_data[7]
                }
            ]
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('personal.html', title='Personal Details', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        if session['loggedin']:
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
    except:
        flash("You are not logged in", 'danger')
    return redirect('login')


@app.route('/academic', methods=['GET', 'POST'])
def academic():
    form = AcadForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("Log in to edit academic details", 'warning')
        return render_template('academic.html', title='Academic Details', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        MIS = session['username']
        try:
            cursor.execute(
                'SELECT * FROM Student_academic_record WHERE MIS = % s', (MIS,))
            a = cursor.fetchone()
            if not a:
                cursor.execute(
                    'INSERT INTO Student_academic_record(MIS) VALUES(%s)', (MIS,))
                mysql.connection.commit()
            cursor.execute('UPDATE  Student_academic_record SET year= %s, branch = %s, CGPA = %s where MIS = %s',
                           (form.year.data, form.branch.data, form.CGPA.data, MIS))
            mysql.connection.commit()

            # after academic details are filled, add the MIS to the respective hostel blocks if criteria are fulfilled.
            cursor.execute('SELECT * FROM stays_in where MIS = %s', (MIS, ))
            a = cursor.fetchone()
            cursor.execute(
                'SELECT * FROM Student_academic_record where MIS = %s', (MIS, ))
            acad = cursor.fetchone()
            flag = 0
            if a:
                if acad == tuple([MIS, form.year.data, form.branch.data, form.CGPA.data]):
                    # print("1")
                    if form.CGPA.data < 5.00 and form.year.data != 'First Year B.Tech':
                        cursor.execute(
                            'DELETE FROM stays_in where MIS = %s', (MIS, ))
                        mysql.connection.commit()
                        # print("2")
                else:
                    #print("Not same")
                    flag = 1
            else:
                if form.CGPA.data >= 5.00 or form.year.data == 'First Year B.Tech':
                    cursor.execute(
                        'INSERT INTO stays_in(MIS) VALUES(%s)', (MIS, ))
                    mysql.connection.commit()
                    cursor.execute('INSERT INTO Mess(MIS) VALUES(%s)', (MIS, ))
                    mysql.connection.commit()
                    flag = 1
                else:
                    flag = 0
            if flag == 1:
                cursor.execute(
                    'SELECT gender, isNRI FROM Student_Info WHERE MIS = %s', (MIS,))
                a = cursor.fetchone()
                # print(a[0])
                cursor.execute(
                    'select count(MIS) from stays_in where block_code = %s', ('A',))
                a_count = cursor.fetchone()
                # print(a_count)
                cursor.execute(
                    'select num_rooms from Hostel_blocks where block_code = %s', ('A',))
                a_total = cursor.fetchone()
                # print(a_total)
                if form.year.data == 'First Year B.Tech':
                    if a[0].lower() == 'male':
                        cursor.execute(
                            'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('H', MIS))
                        mysql.connection.commit()
                    elif a[1]:
                        cursor.execute(
                            'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('GHB', MIS))
                        mysql.connection.commit()
                    elif a_count <= a_total:
                        cursor.execute(
                            'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('A', MIS))
                        mysql.connection.commit()
                    else:
                        cursor.execute(
                            'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('B', MIS))
                        mysql.connection.commit()
                elif a[0].lower() == 'female':
                    cursor.execute(
                        'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('GHB', MIS))
                    mysql.connection.commit()
                elif form.year.data == 'Second Year B.Tech':
                    cursor.execute(
                        'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('I', MIS))
                    mysql.connection.commit()
                elif form.year.data == 'Third Year B.Tech':
                    cursor.execute(
                        'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('F', MIS))
                    mysql.connection.commit()
                elif form.year.data == 'Final Year B.Tech':
                    cursor.execute(
                        'UPDATE stays_in SET block_code = %s WHERE MIS = %s', ('C', MIS))
                    mysql.connection.commit()
                else:
                    pass

        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('academic.html', title='Academic Details', form=form)
        flash("Academic details updated.", 'success')
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('academic.html', title='Academic Details', form=form)


@app.route('/CET', methods=['GET', 'POST'])
def CET():
    form = CETForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("Log in to edit academic details", 'warning')
        return render_template('CET.html', title='CET Details', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        MIS = session['username']
        try:
            cursor.execute('SELECT * FROM Student_CET WHERE MIS = % s', (MIS,))
            a = cursor.fetchone()
            if not a:
                cursor.execute(
                    'INSERT INTO Student_CET(MIS) VALUES(%s)', (MIS,))
                mysql.connection.commit()
            cursor.execute('UPDATE  Student_CET SET CET_rank= %s where MIS = %s',
                           (form.CET_rank.data, MIS))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            mysql.connection.commit()
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('CET.html', title='CET Details', form=form)
        flash("CET details updated.", 'success')
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('CET.html', title='CET Details', form=form)


@app.route('/BP', methods=['GET', 'POST'])
def BP():
    form = BPForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("Log in to edit academic details", 'warning')
        return render_template('BP.html', title='BP Details', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        MIS = session['username']
        try:
            cursor.execute(
                'SELECT * FROM Student_board_percentage WHERE MIS = % s', (MIS,))
            a = cursor.fetchone()
            if not a:
                cursor.execute(
                    'INSERT INTO Student_board_percentage(MIS) VALUES(%s)', (MIS,))
                mysql.connection.commit()
            cursor.execute('UPDATE  Student_board_percentage SET board_percentage= %s where MIS = %s',
                           (form.board_percentage.data, MIS))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            mysql.connection.commit()
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('BP.html', title='BP Details', form=form)
        flash("Board Percentage details updated.", 'success')
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('BP.html', title='BP Details', form=form)


@app.route('/hostel', methods=['GET', 'POST'])
def hostel():
    form = HostelForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in.", 'warning')
        return redirect('home')

    MIS = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT MIS, Hostel_blocks.block_code, room_number, mess_name, total_bill FROM (stays_in NATURAL JOIN Mess) LEFT JOIN Hostel_blocks on Hostel_blocks.block_code = stays_in.block_code WHERE MIS = %s', (MIS,))
    table = cursor.fetchone()
    if request.method == 'POST':
        try:
            if form.room_number.data:
                cursor.execute(
                    'UPDATE stays_in SET room_number = %s where MIS = %s', (form.room_number.data, MIS))
                mysql.connection.commit()
                flash(f"Room number updated successfully.", 'success')
                return redirect('home')

            if form.transaction_id.data:
                cursor.execute('SELECT * FROM pays WHERE MIS = %s', (MIS, ))
                a = cursor.fetchone()
                if a :
                    flash("You have already submitted fee payment details.", 'danger')
                    return render_template('hostel.html', title='Hostel', form=form, table=table)
                try:
                    cursor.execute(
                        'INSERT INTO pays VALUES(%s, %s)', (MIS, form.transaction_id.data))
                    mysql.connection.commit()
                except:
                    flash("You have already updated fee payment details.", 'danger')
                    return render_template('hostel.html', title='Hostel', form=form, table=table)
                cursor.execute(
                    'INSERT INTO Fees VALUES(%s, %s)', (form.transaction_id.data, form.date.data))
                mysql.connection.commit()
                flash(f"Fee payment details updated successfully.", 'success')
                return redirect('home')
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
    return render_template('hostel.html', title='Hostel', form=form, table=table)


@app.route('/mess-admin', methods=['GET', 'POST'])
def mess_admin():
    form = MessForm()
    # ITHUN CONTINUE KAR. DISPLAY MESS MADHLI MULA, FEE BHARLI KA VAGARE
    # view mis, mess name, days, bill, has paid
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "999999999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT MIS, mess_name, total_bill FROM (stays_in LEFT JOIN Hostel_blocks ON stays_in.block_code = Hostel_blocks.block_code) NATURAL JOIN Mess')
    table = cursor.fetchall()

    if request.method == 'POST':
        print("in if")
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE Mess SET total_bill = 0 where total_bill is NULL')
        mysql.connection.commit()
        try:
            #block_code = ele[1].upper()
            if form.num_meals.data:
                print("1")
                if form.num_meals.data < 16:
                    flash("Minimum 16 meals per month are mandatory.", 'danger')
                    return render_template('mess-admin.html', title='Mess-Admin', form=form, table=table)
                cursor.execute('UPDATE  Mess SET number_of_meals = %s where MIS = %s',
                               (form.num_meals.data, form.MIS.data))
                mysql.connection.commit()
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())

            print("2")
            cursor.execute('UPDATE  Mess SET hasPaid= %s where MIS = %s',
                           (form.has_paid.data, form.MIS.data))
            mysql.connection.commit()
            if form.month_bill.data:
                print("3")
                if form.has_paid.data:
                    cursor.execute('UPDATE  Mess SET total_bill = %s where MIS = %s',
                                   (form.month_bill.data, form.MIS.data))
                    mysql.connection.commit()
                else:
                    cursor.execute('UPDATE  Mess SET total_bill = total_bill + %s where MIS = %s',
                                   (form.month_bill.data, form.MIS.data))
                    mysql.connection.commit()
            else:
                month_bill = 0
                if form.has_paid.data:
                    cursor.execute('UPDATE  Mess SET total_bill = %s where MIS = %s',
                                   (month_bill, form.MIS.data))
                    mysql.connection.commit()
                else:
                    cursor.execute('UPDATE  Mess SET total_bill = total_bill + %s where MIS = %s',
                                   (form.month_bill.data, form.MIS.data))
                    mysql.connection.commit()

        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('mess-admin.html', title='Mess-Admin', form=form, table=table)
        flash("Mess details updated.", 'success')
        return redirect('home')
    else:
        print("in else")
        flash("Please enter details in correct format.", 'danger')
    return render_template('mess-admin.html', title='Mess-Admin', form=form, table=table)

    # MESS STAFF


@app.route('/hostel-admin', methods=['GET', 'POST'])
def hostel_admin():
    form = HostelBlocks()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "999999999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        block_code = form.block_code.data.upper()
        try:
            cursor.execute(
                'SELECT * FROM Hostel_blocks WHERE block_code = % s', (block_code,))
            a = cursor.fetchone()
            if not a:
                cursor.execute(
                    'INSERT INTO Hostel_blocks(block_code) VALUES(%s)', (block_code,))
                mysql.connection.commit()
            if form.block_name.data:
                cursor.execute('UPDATE  Hostel_blocks SET block_name= %s where block_code = %s',
                               (form.block_name.data, block_code))
                mysql.connection.commit()
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            if form.num_floors.data:
                cursor.execute('UPDATE  Hostel_blocks SET num_floors= %s where block_code = %s',
                               (form.num_floors.data, block_code))
                mysql.connection.commit()
            if form.num_rooms.data:
                cursor.execute('UPDATE  Hostel_blocks SET num_rooms= %s where block_code = %s',
                               (form.num_rooms.data, block_code))
                mysql.connection.commit()
            if form.mess_name.data:
                cursor.execute('UPDATE  Hostel_blocks SET mess_name= %s where block_code = %s',
                               (form.mess_name.data, block_code))
                mysql.connection.commit()
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('hostel-admin.html', title='Admin-Hostel', form=form)
        flash("Hostel Blocks details updated.", 'success')
        return redirect('home')
    else:
        flash("Please enter details in correct format.", 'danger')
    return render_template('hostel-admin.html', title='Admin-Hostel', form=form)


@app.route('/fees-admin', methods=['GET', 'POST'])
def fees_admin():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "999999999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT MIS FROM stays_in WHERE MIS NOT IN (SELECT MIS FROM pays)')
    table = cursor.fetchall()
    cursor.execute(
        'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    table1 = cursor.fetchall()
    return render_template('fees-admin.html', table=table, table1=table1)


@app.route('/staff-admin', methods=['GET', 'POST'])
def staff_admin():
    form = StaffForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "999999999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT Staff.ID, first_name, middle_name, last_name, Staff_payments.job, salary, works_for.block_code, isOutsourced FROM ((Staff LEFT JOIN Staff_payments ON Staff_payments.job = Staff.job) LEFT JOIN works_for ON Staff.ID = works_for.ID)')
    table = cursor.fetchall()

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        if form.ID.data:
            if not form.ID.data.isnumeric() or len(form.ID.data) != 9:
                flash("ID should be 9 digits only.", 'danger')
                return render_template('staff-admin.html', title='Admin-Staff', form=form)
            try:
                cursor.execute(
                    'SELECT * FROM Staff WHERE ID = % s', (form.ID.data,))
                a = cursor.fetchone()
                if not a:
                    cursor.execute(
                        'INSERT INTO Staff(ID, first_name) VALUES(%s, %s)', (form.ID.data, form.first_name.data))
                    mysql.connection.commit()
                if form.middle_name.data:
                    cursor.execute('UPDATE Staff SET middle_name= %s where ID = %s',
                                   (form.middle_name.data, form.ID.data))
                    mysql.connection.commit()
                if form.last_name.data:
                    cursor.execute('UPDATE Staff SET last_name= %s where ID = %s',
                                   (form.last_name.data, form.ID.data))
                    mysql.connection.commit()
                if form.job.data:
                    cursor.execute('UPDATE Staff SET job= %s where ID = %s',
                                   (form.job.data, form.ID.data))
                    mysql.connection.commit()
                if form.block_code.data:
                    cursor.execute(
                        'SELECT * FROM works_for WHERE ID = % s', (form.ID.data,))
                    a = cursor.fetchone()
                    if not a:
                        cursor.execute(
                            'INSERT INTO works_for(ID, block_code) VALUES(%s, %s)', (form.ID.data, form.block_code.data))
                        mysql.connection.commit()
                    else:
                        cursor.execute('UPDATE works_for SET block_code= %s where ID = %s',
                                       (form.block_code.data, form.ID.data))
                        mysql.connection.commit()
            except Exception as e:
                flash(f"Not committed to database as {e}", 'danger')
                return render_template('staff-admin.html', title='Admin-Staff', form=form)
            flash("Staff details updated.", 'success')
            return render_template('staff-admin.html', title='Admin-Staff', form=form)
        if form.salary.data:
            try:
                cursor.execute(
                    'SELECT salary FROM Staff_payments WHERE job = % s', (form.job.data,))
                a = cursor.fetchone()
                if not a:
                    cursor.execute(
                        'INSERT INTO Staff_payments VALUES(%s, %s, %s)', (form.job.data, form.salary.data, form.isOutsourced.data))
                    mysql.connection.commit()
                else:
                    cursor.execute('UPDATE Staff SET salary = %s, isOutsourced = %s where job = %s',
                                   (form.salary.data, form.isOutsourced.data, form.job.data))
                    mysql.connection.commit()
            except Exception as e:
                flash(f"Not committed to database as {e}", 'danger')
                return render_template('staff-admin.html', title='Admin-Staff', form=form, table=table)
            flash("Staff details updated.", 'success')
            return render_template('staff-admin.html', title='Admin-Staff', form=form, table=table)
    else:
        flash("Please enter details in correct format.", 'danger')
    return render_template('staff-admin.html', title='Admin-Staff', form=form, table=table)


# Run directly using python
if __name__ == '__main__':
    app.run(debug=True)
