import os
from datetime import date, datetime
import gc
import sqlite3
import json
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from wtforms import Form, SubmitField, TextField, IntegerField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import DateField

from dbconnect import Database
import sys


# -------
# SETUP
# -------

# create application instance
app = Flask(__name__)
app.config.from_object(__name__)

# Function to convert date for SQL - CONSIDER MOVING??
def convertdate(date):
	year = date.year
	month = date.month
	day = date.day
	result = "%d-%d-%d" % (year, month, day)
	return result

# Create database connection
database = Database()

# ---------------------------------------------------------------
#  REQUEST FORM
# ---------------------------------------------------------------

class RequestForm(Form):
	title = TextField('Title', [validators.Length(min=6, max=30),
								validators.Required()])

	proj_type = SelectField('Type', validators=[validators.Required(),
												validators.NoneOf("", message="Cannot be empty")],
							   choices=[('',''),
							   			('CEO escalation', 'CEO escalation'),
										('Community funded project', 'Community funded project'),
										('Ethernet tails', 'Ethernet tails'),
										('FTTP tails', 'FTTP tails'),
										('Spine', 'Spine'),
										('Whitespace', 'Whitespace'),
										('Commissioning', 'Commissioning')])

	product = SelectField('	Product', choices=[('',''),
							   			('CURE', 'CURE (copper rearrangement)'),
							   			('Ethernet', 'Ethernet'),
										('FTTC', 'FTTC (fibre to the cabinet)'),
										('FTTP', 'FTTP (fibre to the premise)'),
										('FTTRN', 'FTTRN (fibre to the remote note)')])

	activity = SelectField('Activity', validators=[validators.Required(),
												   validators.NoneOf("", message="Cannot be empty")],
							   choices=[('',''),
							   			('First Look', 'First Look (Feasibility quick look and quick costing)'),
							   			('Desktop survey', 'Desktop survey (Feasibility and detailed costing)'),
										('Complete Estimate', 'Complete Estimate (Full plan and build)')])

	exchange = TextField('Exchange', validators=[validators.Required(),
												 validators.Length(min=4, max=50)])

	pcp = TextField('PCP', validators=[validators.Required()])

	dps = TextField('DPs', validators=[validators.Required()])

	dateReceived = TextField('Date Received')

	dateRequired = TextField('Date Required')

	priority = SelectField('Priority', validators=[validators.Required(),
												   validators.NoneOf("", message="Cannot be empty")],
									   choices=[('',''),
									   			('CAT 1', 'CAT 1 (must be done now next 2 weeks)'),
									   			('CAT 2', 'CAT 2 (important but can wait up to 1 month)'),
												('CAT 3', 'CAT 3 (low priority of infill work)')])

	requestedBy = TextField('Exchange', validators=[validators.Required(),
												 	 validators.Length(min=4, max=50)])

	thp = TextField('THP', validators=[validators.Required()])

	wfmt = TextField('WFMT ID')

	cfp = TextField('CFP Ref')

	onea = TextField('ONEA Ref')

	ogea = TextField('OGEA Ref')

	notes = TextAreaField('Notes', validators=[validators.Required(),
												 validators.Length(min=4, max=4000)])

	submit = SubmitField('Submit')


# ---------------------------------------------------------------
#  UPDATE STATUS
# ---------------------------------------------------------------


def update_status(pid):
	c, conn = connection()

	c.execute('''SELECT * FROM status WHERE pid = %s''', (pid,))
	project = c.fetchall()

	status = {'custStatus': project[3],
				'custName': project[4],
				'custComplete': project[5],
				'spineStatus': project[6],
				'spineName': project[7],
				'spineComplete': project[8],
				'commStatus': project[9],
				'commName': project[10],
				"commComplete": project[11]}

	if not status['custName']:
		status['custStatus'] = 'Unllocated'
	elif not status['custComplete']:
		status['custStatus'] = 'Allocated'
	else:
		status['custStatus'] = 'Complete'

	if not status['spineName']:
		status['spineStatus'] = 'Unallocated'
	elif not status['spineComplete']:
		status['spineStatus'] = 'Allocated'
	else:
		status['spineStatus'] = 'Complete'

	if not status['commName']:
		status['commStatus'] = 'Unallocated'
	elif not status['commComplete']:
		status['commStatus'] = 'Allocated'
	else:
		status['commStatus'] = 'Complete'

	result = json.dumps({'cust': status['custStatus'],
						 'spine': status['spineStatus'],
					   	 'comm': status['commStatus']})

	c.execute('''UPDATE status
				 SET summary=%s
				 WHERE pid=%s''', (result, pid))
	conn.commit()

	return true


