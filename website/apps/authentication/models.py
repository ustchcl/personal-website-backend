from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    AbstractUser
)

import jwt

from website import settings
from website.apps.core.models import TimestampedModel


# Create your models here.


class User(AbstractUser, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    first_name = None
    last_name = None

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token():
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')