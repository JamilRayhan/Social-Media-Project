from App_Post import views
from django.urls import path
app_name= 'App_Post'

urlpatterns = [
    path('', views.home,name='home'),
    
]
