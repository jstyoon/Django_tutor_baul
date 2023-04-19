# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('', views.home, name='home'),
    # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/', views.tweet, name='tweet')
]
