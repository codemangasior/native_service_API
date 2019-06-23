import os
from Native_Service.lib.email_patterns import performer_queue_alert_email
from Native_Service.lib.email_patterns import customer_queue_alert_email
import random
import string

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


class STAGES:
    IN_QUEUE = "in_queue"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ProgressStages:
    """ Basic logic of email alert system. """

    def __init__(self, data, files):
        self.current_stage = None
        self.data = data
        self.files = files
        self.in_queue_stage()

    def in_queue_stage(self):
        self.current_stage = STAGES.IN_QUEUE
        performer_queue_alert_email(self.data, self.files)
        customer_queue_alert_email(self.data)

    def accepted_stage(self):
        self.current_stage = STAGES.ACCEPTED
        print(self.data)

    def in_progress_stage(self):
        self.current_stage = STAGES.IN_PROGRESS

    def done_stage(self):
        self.current_stage = STAGES.DONE


# the function below can be replaced by django/utils/crypto.get_random_string
# https://github.com/django/django/blob/8590726a5dd3087d40b549580703cd8c74f3d7b1/django/utils/crypto.py#L37
def secret_key_generator():
    lenght = 12
    letters = string.ascii_lowercase
    numbers = string.digits
    signs = letters + numbers
    return "".join(random.choice(signs) for i in range(lenght))
