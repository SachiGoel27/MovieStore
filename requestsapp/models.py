from django.db import models
from django.contrib.auth.models import User

class MovieRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_requests")
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (by {self.user.username})"