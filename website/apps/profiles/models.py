from django.db import models

from website.apps.core.models import TimestampedModel

# Create your models here.
class Profile(TimestampedModel):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)
    image = models.FileField(max_length=255, upload_to='static/uploads/%Y/%m/%d/', blank=True)


    def __str__(self):
        return self.user.username