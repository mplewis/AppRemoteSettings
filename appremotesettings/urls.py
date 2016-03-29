"""appremotesettings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from appremotesettings.views import select_api_version

urlpatterns = [
    # /admin/: Admin panel
    url(r'^admin/', admin.site.urls),

    # /api/v#: API endpoint
    url(r'^api/v([0-9]+)/?$', csrf_exempt(select_api_version)),

    # Send all other requests to /admin/
    url(r'^', RedirectView.as_view(url='/admin/')),
]
