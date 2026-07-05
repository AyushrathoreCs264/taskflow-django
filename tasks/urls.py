from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete_task , name='delete'),
    path('update/<int:id>/', views.update, name='update' ),
    path('complete/<int:id>/', views.complete,name='complete'),
    path('login/' , views.login_page, name="login_page"),
    path('register/' , views.register, name="register"),
    path('logout/' , views.logout_page, name="logout_page"),
]
