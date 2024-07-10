from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    owner = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='owned_event')
    attendees = models.ManyToManyField("users.User", related_name='events_attended')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    