"""custom_User URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


from apps.users.views import (login_view, register_view, logout_view, register_profile)
from apps.quotes.views import (quotes_home, add_new_quote, add_favorite)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', include('apps.core.urls')),
    url(r'^$', include('apps.users.urls')),
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    # url(r'^register/', register_view, name='register'),
    url(r'^register', register_profile, name='register'),
    url(r'^quotes/$', quotes_home, name='quotes'),
    url(r'^quotes', include('apps.quotes.urls')),
    url(r'^add_new_quote/', add_new_quote, name='add_new_quote'),
    # url(r'^(?P<user_id>[0-9]+)/(update)$', views.update),

]
