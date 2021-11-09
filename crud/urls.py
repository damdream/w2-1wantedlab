from django.contrib import admin
from django.urls import path,include
import crud.views as views
from .views import companyEnrollmentView

urlpatterns = [
        path('data/injection/', views.DataInjectionView.as_view(),name='data_injection'),

        path('company/enrollment', companyEnrollmentView.as_view())
]