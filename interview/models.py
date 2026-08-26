from django.db import models
from django.contrib.auth.models import User
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Interviewer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)


    def __str__(self):
        return self.name

class Interview(models.Model):
    candidate=models.ForeignKey(Candidate,on_delete=models.CASCADE)
    interviewer=models.ForeignKey(Interviewer,on_delete=models.CASCADE)
    interview_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    mode=models.CharField(max_length=20)
    meeting_link=models.URLField(blank=True)
    status=models.CharField(max_length=20,default='scheduled')
    def __str__(self):
        return f"{self.candidate.name}-{self.interview_date}"

class Feedback(models.Model):
    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE
    )

    technical_rating = models.IntegerField()
    communication_rating = models.IntegerField()
    problem_solving_rating = models.IntegerField()
    overall_rating = models.IntegerField()

    recommendation = models.CharField(max_length=20)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback - {self.interview.candidate.name}"
    