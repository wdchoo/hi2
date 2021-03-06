from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views as core_views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', core_views.metcon, name='home'),

    url(r'^metcon/$', core_views.metcon, name='metcon'),
    url(r'^gymnastics/$', core_views.gymnastics, name='gymnastics'),
    url(r'^weightlifting/$', core_views.weightlifting, name='weightlifting'),

    url(r'^input_additional_info/$', core_views.input_additional_info, name='input_additional_info$'),
    url(r'^change_info/$', core_views.change_info, name='change_info'),

    url(r'^get_metcon_ranking/$', core_views.get_metcon_ranking, name='get_metcon_ranking'),
    url(r'^get_gymnastics_ranking/$', core_views.get_gymnastics_ranking, name='get_gymnastics_ranking'),
    url(r'^get_weightlifting_ranking/$', core_views.get_weightlifting_ranking, name='get_weightlifting_ranking'),

    url(r'^mypage/$', core_views.mypage, name='mypage'),
    url(r'^input/$', core_views.input, name='input'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),


    #url(r'^get_metcon_input_html/$', core_views.get_metcon_input_html, name='get_metcon_input_html'),

]
