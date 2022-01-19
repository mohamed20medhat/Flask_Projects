from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# Config MySQL
#! don't forget to modifiy the connector data
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'YourUserName'
app.config['MYSQL_PASSWORD'] = 'YourPassword'
app.config['MYSQL_DB'] = 'yourDBName'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

#! admin part
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/new_customer', methods=['GET','POST'])
def new_customer():
    #like the login page
    if request.method == 'POST':
        cus_name = request.form['cusName']
        #now we need to connect to the database
        cur = mysql.connection.cursor()
        #now we need to insert the data
        #notice the syntax
        cur.execute("insert into customer(name) values(%s)", [cus_name])
        #now we need to commit the data
        mysql.connection.commit()
        #now we need to close the connection
        cur.close()
        #add flash message
        flash('Customer added successfully')

    return render_template('new_customer.html')


@app.route('/new_dependant', methods=['GET','POST'])
def new_dependant():
    #like the login page
    if request.method == 'POST':
        dep_name = request.form['depName']
        #now we need to connect to the database
        cur = mysql.connection.cursor()
        #now we need to insert the data
        #notice the syntax
        cur.execute("insert into dependants(dep_name,cus_id) values(%s,1)", [dep_name])
        #now we need to commit the data
        mysql.connection.commit()
        #now we need to close the connection
        cur.close()
        #add flash message
        flash('dependant added successfully')

    return render_template('new_dependant.html')


@app.route('/new_hospital', methods=['GET','POST'])
def new_hospital():
    #like the login page
    if request.method == 'POST':
        hos_name = request.form['hosName']
        hos_location = request.form['location']
        hos_plan = int(request.form['plan'])

        if hos_plan >= 3 :
            hos_plan = 3
        elif hos_plan <= 1 :
            hos_plan = 1
        else:
            hos_plan = 2

        #now we need to connect to the database
        cur = mysql.connection.cursor()
        #now we need to insert the data
        #notice the syntax
        cur.execute(
            "insert into hospital(hos_name, location, type_id) values(%s, %s, %s)", [hos_name, hos_location, hos_plan])
        
        #now we need to commit the data
        mysql.connection.commit()
        #now we need to close the connection
        cur.close()
        #add flash message
        flash('hospital added successfully')

    return render_template('new_hospital.html')


@app.route('/view_customers')
def view_customers():
    cur = mysql.connection.cursor()
    result = cur.execute("select * from customer")
    customers = cur.fetchall()
    if result > 0:
        return render_template('view_customers.html', customers=customers)
    else:
        msg = 'no customers found'
        return render_template('view_customers.html', msg=msg)


@app.route('/view_claims')
def view_claims():
    return render_template('view_claims.html')


@app.route('/claims/<string:viewtype>')
def view_claims_type(viewtype):
    cur = mysql.connection.cursor()
    if viewtype == 'show_all':
        result = cur.execute("select * from claims")
    elif viewtype == 'unresolved':
        result = cur.execute("select * from claims where resolved = 0")

    claims = cur.fetchall()
    if result > 0:
        return render_template('claims.html', claims=claims)
    else:
        msg = 'no claims found'
        return render_template('claims.html', msg=msg)


@app.route('/resolve/<string:id>', methods=['GET','POST'])
def resolve_claim(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("update claims set resolved = 1 where claim_id = %s", [id])
        mysql.connection.commit()
        cur.close()
        flash('Claim resolved successfully')
    # return render_template('resolve.html', id=id)
    return render_template('resolve.html')


#! customer part
@app.route('/file_claim', methods=['GET','POST'])
def file_claim():
    #like the login page
    if request.method == 'POST':
        describtion = request.form['describtion']
        expensise = int(request.form['expensise'])
        benficary = request.form['benficary']
        health_care_provider = request.form['HCP']

        #now we need to connect to the database
        cur = mysql.connection.cursor()
        #now we need to insert the data
        #notice the syntax
        cur.execute(
            "insert into claims(expensise, description, cus_id, benficary, health_care_provider) values(%s, %s, 1, %s, %s)", [expensise, describtion, benficary, health_care_provider])

        #now we need to commit the data
        mysql.connection.commit()
        #now we need to close the connection
        cur.close()
        #add flash message
        flash('claim added successfully')

    return render_template('file_claim.html')


#buy plan => user must chose a plan from 1 2 3 
#you can't change cust id
@app.route('/buy_plan', methods=['GET','POST'])
def buy_plan():
    #like the login page
    if request.method == 'POST':
        plan_type = int(request.form['planType'])
        benificary = request.form['benificary']

        if plan_type >= 3:
            plan_type = 3
        elif plan_type <= 1:
            plan_type = 1
        else:
            plan_type = 2

        #now we need to connect to the database
        cur = mysql.connection.cursor()
        #now we need to insert the data
        #notice the syntax
        #you can't change the cus_id
        cur.execute(
            "insert into plan(type_id, cus_id, benficary) values(%s, 1, %s)", [plan_type, benificary])
        
        #now we need to commit the data
        mysql.connection.commit()
        #now we need to close the connection
        cur.close()
        #add flash message
        flash('plan added successfully')

    return render_template('buy_plan.html')


# view plan
@app.route('/plans')
def plans():
    cur = mysql.connection.cursor()
    result = cur.execute("select * from plan where cus_id = 1")
    plans = cur.fetchall()
    if result > 0:
        return render_template('plans.html', plans=plans)
    else:
        msg = 'no plans found'
        return render_template('plans.html', msg=msg)

#!it can show those under each type only. not the whole list like when we add a baisc. the golden should view all the plans
#get all the hospitals under each plan
@app.route('/hospitals/<string:type_id>')
def show_hospitals(type_id):
    cur = mysql.connection.cursor()
    result = cur.execute("select * from hospital where type_id = %s", [type_id])
    hospitals = cur.fetchall()
    if result > 0:
        return render_template('hospitals.html', hospitals=hospitals)
    else:
        msg = 'no hospitals found'
        return render_template('hospitals.html', msg=msg)




if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)