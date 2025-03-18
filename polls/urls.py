from django.urls import path
from . import views


app_name = 'polls'

urlpatterns = [
    #ex: /polls/
    path('', views.IndexView.as_view(), name = "index"),

    #ex: /polls/5
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),

    #ex: /polls/5/vote
    path('<int:question_id>/vote', views.vote, name = 'vote'),

    #ex: /polls/5/result
    #Generic detail view ResultsView must be called with either an object pk or a slug in the URLconf.
    #Reverse for 'results' with arguments '(2,)' not found. 1 pattern(s) tried: ['polls/<int:pk/results\\Z']
    #You are missing the > in the path ('<int:pk/results/', views.ResultsView.as_view(), name='results'),
    #django.core.exceptions.ImproperlyConfigured: URL route '<int:pk/results/>' uses parameter name 'pk/results/' which isn't a valid Python identifier.
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results')
]
