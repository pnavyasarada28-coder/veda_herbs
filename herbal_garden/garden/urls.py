from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_plant, name='add_plant'),
    path('plants/', views.plant_list, name='plant_list'),
    path('api/plants/', views.plant_list, name='api_plant_list'),
    path('plants/<int:id>/', views.plant_detail, name='plant_detail'),
    path('plants/<int:id>/delete/', views.delete_plant, name='delete_plant'),
    path('favourites/', views.favourites, name='favourites'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]