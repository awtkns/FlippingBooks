from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^about', views.about, name='about'),

    url(r'^contact', views.contact, name='contact'),

    url(r'^login', views.login_r, name='login'),

    url(r'^signup', views.UserFormView.as_view(), name='signup'),

    url(r'^index', views.index, name='index'),

    url(r'^logout', views.logout_r, name='logout'),

    url(r'^mylisting', views.my_listing, name='mylisting'),

    url(r'^search', views.search, name='search'),

    url(r'^add', views.add, name='add'),
]
