from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('torrent/<int:torrent_id>/', views.torrent, name='torrent'),
    path('about/', views.about, name='about'),
    path('download/<int:torrent_id>/', views.download, name='download'),
    path('parse_site/', views.parse_site, name='parse_site')
    #path('item/<str:item_name>/<str:item_id>/', views.item, name='item'),
    #path('^media/(?P<path>.*)$', views.media, name="media")
]
