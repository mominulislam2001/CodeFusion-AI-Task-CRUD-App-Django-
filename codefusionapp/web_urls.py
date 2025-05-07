from django.urls import path
from .views_web import (
    countries_view, regional_view, language_view,
    country_detail_view, add_country, edit_country, delete_country
)

urlpatterns = [
    path('',countries_view,  name='countries'),
    path('regional/<int:pk>/',regional_view,name='country-regional'),
    path('language/<str:code>/',language_view,name='country-language'),
    path('detail/<int:pk>/',country_detail_view,name='country-detail'),

    
    path('add/',add_country,name='country-add'),

    path('edit/<int:pk>/',edit_country,name='country-edit'),
    path('delete/<int:pk>/', delete_country,name='country-delete'),
]
