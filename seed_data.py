from lessonfinder import db, user_manager
from lessonfinder.models import User, Participant, Organization, Lesson
from datetime import date, time, timedelta
import datetime
import calendar
import random


# create users
for i in range(1, 501):
	id = str(i)

	# create random variables for a user
	year = random.randrange(1960, 2001)
	month = random.randrange(1, 13)
	day = random.randrange(1, 29)

	# create a new user
	new_user = User(active=True,
					fName="Test" + id,
					lName="User",
					email="test" + id + "user@mail.com",
					birthday=datetime.date(year, month, day),
					username="Test" + id + "User",
					password=user_manager.hash_password("thi5IztesT" + id))

	# commit user to the database
	db.session.add(new_user)
	db.session.commit()


# create dependents for every other user
for i in range(1, 351):
	id = str(i)

	# set a user that will be the dependents guardian
	current_user = User.query.get(random.randrange(102, 500, 2))
	# create a new dependent
	dep = Participant(fName="Dependent" + id,
					  lName=current_user.lName,
					  contactNum="123-456-78" + id,
					  contactEmail=current_user.email)

	# commit user to the database
	current_user.dependents.append(dep)
	db.session.add(dep)
	db.session.commit()


# create organizations
for i in range(1, 31):
	id = str(i)

	# set a random manager email
	manager_email = "manager" + id + "@mail.com"
	# create organization
	org = Organization(manager="Manager " + id,
					   managerEmail=manager_email,
					   name="Recreation Center " + id,
					   address=str(random.randrange(1, 101)) + " Test Street",
					   town="Test Town",
					   state="CT")

	# commit the org to the database
	db.session.add(org)
	db.session.commit()


# create lessons
for i in range(1, 201):
	id = str(i)

	# set organization that created the lesson
	org = Organization.query.get(random.randrange(1, 31))

	# set random variables for lesson
	year = random.randrange(2020, 2021)
	month = random.randrange(1, 13)
	day = random.randrange(1, 29)
	startDate = date(year, month, day)
	endDate = startDate + timedelta(random.randrange(30, 61))
	day_of_week = calendar.day_name[startDate.weekday()]

	# create lesson
	lesson = Lesson(name="Lesson " + id,
					startDate=startDate,
					endDate=endDate,
					startTime=time(11, 0),
					endTime=time(12, 0),
					contactEmail="manager" + str(org.id) + "@mail.com",
					level=random.randrange(1, 7),
					location="Recreation Center " + str(org.id),
					organization=org,
					instructor="Instructor " + str(org.id),
					desc="This is a description of the lesson for which you are registering.",
					cap=25,
					day=day_of_week)

	# commit lesson to the database
	db.session.add(lesson)
	db.session.commit()