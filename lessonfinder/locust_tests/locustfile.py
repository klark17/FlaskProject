from locust import HttpLocust, TaskSet, task
import random


class UserBehavior(TaskSet):

    def on_start(self):
        self.client.post("/user/sign-in", {"username":"Test1User", "password":"test"})

    @task(2)
    def index(self):
        self.client.get("/about")

    @task(1)
    def profile(self):
        self.client.get("/profile")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000