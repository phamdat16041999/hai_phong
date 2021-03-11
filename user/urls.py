from django.contrib import admin
from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login', views.login),
    path('', views.index),
    path('logout', views.logout_view),
    path('ViewAlbum', views.ViewAlbum),
    path('ViewMusic', views.ViewMusic),
    path('viewMusicInAlbum/<int:id>/', views.viewMusicInAlbum),
    path('LikeMusic/<int:id>/', views.LikeMusic),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)