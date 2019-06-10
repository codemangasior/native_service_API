import os
from Native_Service.lib.email_patterns import performer_queue_alert_email
from Native_Service.lib.email_patterns import customer_queue_alert_email
import random
import string

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


class ProgressStages:
    """ Basic logic of email alert system. """

    STAGES = ("in_queue", "accepted", "in_progress", "done")

    def __init__(self, data, files):
        self.current_stage = None
        self.data = data
        self.files = files
        self.in_queue_stage()

    def in_queue_stage(self):
        self.current_stage = self.STAGES[0]
        performer_queue_alert_email(self.data, self.files)
        customer_queue_alert_email(self.data)

    def accepted_stage(self):
        self.current_stage = self.STAGES[1]
        print(self.data)

    def in_progress_stage(self):
        self.current_stage = self.STAGES[2]
        pass

    def done_stage(self):
        self.current_stage = self.STAGES[3]
        pass


def secret_key_generator():
    lenght = 12
    letters = string.ascii_lowercase
    numbers = string.digits
    signs = letters + numbers
    return "".join(random.choice(signs) for i in range(lenght))
