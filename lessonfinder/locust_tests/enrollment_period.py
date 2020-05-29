from locust import HttpUser, SequentialTaskSet, task, between, TaskSet
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
    if result:
        csrf_token = str(result.group(1))
        return csrf_token
    else:
        return False


# sets a hash of params to search for
def search_params(response):
    # year = random.randrange(2020, 2021)
    # month = random.randrange(1, 13)
    # day = random.randrange(1, 29)
    # startDate = date(year, month, day)
    # startTime = time(random.randrange(7, 19))
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    csrf_token = find_token(response)
    if csrf_token:
        params = {"level": random.randrange(1, 7),
                  "location": "Recreation Center " + str(random.randrange(1, 31)),
                  "day": day_of_week[random.randrange(0, len(day_of_week))],
                  "csrf_token": csrf_token}
        return params
    else:
        return False


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
    if result:
        lesson = str(result.group(0))
        return lesson
    else:
        return False


class ExistingUserBehavior(SequentialTaskSet):

    id = str(random.randrange(1, 501))
    username = None
    password = None

    def on_start(self):
        print("Starting existing user...")
        response = self.client.get('/user/sign-in')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        csrf_token = find_token(response)
        if csrf_token:
            self.client.post('/user/sign-in', {'username': self.username,
                                               'password': self.password,
                                               'next': '/',
                                               'reg_next': '/',
                                               'csrf_token': csrf_token,
                                               'submit': 'Sign in'})
        else:
            pass

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))


    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        csrf_token = find_token(response)
        register_self = random.randrange(1, 3)
        if register_self == 1:
            link = find_lesson_id(response, '/register_yourself/\d*')
            if link and csrf_token:
                self.client.request("post", link, auth=(self.username, self.password))
        else:
            link = find_lesson_id(response, '/register/\d*')
            if link and csrf_token:
                response = self.client.request("get", link, auth=(self.username, self.password))
                dep = "Dependent" + self.id
                email = "test" + self.id + "user@mail.com"
                self.client.request("post",
                                    link,
                                    params={
                                    "fName": dep,
                                    "lName": "User",
                                    "contactEmail": email,
                                    "csrf_token": csrf_token
                                   },
                                   auth=(self.username, self.password))
        pass

    @task
    def index(self):
        self.client.get("/about")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":self.username, "password":self.password})


class NewUserBehavior(SequentialTaskSet):
    id = str(random.randrange(501, 1001))
    username = None
    password = None

    @task
    def home(self):
        print("Starting new user...")
        self.client.get("/about")

    @task
    def failed_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register_yourself/\d*')
        if link:
            self.client.request("post", link)
        else:
            pass

    @task
    def signup(self):
        self.client.get("/signup")
        self.client.post("/signup", signup_params(int(self.id)))

    @task
    def start_authorized_user(self):
        response = self.client.get('/user/sign-in')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        csrf_token = find_token(response)
        if csrf_token:
            self.client.post('/user/sign-in', {'username': self.username,
                                               'password': self.password,
                                               'next': '/',
                                               'reg_next': '/',
                                               'csrf_token': csrf_token,
                                               'submit': 'Sign in'})
        else:
            pass

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))

    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register_yourself/\d*')
        if link:
            self.client.request("post", link, auth=(self.username, self.password))
        else:
            pass

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":self.username, "password":self.password})


class RandomBehavior(TaskSet):
    id = str(random.randrange(1, 501))
    username = None
    password = None

    def on_start(self):
        print("starting random behavior...")
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        response = self.client.get('/user/sign-in')
        csrf_token = find_token(response)
        if csrf_token:
            self.client.post('/user/sign-in', {'username': self.username,
                                               'password': self.password,
                                               'next': '/',
                                               'reg_next': '/',
                                               'csrf_token': csrf_token,
                                               'submit': 'Sign in'})
        else:
            pass

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))

    @task
    def edit_username(self):
        response = self.client.request("get",
                                       "/update_username",
                                       auth=(self.username, self.password))
        csrf_token = find_token(response)
        if csrf_token:
            username = self.username + "Changed"
            self.client.request('post',
                                '/update_username',
                                params={'username': username,
                                        'csrf_token': csrf_token,
                                        'submit': 'Submit Changes'},
                                auth=(self.username, self.password))
        else:
            pass

    @task
    def successful_self_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register_yourself/\d*')
        if link:
            self.client.request("post", link, auth=(self.username, self.password))

    @task
    def successful_dep_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, '/register/\d*')
        if link:
            response = self.client.request("get", link, auth=(self.username, self.password))
            dep = "Dependent" + self.id
            email = "test" + self.id + "user@mail.com"
            csrf_token = find_token(response)
            if csrf_token:
                self.client.request("post",
                                    link,
                                    params={
                                        "fName": dep,
                                        "lName": "User",
                                        "contactEmail": email,
                                        "csrf_token": csrf_token
                                    },
                                    auth=(self.username, self.password))

    @task
    def remove_lesson(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        lesson_link = find_lesson_id(profile_resp, '/lesson_info/\d*\?user_id=\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            if lesson_info:
                unregister_self = find_lesson_id(lesson_info, '/unregister/\d*/delete')
                unregister_dep = find_lesson_id(lesson_info, '/unregister_dep/\d*/delete/\d*')
                if unregister_self:
                    self.client.request("post",
                                        unregister_self,
                                        auth=(self.username, self.password))
                else:
                    self.client.request("post",
                                        unregister_dep,
                                        auth=(self.username, self.password))
        else:
            pass

    @task
    def update_dependent(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        lesson_link = find_lesson_id(profile_resp, '/dep_lesson_info/\d*/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            edit_info_link = find_lesson_id(lesson_info, '/edit_registration/\d*')
            edit_page = self.client.get(edit_info_link)
            csrf_token = find_token(edit_page)
            if csrf_token:
                new_email = "change" + self.id + "email@mail.com"
                new_phone = "203-123-45" + self.id
                self.client.post("post",
                                 edit_page,
                                 params={'contactEmail': new_email,
                                         'contactNum': new_phone,
                                         'csrf_token': csrf_token,
                                         'submit': 'Submit Changes'},
                                 auth=(self.username, self.password))
        else:
            pass

    @task
    def delete_dependent(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        delete_link = find_lesson_id(profile_resp, '/remove_dep/\d*')
        if delete_link:
            self.client.request("post",
                                delete_link,
                                auth=(self.username, self.password))
        else:
            pass

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":self.username, "password":self.password})


class WebsiteUser(HttpUser):
    tasks = {
        NewUserBehavior: 1,
        ExistingUserBehavior: 10,
        RandomBehavior: 1
    }
    wait_time = between(3.0, 10.5)