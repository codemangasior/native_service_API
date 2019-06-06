import os
from ..models import NativePost
from ..forms import NativePostForm
from Native_Service.lib.email_patterns import performer_queue_alert_email


os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


class ProgressStages:

    STAGES = ("in_queue", "accepted", "in_progress", "done")

    def __init__(self, data):
        self.current_stage = None
        self.data = data
        self.in_queue_stage()

    def in_queue_stage(self):
        self.current_stage = self.STAGES[0]
        performer_queue_alert_email(self.data)

    def accepted_stage(self):
        self.current_stage = self.STAGES[1]
        print(self.data)
