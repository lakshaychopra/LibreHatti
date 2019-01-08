from django.urls import re_path

from django.views.generic import TemplateView

from librehatti.prints import views


urlpatterns = [        
    re_path(r'^bill/', views.bill, name= 'bill'),
    re_path(r'^suspense_bill/', views.suspense_bill, name= 'suspense_bill'),
    re_path(r'^quoted_bill/',views.quoted_bill, name= 'quoted_bill'),
]	
