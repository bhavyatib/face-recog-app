"""trialproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from prof_module.views import *
from stud_module.views import *
from auth_module.views import *

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', login_page),
    re_path(r'^signup/$',signup),
    re_path(r'^login/$',login_page),
    re_path(r'^auth/$',auth),
    re_path(r'^verify/$',before_verify),
    re_path(r'^verification/',after_verify),
    re_path(r'^finish-signup/$',finish_signup),
    re_path(r'^prof_home/$',prof_home),
    re_path(r'^prof_course/([a-zA-Z0-9]+)/$',prof_course),
    # url(r'^add_stud/([a-zA-Z0-9]+)/$',add_stud),
    re_path(r'^daily_report/([a-zA-Z0-9]+)/([0-9]{4})/([0-9]{2})/([0-9]{2})/$',daily_report),
    re_path(r'^prof_history/([a-zA-Z0-9]+)/$',prof_history),
    re_path(r'^take_attendance/([a-zA-Z0-9]+)/$',take_attendance),
    re_path(r'^upload_class_photos/([a-zA-Z0-9]+)/$',upload_class_photos),
    re_path(r'^prof_queries/([a-zA-Z0-9]+)/$',prof_queries),
    re_path(r'^query/([a-zA-Z0-9]+)/$',query),
	re_path(r'^stud_home/$',stud_home),
    re_path(r'^stud_course/([a-zA-Z0-9]+)/$',stud_course),
    re_path(r'^stud_daily_report/$',stud_daily_report),
    re_path(r'^stud_history/([a-zA-Z0-9]+)/$',stud_history),
    re_path(r'^view_queries/([a-zA-Z0-9]+)/$',view_queries),
	re_path(r'^raise_query/([a-zA-Z0-9]+)/$',raise_query),
	re_path(r'^logout/$',logout_view),
	re_path(r'^view_images/$',view_images),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
