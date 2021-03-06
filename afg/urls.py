from django.conf.urls.defaults import *

from afg import utils

rid = "(?P<rid>[-A-Za-z0-9]+)"

urlpatterns = patterns('afg.views',
    url(r'about/$', lambda r: utils.redirect_to('afg.about')),
    url(r'api/$', 'api', name='afg.api'),
    url(r'entry_popup/$', 'entry_popup', name='afg.entry_popup'),
    url(r'search/(?P<api>json)?$', 'search', name='afg.search'),
    url(r'random/$', 'random_entry', name='afg.random_entry'),
    url(r'^id/%s/(?P<api>json)?$' % rid, 'show_entry',
        {'template': 'afg/entry_page.html'}, 
        name='afg.show_entry'),
    url(r'^id/%s\.stub$' % rid, 'show_entry', 
        {'template': 'afg/entry.html'}, 
        name='afg.show_entry_stub'),
    url(r'^$', 'search', {'about': True}, name='afg.about'),
)
