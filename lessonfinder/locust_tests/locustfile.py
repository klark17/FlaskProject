from locust import HttpLocust, TaskSet, task
from werkzeug.test import Client
from werkzeug.testapp import test_app
import time
import pdb
import re
# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:5000

# class WerkzeugClient(Client):
#     def __getattr__(self, name):
#         func = Client.__getattr__(self, name)
#
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             try:
#                 result = func(*args, **kwargs)
#             except Client.Fault as e:
#                 total_time = int((time.time() - start_time) * 1000)
#                 events.request_failure.fire(request_type="werkzeug", name=name, response_time=total_time, exception=e)
#             else:
#                 total_time = int((time.time() - start_time) * 1000)
#                 events.request_success.fire(request_type="werkzeug", name=name, response_time=total_time,
#                                             response_length=0)
#         return wrapper
#
# class WerkzeugLocust(User):
#
#     abstract = True
#     def __init__(self, *args, **kwargs):
#         super(WerkzeugLocust, self).__init__(*args, **kwargs)
#         self.client = WerkzeugClient(test_app)


class UserBehavior(TaskSet):

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

    def on_stop(self):
        self.client.post("/user/sign-out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 10000
    max_wait = 30000