from django.db import models
from users.models import CustomUser
# Create your models here.

class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.end_date

    def __str__(self):
        return self.title

class Candidate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')

    def __str__(self):
        return f"{self.user.username} - {self.election.title}"

class Vote(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['voter', 'candidate']
