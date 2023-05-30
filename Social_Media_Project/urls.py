from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from App_Post import views
urlpatterns = [
    path('', views.home,name='home'),
    path('admin/', admin.site.urls),
    path('accounts/',include('App_Login.urls')),
    path('post/',include('App_Post.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)