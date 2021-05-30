from django.test import TestCase
from App.models import Quiz
from django.contrib.auth.models import User


class QuizTestCase(TestCase):
    def setUp(self):
        # Creating a user from User Model
        user = User.objects.create_user(username='Salman', password='12345')
        # Creating a record
        Quiz.objects.create(
                            manager          =  user,
                            trivia_api_link  = "https://opentdb.com/api.php.com",
                            score            =  7,
                            time_taken       =  "2 min",
                            user_answers     =  "Answer1,Answer2",
                            )

    def test_quiz_record_count(self):
        """this will test record count"""
        query_set = Quiz.objects.all()
        self.assertEqual(query_set.count(),1)


    def test_quiz_result_method(self):
        """this will test the result() method in Quiz Model Class"""
        quiz_record = Quiz.objects.get(id=1)
        self.assertEqual(quiz_record.result(),"Win")
