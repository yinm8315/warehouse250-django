# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='dashboard'),
    path('api/changeOrderStatus/<int:id>/<str:val>', views.changeOrderStatus, name='changeOrderStatus'),
    path('api/changeVendorEnalbed/<int:id>/<str:val>', views.changeVendorEnalbed, name='changeVendorEnalbed'),
    # path('api/changeOrderStatus/<int:id>/<str:val>', views.changeOrderStatus, name='changeOrderStatus'),
    # path('api/changeOrderStatus/<int:id>/<str:val>', views.changeOrderStatus, name='changeOrderStatus'),
    # path('api/changeOrderStatus/<int:id>/<str:val>', views.changeOrderStatus, name='changeOrderStatus'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
