from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChartView.as_view(), name='charts'),
]   