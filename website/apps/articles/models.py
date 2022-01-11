from django.db import models
from website.apps.core.models import TimestampedModel

# Create your models here.
class Article(TimestampedModel):
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    tags = models.ManyToManyField('articles.Tag', related_name='articles')
    cover = models.FileField(max_length=255, upload_to='static/uploads/%Y/%m/%d/', blank=True)
    markdown_path = models.TextField()
    recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()

    article = models.ForeignKey('articles.Article', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey('profiles.Profile', related_name='comments', on_delete=models.CASCADE)


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag