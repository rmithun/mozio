from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from api import views as api_views


router = routers.DefaultRouter()
router.register(r'provider?', api_views.ProviderViewSet)
router.register(r'service?', api_views.ServiceAreaViewset)


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mozio.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(
                           template_name='add_provider/index.html'),
                           name='login'),
                       url(r'^signup/$', TemplateView.as_view(
                           template_name='add_provider/signup.html'),
                           name='provider_signup'),
                       url(r'^define_service/$', TemplateView.as_view(
                           template_name='add_provider/define_service.html'),
                           name='define_service'),
                       url(r'^view_areas/$', TemplateView.as_view(
                           template_name='add_provider/view_areas.html'),
                           name='view_areas'),
                       url(r'^verify_areas/$', TemplateView.as_view(
                           template_name='add_provider/verify_areas.html'),
                           name='verify'),
                       url(r'^get_access/$', api_views.get_access,
                           name='get_access'),
                       url(r'^load_editor/(?P<id>[\d]+)/$',
                           api_views.load_editor,
                           name='edit_service'),
                       url(r'^', include(router.urls)),
                       )
