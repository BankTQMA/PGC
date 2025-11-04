from django.test import TestCase, Client
from django.urls import reverse
from .models import GradeResult
from .views import score_to_grade
import json
