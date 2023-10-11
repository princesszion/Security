from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Import the settings module


class CustomUser(AbstractUser):
    Student = 'student'
    Facilitator = 'facilitator'
    Team_Lead = 'team_lead'
    ROLES = [
        (Student,'student'),
        (Facilitator,'facilitator'),
        (Team_Lead,'team_lead'),
    ]
    role = models.CharField(max_length=20, choices=ROLES,default=Student)

    def __str__(self):
         return self.username
    

class AdminRequest(models.Model):
    # student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    description = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.description



    
#     @property
#     def can_view_all_admin_requests(self):
#          return self.role == CustomUser.Team_Lead
    
#     @property
#     def can_view_own_admin_requests(self):
#          return self.role == CustomUser.Student
    
#     @property
#     def can_view_academic_requests(self):
#           return self.role == CustomUser.FACILITATOR

