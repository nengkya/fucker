#Django is named after the legendary jazz guitarist, Django Reinhardt
from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse


#create your tests here.
#writing unit tests, even when you know the result is false (i.e., the test fails), is important for reasons that proves the bug exists
#what if we just fix the bug without a test? the same issue might return without us noticing
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        #was_published_recently() suppose returns False for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days = 30)

        future_question = Question(pub_date = time)

        self.assertIs(future_question.was_published_recently(), False) #import unittest somewhere for assertIs


    def test_was_published_recently_with_old_question(self):
        #was_published_recently() returns False for questions whose pub_date is older than 1 day
        time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        #was_published_recently() returns True for questions whose pub_date is within the last day
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    #create question with given question_text and published the given number of days offset now
    #(negative for questions published in the past, positive for questions that have yet to be published)
    time = timezone.now() + datetime.timedelta(days = days)

    return Question.objects.create(question_text = question_text, pub_date = time)


class QuestionIndexViesTests(TestCase):
    def test_no_questions(self):
        #if no questions exist, an appropriate message is displayed
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No HaGa polls are available !')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        #question with a pub_date in the past are displayed on the index page
        question = create_question(question_text = 'Past question.', days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question]) #past questions appear in latest_question_list

    def test_future_question(self):
        #question with a pub_date in the future are not displayed on the index page
        question = create_question(question_text = 'Future question.', days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], []) #future questions do not appear in latest_question_list

    def test_two_past_questions(self):
        question1 = create_question(question_text = 'Past question .', days = -30)
        question2 = create_question(question_text = 'Past question 2.', days = - 5)
        response = self.client.get(reverse('polls:index'))
        #question2 first sequence because days -5 is the 'latest_question_list'
        #assertQuerySetEqual is specifically designed for comparing Django QuerySet objects
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        #the detail view of a question with a pub_date in the future returns a 404 not found
        future_question = create_question(question_text = 'future question', days = 5)
        #"polls:detail/<int:pk>/"
        url = reverse('polls:detail', args = (future_question.id, ))
        response = self.client.get(url)
        #unittest.TestCase
        #self.assertEqual(2 + 2, 4)  passes
        #self.assertEqual("hello", "hello")  passes
        #self.assertEqual([1, 2, 3], [1, 2, 3])  passes
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        #the detail view of a question with a pub_date in the past displays the question's text
        past_question = create_question(question_text = 'past question', days = -5)
        url = reverse('polls:detail', args = (past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)         
