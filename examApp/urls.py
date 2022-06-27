from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('signin',views.signin),
    path('login',views.login),
    path('logout',views.logout),
    path('home',views.home),
    path('makewish',views.wish),
    path('addwish',views.makewish),
    path('<int:_id>', views.delete),
    path('edit/<_id>', views.edit),
    path('update/<_id>', views.update),
    path('like/<_id>', views.like),
    path('grant/<_id>', views.grant),
    path('stats', views.stats),
]