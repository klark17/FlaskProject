from locust import HttpLocust, TaskSet, task, seq_task
import re
import datetime
import random
# import names
# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:5000


class NewUser(TaskSet):
    id = 10

    @task
    def home(self):
        self.client.get("/about")

    # @seq_task(1)
    # def search(self):
    #     params = {}
    #     self.client.get("/search")
    #     self.client.post("/search", params)

    # @seq_task(2)
    # def failed_register(self):
    #     self.client.post("/register")

    @task
    def signup(self):
        id = str(self.id + 1)
        year = random.randrange(1960, 2001)
        month = random.randrange(1, 13)
        day = random.randrange(1, 29)
        params = {"fName": "Test" + id,
                  "lName": "User",
                  "email": "test" + id + "user@mail.com",
                  "birthday": datetime.date(year, month, day),
                  "username":"Test" + id + "User",
                  "password": "thisI5theTeSt" + id}
        self.client.get("/signup")
        self.client.post("/signup", params)

    # def login(self):
    # repeated logic that for passing a token
        # response = self.client.get('/user/sign-in')
        # pattern = 'csrf_token.*csrf_token.*value[=]["](.*)["]'
        # result = re.search(pattern, response.text)
        # csrf_token = str(result.group(1))
        # self.client.post('/user/sign-in', {'username': 'Test1User',
        #                                    'password': 'test',
        #                                    'next': '/',
        #                                    'reg_next': '/',
        #                                    'csrf_token': csrf_token,
        #                                    'submit': 'Sign in'})

    # @seq_task(4)
    # def profile(self):
    #     self.client.get("/profile")

    # def on_stop(self):
    #     self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class ExistingUser(TaskSet):

    def on_start(self):
        response = self.client.get('/user/sign-in')
        pattern = 'csrf_token.*csrf_token.*value[=]["](.*)["]'
        result = re.search(pattern, response.text)
        csrf_token = str(result.group(1))
        self.client.post('/user/sign-in', {'username': 'Test1User',
                                           'password': 'test',
                                           'next': '/',
                                           'reg_next': '/',
                                           'csrf_token': csrf_token,
                                           'submit': 'Sign in'})

    @task
    def index(self):
        self.client.get("/about")

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=("Test1User", "test"))

    # seq_task: search for lesson
    # seq_task select to register

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = NewUser
    min_wait = 10000
    max_wait = 30000

