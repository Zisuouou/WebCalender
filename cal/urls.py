from django.urls import path
from . import views

app_name = 'cal'

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.CalendarView.as_view(), name='calendar'),
    path("detail/", views.post_detail, name="post_detail"),
]
