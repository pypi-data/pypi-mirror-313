from django.contrib import admin
from django.urls import path

from tinyturret import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinyturret', views.main_turret_view, name='tinyturret-main'),
    path('tinyturret/exception/<str:group_key>/', views.exception_views, name='tinyturret-exception'),
]
