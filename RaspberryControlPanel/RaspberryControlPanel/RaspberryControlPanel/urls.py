"""
Definition of urls for RaspberryControlPanel.
"""


from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib import admin

import app.forms
import app.views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^admin$', app.views.admin, name='admin'),
    url(r'^login/$',LoginView.as_view(
        template_name = 'app/login.html',
        authentication_form = app.forms.BootstrapAuthenticationForm ),
        name='login'),     
    url(r'^logout$',LogoutView.as_view(template_name = 'app/logout.html'),
        name='logout'),

]
