from App_Settings import views
from django.urls import path

app_name = 'App_Settings'

urlpatterns = [
    path('',views.settings , name='settings'), 
]
