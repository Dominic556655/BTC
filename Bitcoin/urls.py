from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.index, name = 'index'),
        path('Home', views.dashboard, name= 'Home'),
        path('dashboard', views.dashboard, name='dashboard'),
        path('Register', views.Register, name = 'Register'),
        path('logout', views.logout, name='logout'),
        path('login', views.Login, name='login'),
        path('about', views.about, name='about'),
        path('plan', views.plan, name = 'plan'),
        path('deposit', views.transaction, name='deposit'),
        path('withdraw', views.withdraw, name='withdraw'),
        path('transaction', views.transaction, name='transaction'),
        path('news', views.news, name='news'),
        path('single-blog.html', views.single_blog, name='single-blog'),
        path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ]