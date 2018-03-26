# from restful_proj.apps.accounts.views import *
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.quotes_home),
    # url(r'^new$', views.create),
    # url(r'^add/$', views.add),
    # url(r'^register/', include('apps.accounts.urls'), name='register'),
    # url(r'^login/', include('apps.accounts.urls'), name='login'),
    # url(r'^logout/', views.logout, name='logout'),
    # url(r'^(?P<user_id>[0-9]+)/$', views.show),
    # url(r'^(?P<user_id>[0-9]+)/(edit)$', views.edit),
    url(r'^/(?P<quote_id>[0-9]+)/(add_fave)/$', views.add_favorite),
    url(r'^/(?P<quote_id>[0-9]+)/(delete)/$', views.delete_quote),
    url(r'^/user/(?P<user_id>[0-9]+)/(all)$', views.get_quotes_by_user),

    # url(r'^(?P<user_id>[0-9]+)/(update)$', views.update),
    # url(r'^(?P<user_id>[0-9]+)/(delete)$', views.destroy),
]