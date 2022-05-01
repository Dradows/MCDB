"""MCDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from app import views

urlpatterns = [
    re_path(r'MCDB/', include(
        [
            path('admin/', admin.site.urls),
            path('test/', views.test),
            path('', views.blank),
            path('ccdownload/', views.ccdownload),
            path('pcdownload/', views.pcdownload),
            path('cdownload/', views.cdownload),
            path('gdownload/', views.gdownload),
            path('index_html/', views.index_html),
            path('data_html/', views.data_html),
            path('gene_html/', views.gene_html),
            path('gene_search/', views.gene_search),
            path('go/', views.go_search),
            path('compound_html/', views.compound_html),
            path('compound_search/', views.compound_search),
            path('pdb_html/', views.pdb_html),
            path('pdb_search/', views.pdb_search),
            path('ccompare_html/', views.ccompare_html),
            path('ccompare_search/', views.ccompare_search),
            path('pcompare_html/', views.pcompare_html),
            path('pcompare_search/', views.pcompare_search),
            path('upload_html/', views.upload_html),
            path('gene_upload/', views.gene_upload),
            path('compound_upload/', views.compound_upload)
        ]
    ))
]
