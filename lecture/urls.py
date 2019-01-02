from django.conf.urls import url
from . import views

app_name = 'lecture'

urlpatterns = [
	# /lecture/
    url(r'^$', views.index, name='index'),

    # /lecture/id


      # /lecture/id/favorite
    # url(r'^(?P<course_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^classroom/$', views.classroom, name='classroom'),
    url(r'^video/$', views.video, name='video'),
    url(r'^desktop/$', views.desktop, name='desktop'),
    url(r'^collaboration/$', views.collaboration, name='collaboration'),
    url(r'^evaluation/$', views.evaluation, name='evaluation'),
    url(r'^answer/$', views.answer, name='answer'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<podcast_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^podcasts/(?P<filter_by>[a-zA_Z]+)/$', views.podcasts, name='podcasts'),



    url(r'^create_coursepack/$', views.create_coursepack, name='create_coursepack'),
    url(r'^(?P<course_id>[0-9]+)/create_podcast/$', views.create_podcast, name='create_podcast'),
    url(r'^(?P<course_id>[0-9]+)/delete_podcast/(?P<podcast_id>[0-9]+)/$', views.delete_podcast, name='delete_podcast'),
    url(r'^(?P<course_id>[0-9]+)/favorite_course/$', views.favorite_course, name='favorite_course'),
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name='delete_course'),

]