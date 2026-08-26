from django.contrib import admin
from .models import Candidate,Interviewer,Interview,Feedback
admin.site.register(Candidate)
admin.site.register(Interviewer)
admin.site.register(Interview)
admin.site.register(Feedback)
