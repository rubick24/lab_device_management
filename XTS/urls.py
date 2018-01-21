from django.conf.urls import url
from django.contrib import admin
from lab.views import index,user_register,user_login,user_logout
from lab.views import devices,device_detail
from lab.views import add_apply,apply_list,apply_detail,accept_apply,refuse_apply,finish_apply
from lab.views import repair_add,repair_list,repair_detail,finish_repair
from lab.views import scrap_add,scrap_list,scrap_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),

    #用户
    url(r'^register$',user_register),
    url(r'^login$',user_login),
    url(r'^logout$',user_logout),

    #设备
    url(r'^device/$', devices),
    url(r'^device/add$', devices),
    url(r'^device/(?P<device_id>[0-9]+)$',device_detail),

    #申请设备相关
    url(r'^apply/add$',add_apply),
    url(r'^apply$',apply_list),
    url(r'^apply/(?P<apply_id>[0-9]+)$',apply_detail),
    url(r'^apply/(?P<apply_id>[0-9]+)/accept$',accept_apply),
    url(r'^apply/(?P<apply_id>[0-9]+)/refuse$',refuse_apply),
    url(r'^apply/(?P<apply_id>[0-9]+)/finish$',finish_apply),

    #维修设备相关
    url(r'^device/(?P<device_id>[0-9]+)/repair$',repair_add),
    url(r'^repair/$',repair_list),
    url(r'^repair/(?P<repair_id>[0-9]+)$',repair_detail),
    url(r'^repair/(?P<repair_id>[0-9]+)/finish$',finish_repair),

    #报废设备相关
    url(r'^device/(?P<device_id>[0-9]+)/scrap$',scrap_add),
    url(r'^scrap/$',scrap_list),
    url(r'^scrap/(?P<scrap_id>[0-9]+)$',scrap_detail),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
