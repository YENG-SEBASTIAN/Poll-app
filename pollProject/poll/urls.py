from django.urls import path, include

from .views import homeView, createPoll, resultsView, vote, complete, expired_session, activate_session

urlpatterns = [
    path('', homeView, name='homeView'),
    path('createPoll/', createPoll, name='createPoll'),
    path('resultsView/<poll_id>/', resultsView, name='resultsView'),
    path('vote/<poll_id>/', vote, name='vote'),
    path('complete/', complete, name='complete'),
    path('expired_session/', expired_session, name='expired_session'),
    path('activate_session/', activate_session, name='activate_session'),
]
