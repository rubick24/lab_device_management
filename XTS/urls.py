from django.urls import path
from django.contrib import admin
from lab.views import index,user_register,user_login,user_logout
from lab.views import devices,device_detail
from lab.views import add_apply,apply_list,apply_detail,accept_apply,refuse_apply,finish_apply
from lab.views import repair_add,repair_list,repair_detail,finish_repair
from lab.views import scrap_add,scrap_list,scrap_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),

    #用户
    path('register',user_register),
    path('login',user_login),
    path('logout',user_logout),

    #设备
    path('device/', devices),
    path('device/add', devices),
    path('device/<int:device_id>',device_detail),

    #申请设备相关
    path('apply/add',add_apply),
    path('apply/',apply_list),
    path('apply/<int:apply_id>',apply_detail),
    path('apply/<int:apply_id>/accept',accept_apply),
    path('apply/<int:apply_id>/refuse',refuse_apply),
    path('apply/<int:apply_id>/finish',finish_apply),

    #维修设备相关
    path('device/<int:device_id>/repair',repair_add),
    path('repair/',repair_list),
    path('repair/<int:repair_id>',repair_detail),
    path('repair/<int:repair_id>/finish',finish_repair),

    #报废设备相关
    path('device/<int:device_id>/scrap',scrap_add),
    path('scrap/',scrap_list),
    path('scrap/<int:scrap_id>',scrap_detail),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
