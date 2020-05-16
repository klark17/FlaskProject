from locust import HttpLocust, TaskSet, task, seq_task
import re
import datetime
from datetime import date, time
import random
import pdb
# import names
# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:5000

# sets a hash of params to search for
def search_params():
    year = random.randrange(2020, 2021)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    # startDate = date(year, month, day)
    # startTime = random.randrange(7, 19)
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    params = {"level": random.randrange(1, 7),
              "location": "Recreation Center " + str(random.randrange(1, 31)),
              "day": day_of_week}
    return params


# sets a set of params to signup with Lesson Finder
def signup_params(num):
    id = str(num + 1)
    year = random.randrange(1960, 2001)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    params = {"fName": "Test" + id,
              "lName": "User",
              "email": "test" + id + "user@mail.com",
              "birthday": datetime.date(year, month, day),
              "username": "Test" + id + "User",
              "password": "thisI5theTeSt" + id}

    return(params)

# finds a random lesson on the page to signup for
def find_lesson_id(resp):
    # TODO: determine the correct regex pattern for this
    pattern = '/register_yourself/\d'
    result = re.search(pattern, resp.text)
    lesson = str(result.group(1))
    return lesson


# finds csrf_token on the page
def find_token(resp):
    pattern = 'csrf_token.*csrf_token.*value[=]["](.*)["]'
    result = re.search(pattern, resp.text)
    csrf_token = str(result.group(1))
    return csrf_token


class NewUser(TaskSet):
    id = 500

    @task
    def home(self):
        self.client.get("/about")

    @seq_task(1)
    def search(self):
        self.client.get("/search")

    @seq_task(2)
    def failed_register(self):
        response = self.client.post("/search", search_params())
        link = find_lesson_id(response)
        self.client.post(link)

    @task
    def signup(self):
        self.client.get("/signup")
        self.client.post("/signup", signup_params(self.id))

    @seq_task(4)
    def profile(self):
        self.client.get("/profile")


class ExistingUser(TaskSet):

    id = str(random.randrange(1, 501))
    username = None
    password = None

    def on_start(self):
        response = self.client.get('/user/sign-in')
        csrf_token = find_token(response)
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post('/user/sign-in', {'username': self.username,
                                           'password': self.password,
                                           'next': '/',
                                           'reg_next': '/',
                                           'csrf_token': csrf_token,
                                           'submit': 'Sign in'})

    @seq_task(1)
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))

    @seq_task(2)
    def search(self):
        self.client.get("/search")

    @seq_task(3)
    def successful_register(self):
        response = self.client.post("/search", search_params())
        pdb.set_trace()
        link = find_lesson_id(response)
        self.client.post(link)

    @task
    def index(self):
        self.client.get("/about")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    # task_set = NewUser
    task_set = ExistingUser
    min_wait = 10000
    max_wait = 30000
