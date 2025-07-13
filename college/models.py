from django.db import models
from django.conf import settings
from PIL import Image
from django.db.models import Q

# QuerySet for CollegeAndUniversities
class CollegeAndUniversitiesQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(summary__icontains=query) | Q(posted_as__icontains=query)
        return self.filter(lookups).distinct()

# Manager for CollegeAndUniversities
class CollegeAndUniversitiesManager(models.Manager):
    def get_queryset(self):
        return CollegeAndUniversitiesQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


#college and university models

class CollegeAndUniversities(models.Model):
    POST_CHOICES = [
        ('university', 'University'),
        ('college', 'College'),
    ]

    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=200, blank=True, null=True)
    website_url = models.CharField(max_length=2000, null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True)
    posted_as = models.CharField(choices=POST_CHOICES, max_length=10)
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'college_collegeanduniversities'

    def __str__(self):
        return self.title or "Untitled University/College"

    def get_picture_url(self):
        if self.picture:
            return f"{settings.MEDIA_URL}{self.picture}"
        return f"{settings.MEDIA_URL}default.png"