# ---------------------------------------------------------------
#  PAGES
# ---------------------------------------------------------------

# Home
@app.route('/', methods=["GET", "POST"])
def homepage():
	return redirect(url_for('requestproj'))

# REQUESTPROJ
@app.route('/request/', methods=["GET", "POST"])
def requestproj():
	today = datetime.now().date()

	try:
		form = RequestForm(request.form)
		# Capture data from form
		if request.method == "POST" and form.validate():
			title = form.title.data
			proj_type = form.proj_type.data
			product = form.product.data
			activity = form.activity.data
			exchange = form.exchange.data
			pcp = form.pcp.data
			dps = form.dps.data
			dateReceived = convertdate(datetime.strptime(form.dateReceived.data, '%d-%m-%Y'))
			dateRequired = convertdate(datetime.strptime(form.dateRequired.data, '%d-%m-%Y'))
			priority = form.priority.data
			requestedBy = form.requestedBy.data
			thp = form.thp.data
			wfmt = form.wfmt.data
			cfp = form.cfp.data
			ogea = form.ogea.data
			onea = form.onea.data
			notes = form.notes.data
			uid = 12

			# Connect to database
			c, conn = connection()

			# Check if title is already taken
			c.execute('''SELECT title FROM projects WHERE title=%s''', (title,))
		 	check = c.fetchall()
			if len(check) > 0:
				flash('There is already a project with this name, please enter a different one')
				return render_template('request.html', form=form)		# ENDS FUNCTION


			# Insert data into projects table
			values = (uid, title, proj_type, product, activity, exchange, pcp,
					  dps, dateReceived, dateRequired, priority, leadCustomer, thp, other)

			x = c.execute('''INSERT INTO projects (uid, title, type, product,
							activity, exchange, pcp, dps, dateReceived, dateRequired,
							priority, leadCustomer, thp, other)
							VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', values)
			conn.commit()


			# Insert status data
			c.execute('''SELECT pid FROM projects WHERE title=%s''', (title,))
			project_id = c.fetchall()


			c.execute('''INSERT INTO status (pid, uid, dateCreated, custStatus, spineStatus, commStatus)
						 VALUES (%s, %s, %s, %s, %s, %s)''', (project_id, uid, today, 'Unallocated', 'Unallocated', 'Unallocated'))
			conn.commit()


			# Close connection and collect garbage
			c.close()
			conn.close()
			gc.collect()
			flash('Your request has been submitted successfully!')
			return render_template('request.html', form=form)

		# GET METHOD
		else:
			return render_template('request.html', form=form)

	except Exception as e:
		return(str(e))


# SUBMITTED
@app.route('/submitted/')
def submitted():
	return render_template('submitted.html')

# TRACKER
@app.route('/tracker/')
def tracker():
	try:
		c, conn = database.connect()
		c.execute('''SELECT * FROM projects''')
		data = c.fetchall()
		return render_template('tracker.html', data=data)

	except Exception as e:
		return 'There has been a problem, please try again (%s)' % e


@app.route('/settings/')
def settings():
	return 'This will be the SETTINGS'

@app.route('/dashboard/')
def dashboard():
	return render_template('dashboard.html')


# ---------------------------------------------------------------
#  API
# ---------------------------------------------------------------


@app.route('/api/status')
def getStatus():
	try:
		pid = request.args['pid']

		c, conn = database.connect()
		c.execute('''SELECT custStatus, spineStatus, commStatus, summary FROM status WHERE pid=%s''', (pid,))
		data = c.fetchall()

		response = {
			'custStatus': data[0][0],
			'spineStatus': data[0][1],
			'commStatus': data[0][2],
			'summary': data[0][3]
		}

		return json.dumps(response)
	except Exception as e:
		return e

@app.route('/api/project')
def getProject():
	try:
		pid = request.args['pid']

		c, conn = database.connect()
		c.execute('''SELECT * FROM projects WHERE pid=%s''', (pid,))
		data = c.fetchall()

		response = {
			'pid': data[0][0],
			'title': data[0][2],
			'type': data[0][3],
			'product': data[0][4],
			'activity': data[0][5],
			'exchange': data[0][6],
			'pcp': data[0][7],
			'dps': data[0][8],
			'dateRequired': str(data[0][9]),
			'dateReceived': str(data[0][10]),
			'priority': data[0][11],
			'requestedBy': data[0][12],
			'thp': data[0][13],
			'other': data[0][14]
		}
		return json.dumps(response)

	except Exception as e:
		return e





if __name__ == "__main__":
	app.run()
