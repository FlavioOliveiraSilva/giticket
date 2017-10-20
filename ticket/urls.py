from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #User authentication
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='/registration/password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_complete,  name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_done, name='password_reset_complete'),
    #url(r'^login/$', auth_views.login, {'template_name': 'ticket/login.html'}, name='login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^$', auth_views.login, {'template_name': 'ticket/registration/login.html'}, name='login'),
    #url(r'^$', auth_views.login, {'template_name': 'ticket/login.html'}, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^ticket_new/$', views.ticket_new, name='ticket_new'),
    url(r'^ticket_overview/$', views.ticket_overview, name='ticket_overview'),
    url(r'^actions/$', views.actions, name='actions'),
    url(r'^ticket_process/$', views.ticket_process, name='ticket_process'),
    url(r'^ticket_detail/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
    url(r'^ticket_sent/$', views.ticket_sent, name='ticket_sent'),
    url(r'^denied/$', views.denied, name='denied'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^proceed_ticket/(?P<ticket_id>\d+)/(?P<next_state_id>\d+)/$', views.proceed_ticket, name='proceed_ticket'),
        ]

