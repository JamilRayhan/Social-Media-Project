from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from apps.App_Post import views
urlpatterns = [
    path('', views.home,name='home'),
    path('admin/', admin.site.urls),
    path('accounts/',include('apps.App_Login.urls')),
    path('post/',include('apps.App_Post.urls')),
    path('messages/', include('apps.App_Message.urls')),
    path('settings/', include('apps.App_Settings.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)