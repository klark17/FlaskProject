from locust import HttpUser, SequentialTaskSet, task
import re
import datetime
from datetime import date, time
import random
import pdb
# import names
# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f enrollment_period.py --host=http://127.0.0.1:5000

# finds csrf_token on the page
def find_token(resp):
    pattern = 'csrf_token.*csrf_token.*value[=]["](.*)["]'
    result = re.search(pattern, resp.text)
    csrf_token = str(result.group(1))
    return csrf_token


# sets a hash of params to search for
def search_params(response):
    year = random.randrange(2020, 2021)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    # startDate = date(year, month, day)
    # startTime = random.randrange(7, 19)
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    params = {"level": random.randrange(1, 7),
              "location": "Recreation Center " + str(random.randrange(1, 31)),
              "day": day_of_week,
              "csrf_token": find_token(response)}
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
              "password": "thi5IztesT" + id}

    return(params)

# finds a random lesson on the page to signup for
def find_lesson_id(resp, pattern):
    result = re.search(pattern, resp.text)
    lesson = str(result.group(0))
    return lesson


class ExistingUser(SequentialTaskSet):

    id = str(random.randrange(1, 501))
    username = None
    password = None
    round = 1

    def on_start(self):
        response = self.client.get('/user/sign-in')
        csrf_token = find_token(response)
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        loggedin = self.client.post('/user/sign-in', {'username': self.username,
                                           'password': self.password,
                                           'next': '/',
                                           'reg_next': '/',
                                           'csrf_token': csrf_token,
                                           'submit': 'Sign in'})

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))


    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        print(self.round)
        if self.round == 1:
            link = find_lesson_id(response, '/register_yourself/\d*')
            print("Hitting a successful existing register with " + link)
            response = self.client.request("post", link, auth=(self.username, self.password))
            print("Existing user has registered for " + link + " with code:")
            print(response)
            self.round = self.round + 1
        else:
            link = find_lesson_id(response, '/register/\d*')
            response = self.client.request("get", link, auth=(self.username, self.password))
            self.client.request("post",
                                link,
                                params={
                                "fName": "Dependent " + self.id,
                                "lName": "User",
                                "contactEmail": "",
                                "csrf_token": find_token(response)
                               },
                               auth=(self.username, self.password))
            self.round = self.round - 1

    @task
    def index(self):
        self.client.get("/about")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":self.username, "password":self.password})


class NewUser(SequentialTaskSet):
    id = str(random.randrange(501, 1001))
    username = None
    password = None

    @task
    def home(self):
        self.client.get("/about")

    @task
    def failed_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register_yourself/\d*')
        self.client.request("post", link)

    @task
    def signup(self):
        self.client.get("/signup")
        self.client.post("/signup", signup_params(int(self.id)))

    @task
    def start_authorized_user(self):
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

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))

    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register_yourself/\d*')
        reg = self.client.request("post", link, auth=(self.username, self.password))

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":self.username, "password":self.password})


class WebsiteUser(HttpUser):
    tasks = [
        NewUser,
        ExistingUser
    ]
    min_wait = 10000
    max_wait = 30000
