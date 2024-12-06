from django.urls import path

from tinyturret import views

urlpatterns = [
    path('', views.main_turret_view, name='tinyturret-main'),
    path('exceptions/<str:group_key>/', views.exception_views, name='tinyturret-exception'),
]
