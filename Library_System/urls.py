"""Library_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home,name='home'),

    url(r'^$', views.login,name='login'),
    url(r'^register/', views.register,name='register'),

    url(r'^book_list/', views.book_list,name='book_list'),
    url(r'^add_book/', views.add_book,name='book_add'),
    url(r'^delete_book/(\d+)', views.delete_book,name='book_delete'),
    url(r'^edit_book/(\d+)', views.edit_book,name='book_edit'),

    url(r'^author_list/', views.author_list,name='author_list'),
    url(r'^add_author/', views.add_author,name='author_add'),
    url(r'^delete_author/(\d+)', views.delete_author,name='author_delete'),
    url(r'^edit_author/(\d+)', views.edit_author,name='author_edit'),
    url(r'^author_detail/(\d+)', views.author_detail,name='author_detail'),

    url(r'^publish_list/', views.publish_list,name='publish_list'),
    url(r'^add_publish/', views.add_publish,name='publish_add'),
    url(r'^delete_publish/(\d+)', views.delete_publish,name='publish_delete'),
    url(r'^edit_publish/(\d+)', views.edit_publish,name='publish_edit'),
]
