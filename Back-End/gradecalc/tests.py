from django.test import TestCase, Client
from django.urls import reverse
from .models import GradeResult
from .views import score_to_grade
import json

class GradeCalcTests(TestCase):

    def setUp(self):
        # Set up a test client that we can use to make requests
        self.client = Client()

    def test_score_to_grade_logic(self):
        """
        Tests the score_to_grade utility function in views.py
        to ensure all grade boundaries are correct.
        """
        print("Testing score_to_grade logic...")
        self.assertEqual(score_to_grade(100), "A")
        self.assertEqual(score_to_grade(80), "A")
        self.assertEqual(score_to_grade(79.9), "B+")
        self.assertEqual(score_to_grade(75), "B+")
        self.assertEqual(score_to_grade(74.9), "B")
        self.assertEqual(score_to_grade(70), "B")
        self.assertEqual(score_to_grade(65), "C+")
        self.assertEqual(score_to_grade(60), "C")
        self.assertEqual(score_to_grade(55), "D+")
        self.assertEqual(score_to_grade(50), "D")
        self.assertEqual(score_to_grade(49.9), "F")
        self.assertEqual(score_to_grade(0), "F")

    def test_calculate_grade_get_api(self):
        """
        Tests the GET /api/calculate/ endpoint.
        """
        print("Testing GET API...")
        url = reverse('calculate_grade') + '?scores=80,90,75&credits=3,3,2'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # --- THIS IS THE CORRECTED VALUE ---
        expected_data = {"GPA": 82.5, "Grade": "A"} 
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_calculate_grade_post_api(self):
        """
        Tests the POST /api/calculate/post/ endpoint.
        """
        print("Testing POST API...")
        url = reverse('calculate_post')

        post_data = {
          "subjects": [
            {"name": "Math", "score": 82, "credit": 3},
            {"name": "ITF", "score": 90, "credit": 2}
          ]
        }

        initial_count = GradeResult.objects.count()
        self.assertEqual(initial_count, 0)

        response = self.client.post(
            url, 
            data=json.dumps(post_data), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # --- THIS IS THE CORRECTED VALUE ---
        expected_data = {"GPA": 85.2, "Grade": "A"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

        final_count = GradeResult.objects.count()
        self.assertEqual(final_count, initial_count + 1)

        saved_result = GradeResult.objects.first()
        self.assertEqual(saved_result.total_gpa, 85.2)
        self.assertEqual(saved_result.grade_letter, "A")

    def test_calculate_grade_post_api_invalid(self):
        """
        Tests that the POST API correctly returns a 400 Bad Request
        error when given invalid data (e.g., score > 100).
        """
        print("Testing POST API with invalid data...")
        url = reverse('calculate_post')

        invalid_data = {
          "subjects": [
            {"name": "Math", "score": 82, "credit": 3},
            {"name": "History", "score": 101, "credit": 2} # Invalid score
          ]
        }

        response = self.client.post(
            url, 
            data=json.dumps(invalid_data), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(GradeResult.objects.count(), 0)