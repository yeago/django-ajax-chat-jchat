# -*- encoding: UTF-8 -*-
"""
URLConf for Chat.

@author: Federico Cáceres <fede.caceres@gmail.com>
"""
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'jchat.views.test'),
    url(r'^send/$', 'jchat.views.send'),
    url(r'^receive/$', 'jchat.views.receive'),
    url(r'^sync/$', 'jchat.views.sync'),

    url(r'^join/$', 'jchat.views.join'),
    url(r'^leave/$', 'jchat.views.leave'),
)