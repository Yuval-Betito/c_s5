from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views  # הוספתי את views של האפליקציה users

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),

    # Password change paths
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    # Add home page route
    path('', views.home, name='home'),  # הגדרת נתיב לדף הבית
]
