from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),

    # quiz urls
    path('quiz/<str:domain>/', views.start_quiz, name='start_quiz'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]
