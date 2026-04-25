from django.urls import path
from .views import *

urlpatterns = [
    path('all/', PublicFeedbackListView.as_view(), name='feedback_all'),
    path('', FeedbackCreateView.as_view(), name='feedback'),
    path('thanks/', FeedbackThanksView.as_view(), name='feedback_thanks'),
    path('list/', FeedbackListView.as_view(), name='feedback_list'),
    path('unread/', UnreadFeedbackListView.as_view(), name='feedback_unread'),
    path('read/<int:pk>/', mark_as_read, name='feedback_read'),
]
