from django.apps import apps
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from peacecorps import api, views
from peacecorps.cache import midterm_cache, shortterm_cache

_slug = r'(?P<slug>[a-zA-Z0-9_-]+)'

urlpatterns = patterns(
    '',
    url(r'^donate/?$', midterm_cache(views.donate_landing),
        name='donate landing'),
    url(r'^donate/projects-funds/?$', midterm_cache(views.donate_projects_funds),
        name='donate projects funds'),

    # not cached so the values are up-to-date
    url(r'^donate/campaign/' + _slug + r'/?$',
        midterm_cache(views.donate_campaign), name='donate campaign'),
    url(r'^donate/campaign/' + _slug + r'/success/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_success.jinja'),
        name='campaign success'),
    url(r'^donate/campaign/' + _slug + r'/failure/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_failure.jinja'),
        name='campaign failure'),

    url(r'^donate/project/' + _slug + r'/?$',
        midterm_cache(views.donate_project), name='donate project'),
    # not cached so the values are up-to-date
    url(r'^donate/project/' + _slug + r'/success/?$',
        views.ProjectReturn.as_view(
            template_name='donations/project_success.jinja'),
        name='project success'),
    url(r'^donate/project/' + _slug + r'/failure/?$',
        views.ProjectReturn.as_view(
            template_name='donations/project_failure.jinja'),
        name='project failure'),

    url(r'^donate/country/' + _slug + r'/?$',
        midterm_cache(views.donate_country), name='donate country'),
    # not cached so the values are up-to-date
    url(r'^donate/country/' + _slug + r'/success/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_success.jinja'),
        name='country success'),
    url(r'^donate/country/' + _slug + r'/failure/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_failure.jinja'),
        name='country failure'),
    url(r'^donate/countries', midterm_cache(views.donate_countries),
        name='donate countries'),

    url(r'^donate/memorial/' + _slug + r'/?$',
        midterm_cache(views.donate_memorial), name='donate memorial'),
    # not cached so the values are up-to-date
    url(r'^donate/memorial/' + _slug + r'/success/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_success.jinja'),
        name='memorial success'),
    url(r'^donate/memorial/' + _slug + r'/failure/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_failure.jinja'),
        name='memorial failure'),
    # this needs to be below other donate urls.
    url(r'^donate/' + _slug + r'/?$', midterm_cache(views.donate_general),
        name='donate general'),
    # not cached so the values are up-to-date
    url(r'^donate/' + _slug + r'/success/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_success.jinja'),
        name='general success'),
    url(r'^donate/' + _slug + r'/failure/?$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_failure.jinja'),
        name='general failure'),

    url(r'^donations/contribute/?$', midterm_cache(views.donation_payment),
        name='donations_payment'),
    # not cached so the values are up-to-date
    url(r'^success/?$',
        TemplateView.as_view(template_name='donations/success.jinja'),
        name='donation success'),
    url(r'^failure/?$',
        TemplateView.as_view(template_name='donations/failure.jinja'),
        name='donation failure'),

    url(r'^api/account/' + _slug + r'/?$',
        shortterm_cache(api.GetAccountPercent.as_view())),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if apps.is_installed('paygov'):
    urlpatterns += patterns(
        '', url(r'^callback/', include('paygov.urls', namespace='paygov')))

if apps.is_installed('contenteditor'):
    urlpatterns += patterns(
        '', url(r'^admin/', include('contenteditor.urls')))

if apps.is_installed('tinymce'):
    urlpatterns += patterns(
        '', url(r'^tinymce/', include('tinymce.urls')))

if settings.SIRTREVOR:
    urlpatterns += patterns(
        '', url(r'^sirtrevor/', include('sirtrevor.urls')))
