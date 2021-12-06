from django.db import models

from website.apps.core.models import TimestampedModel

# Create your models here.
class Profile(TimestampedModel):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)

    image = models.FileField(max_length=255, upload_to='uploads/%Y/%m/%d/')


    def __str__(self):
        return self.user.username