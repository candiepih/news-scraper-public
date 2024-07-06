from djongo import models
from djongo.models import ArrayField, CharField


class BaseModel(models.Model):
    _id = models.ObjectIdField()
    title = models.TextField()
    image = models.URLField()
    link = models.URLField()
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=[])
    source = models.CharField(max_length=100)
    # digest is a unique value generated for each article, to be used for duplicate detection
    digest = models.CharField(max_length=100, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True
