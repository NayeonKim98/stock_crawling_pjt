from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('delete_stock/<int:pk>/', views.delete_stock, name='delete_stock'),
]