from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    # path('', views.index),
    path('', views.PostList.as_view()),
]

