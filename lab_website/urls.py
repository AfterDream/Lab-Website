'''This package has the url encodings for the main app.'''
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin, sitemaps
from django.conf.urls.static import static
from django.conf import settings

from tastypie.api import Api

from communication.views import FeedDetailView, LabLocationView

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap, CommentarySitemap
from projects.sitemap import ProjectsSitemap

from papers.api import PublicationResource
from projects.api import ProjectResource
from personnel.api import PersonnelResource

from papers.feeds import LabPapersFeed, InterestingPapersFeed, CommentaryFeed
from projects.feeds import ProjectsFeed

from views import IndexView

class StaticViewSitemap(sitemaps.Sitemap):
    '''This sitemap is for all static pages, including list views home and feeds.'''   
 
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return ['location','feed-details','laboratory-papers','interesting-papers','commentary-list','laboratory-personnel','project-list',
                 'twitter','google-calendar','wikipedia','lab-rules','lab-news','contact-info']

    def location(self, item):
        return reverse(item)

v1_api = Api(api_name='v1')
v1_api.register(PublicationResource())
v1_api.register(ProjectResource())
v1_api.register(PersonnelResource())

#this dictionary lists sitemap files which will be generated.
sitemaps = {
    'personnel': LabPersonnelSitemap,
    'papers': LabPublicationsSitemap,
    'commentary': CommentarySitemap,
    'projects': ProjectsSitemap,
    'static': StaticViewSitemap
    }

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^contact/', include('communication.urls')), 
    url(r'^papers/', include('papers.urls')),
    url(r'^people/', include('personnel.urls')),
    url(r'^projects/', include('projects.urls')),
    
    url(r'location/?$', LabLocationView.as_view(), name="location"),
    
    url(r'^feeds/?$', FeedDetailView.as_view(), name="feed-details"),
    url(r'^feeds/lab-papers/?$', LabPapersFeed(), name="lab-papers-feed"),
    url(r'^feeds/interesting-papers/?$', InterestingPapersFeed(), name="interesting-papers-feed"),
    url(r'^feeds/commentaries/?$', CommentaryFeed(), name="commentary-feed"),
    url(r'^feeds/projects/?', ProjectsFeed(), name="projects-feed"),
       
    (r'^api/',include(v1_api.urls)),   
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^$', IndexView.as_view())
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

