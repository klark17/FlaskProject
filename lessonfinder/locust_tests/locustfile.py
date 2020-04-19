from locust import HttpLocust, TaskSet, task


# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:5000
def login(l):
    l.client.post("/user/sign-in", {"username":"Test1User", "password":"test"})


def logout(l):
    l.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/profile")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        self.client.post("/user/sign-in", {"username":"Test1User", "password":"test"})

    @task
    def index(self):
        self.client.get("/about")

    @task
    def about(self):
        self.client.get("/profile")

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000