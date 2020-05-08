from locust import HttpLocust, TaskSet, task
import random
from datetime import date

# This is a load test to simulate a user signing up with the site
class UserBehavior(TaskSet):

    def on_start(self):
        self.client.post("/signup", {"fName":"Test5",
                                     "lName":"User",
                                     "active": True,
                                     "email": "test5user@mail.com",
                                     "birthday": date(2000, 1, 1),
                                     "username":"Test5User",
                                     "password":"pw"})

    @task
    def index(self):
        self.client.get("/about")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000