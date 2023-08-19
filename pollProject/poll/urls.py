from django.urls import path, include

from .views import (homeView, createPoll, resultsView, vote,  expired_session, openPollView, 
                    openPollTemplate, activate_session, complete, sendOpenPollCode, endPoll)

urlpatterns = [
    path('', homeView, name='homeView'),
    path('createPoll/', createPoll, name='createPoll'),
    path('resultsView/<poll_id>/', resultsView, name='resultsView'),
    path('vote/<poll_id>/', vote, name='vote'),
    path('complete/<poll_id>/', complete, name='complete'),
    path('sendOpenPollCode/<poll_id>/', sendOpenPollCode, name='sendOpenPollCode'),
    path('openPollView/', openPollView, name='openPollView'),
    path('openPollTemplate/', openPollTemplate, name='openPollTemplate'),
    path('endPoll/<poll_id>/', endPoll, name='endPoll'),
    path('expired_session/', expired_session, name='expired_session'),
    path('activate_session/', activate_session, name='activate_session'),
]
