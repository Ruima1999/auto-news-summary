from django.urls import path

from . import views

app_name = 'signup'
urlpatterns = [
    path('', views.addemail, name='addemail'),
    path('results/', views.ResultsView.as_view(), name='results'),
]