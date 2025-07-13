from django.db import models
from django.shortcuts import render
import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main_app.models import School, Grade, Term, Subject, Educator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#question paper
class QuestionPaper(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    educator = models.ForeignKey(Educator, on_delete=models.DO_NOTHING, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True, blank=True)
    file = models.FileField(upload_to='question_papers/')
    
    COMPLEXITY_CHOICES = [(i, f"Level {i}") for i in range(1, 6)]
    complexity_rating = models.IntegerField(choices=COMPLEXITY_CHOICES)
    topics = models.ManyToManyField(Topic, related_name="question_papers")
    number_of_questions = models.TextField()

    class Meta:
        managed = False
        db_table = 'questpaper_questionpaper'

    def __str__(self):
        return f"{self.grade} - {self.term} - {self.subject.name if self.subject else 'Unknown'}"

#Prospectors
class Prospectors(models.Model):
    institution = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    copy = models.FileField(upload_to='store/prospectors/')
    logo = models.ImageField(upload_to='store/prospectors/')

    class Meta:
        managed = False  # Prevent Django from creating a new table in MA
        db_table = 'questpaper_prospectors'  # Ensure it maps to the correct CMS table

    def __str__(self):
        return self.institution