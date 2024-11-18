"""
URL configuration for project_database_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.customers, name='customers'),

    path('add/customer', views.add_customers, name='add_customers'),

    path('customer/remove/<int:customer_id>', views.remove_customer, name='remove_customer'),

    path('customer/update/<int:customer_id>', views.update_customer, name='update_customer'),

    path('customer/details/<int:customer_id>', views.customer_details, name='customer_details'),

    # path('statistics', views.statistics, name='statistics'),
    #
    # path('transactions', views.transactions, name='transactions'),
    path('admin/', admin.site.urls),
]
