from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    RATING_CHOICES = (
        (0, 'G'),
        (1, 'PG'),
        (2, 'PG-13'),
        (3, 'R'),
    )
    # Default to 'R' (3) so new users can see everything by default
    max_content_rating = models.IntegerField(choices=RATING_CHOICES, default=3)

    def __str__(self):
        return self.user.username