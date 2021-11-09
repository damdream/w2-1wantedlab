from django.contrib import admin
from django.urls import path,include
import crud.views as views


urlpatterns = [
        path('data/injection/', views.DataInjectionView.as_view(),name='data_injection'),
        path('search/<str:company_name>/', views.SearchAPIView.as_view(),name='search_company'),
        path('search', views.AutoCompleteAPIView.as_view(),name='auto_complete'),
        path('enrollment', views.companyEnrollmentView.as_view(), name='enrollment')
    ]

