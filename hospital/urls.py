from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'hospital.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'main.views.index_page', name='index_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/get_doctors/json/$', 'main.views.get_doctors',
        name='get_doctors'),
    url(r'^main/get_doctors/json/(?P<spec_id>\d+)/$', 'main.views.get_doctors',
        name='get_doctors'),
]
