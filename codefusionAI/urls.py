from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('admin/', admin.site.urls),

    # ①  API lives under /api/
    path('api/', include('codefusionapp.api_urls')),

    # ②  Web interface & auth
    path('login/', auth_views.LoginView.as_view(
            template_name='codefusionapp/login.html'),
         name='login'),
    
     path('logout/',
         auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),
     
    path('', include('codefusionapp.web_urls')),      # ‘’ → countries table
]