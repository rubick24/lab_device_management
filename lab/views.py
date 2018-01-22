from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.http import HttpResponse,HttpResponseNotAllowed,HttpResponseRedirect,HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import DeviceType,Device,Repair,Scrap,ApplyRecord
from .forms import ApplyForm,RepairForm,ScrapForm,RegisterForm,LoginForm

# 系统首页
@require_http_methods(["GET"])
def index(request):
    device_count = Device.objects.filter(status=0).count()
    repair_count = Repair.objects.filter(status=0).count()
    apply_count = ApplyRecord.objects.filter(status=0).count()
    apply_count2 = ApplyRecord.objects.filter(status=1).count()
    scrap_count = Scrap.objects.all().count()
    context = {
        'device_count': device_count,
        'repair_count': repair_count,
        'apply_count': apply_count,
        'apply_count2': apply_count2,
        'scrap_count': scrap_count,
    }
    return render(request,'home.html',context)

#用户注册
@require_http_methods(["GET","POST"])
def user_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email =  form.cleaned_data['email']
            password =  form.cleaned_data['password']
            if User.objects.filter(username=username).count() is 0:
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect('/login?msg=register success')
            else:
                return HttpResponseRedirect('/register?msg=username has been used')
        else:
            return HttpResponseRedirect('/register?msg='+str(form.errors))

#用户登录
@require_http_methods(["GET","POST"])
def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/?msg=welcome '+user.username)
            else:
                return HttpResponseRedirect('/login?msg=authenticate failed')
        else:
            return HttpResponseRedirect('/login?msg='+str(form.errors))

#退出登录
@require_http_methods(["GET","POST"])
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/?msg=logout success')

# 设备列表
@require_http_methods(["GET"])
def devices(request):
    if request.method == 'GET':
        param = dict(request.GET)
        if 'page' in param:
            param.pop('page')
        if 'msg' in param:
            param.pop('msg')
        for key, value in  param.items():
            param[key] = value[0]
        devices = Device.objects.filter(**param).order_by('status','-purchase_at')
        #return  HttpResponse(str(param)+'###'+str(devices.count()))
        paginator = Paginator(devices, 10)
        page = request.GET.get('page')
        try:
            device_list = paginator.page(page)
        except PageNotAnInteger:
            device_list = paginator.page(1)
        except EmptyPage:
            device_list = paginator.page(paginator.num_pages)
        return render(request,'lab/device_list.html',{'device_list': device_list})
    return HttpResponseNotAllowed(permitted_methods=["GET"])

#设备详情
@login_required()
@require_http_methods(["GET"])
def device_detail(request,device_id):
    device = get_object_or_404(Device,pk=device_id)
    if device.status == 0:
        context = {
            'device': device
        }
    elif device.status == 1:
        repair = device.repair_set.get(status=0)
        context = {
            'device': device,
            'repair': repair
        }
    else:
        scrap = device.scrap_set.first()
        context = {
            'device': device,
            'scrap': scrap
        }
    return render(request,'lab/device_detail.html',context)

# 直接添加设备 /to do
@require_http_methods(["GET", "POST"])
def add_device(request):
    if request.method == 'GET':
        return render(request,'lab/add_device.html')
    elif request.method == 'POST':
        pass
    return HttpResponseNotAllowed(permitted_methods=["GET", "POST"])

# 申请新设备
@login_required()
@require_http_methods(["GET", "POST"])
def add_apply(request):
    if request.method == 'GET':
        return render(request,'lab/apply.html')
    else:
        form = ApplyForm(request.POST)
        if form.is_valid():
            record = ApplyRecord()
            record.applicant = form.cleaned_data['applicant']
            res = DeviceType.objects.filter(name=form.cleaned_data['device_type'])
            if len(res) != 0:
                record.device_type = res[0]
            else:
                device_type = DeviceType(name=form.cleaned_data['device_type'])
                device_type.save()
                record.device_type = device_type
            record.applicant = form.cleaned_data['applicant']
            record.name = form.cleaned_data['name']
            record.model = form.cleaned_data['model']
            record.unit_price = form.cleaned_data['unit_price']
            record.count = form.cleaned_data['count']
            record.reason = form.cleaned_data['reason']
            record.manufacturer = form.cleaned_data['manufacturer']
            record.apply_at = timezone.now()
            record.save()
            return HttpResponseRedirect('/apply?msg=success')
        else:
            #return HttpResponse(str(form.errors))
            return HttpResponseRedirect('/apply/add?msg='+str(form.errors))

#申请表列表
@login_required()
@require_http_methods(["GET"])
def apply_list(request):
    param = dict(request.GET)
    if 'page' in param:
        param.pop('page')
    if 'msg' in param:
        param.pop('msg')
    for key, value in  param.items():
        param[key] = value[0]
    apply_records = ApplyRecord.objects.all().filter(**param).order_by('status','-apply_at')
    paginator = Paginator(apply_records, 10)
    page = request.GET.get('page')
    try:
        apply_list = paginator.page(page)
    except PageNotAnInteger:
        apply_list = paginator.page(1)
    except EmptyPage:
        apply_list = paginator.page(paginator.num_pages)
    return render(request,'lab/apply_list.html',{'apply_list': apply_list})

#申请表详情
@login_required()
@require_http_methods(["GET"])
def apply_detail(request,apply_id):
    apply = get_object_or_404(ApplyRecord,pk=apply_id)
    return render(request,'lab/apply_detail.html',{'apply':apply})

#接受申请
@login_required()
@require_http_methods(["POST"])
def accept_apply(request,apply_id):
    apply = get_object_or_404(ApplyRecord,pk=apply_id)
    if apply.status == 0:
        apply.status = 1
        apply.accept_at = timezone.now()
        apply.save()
        return HttpResponseRedirect('/apply/' + str(apply.id) +"?msg=accept success")
    else:
        return HttpResponseBadRequest()

#拒绝申请
@login_required()
@require_http_methods(["POST"])
def refuse_apply(request,apply_id):
    apply = get_object_or_404(ApplyRecord,pk=apply_id)
    if apply.status == 0:
        apply.status = 3
        apply.accept_at = timezone.now()
        apply.save()
        return HttpResponseRedirect('/apply/' + str(apply.id) +"?msg=refuse success")
    else:
        return HttpResponseBadRequest()

#完成申请
@login_required()
@require_http_methods(["POST"])
def finish_apply(request,apply_id):
    apply = get_object_or_404(ApplyRecord,pk=apply_id)
    if apply.status == 1:
        apply.status =2
        apply.finish_at = timezone.now()
        apply.save()
        for i in range(apply.count):
            device = Device()
            device.name = apply.name+'-'+str(i+1)
            device.device_type = apply.device_type
            device.model = apply.model
            device.manager = apply.applicant
            device.manufacturer = apply.manufacturer
            device.purchase_at = apply.finish_at
            device.save()
        return HttpResponseRedirect('/apply/' + str(apply.id) +"?msg=finish success")
    else:
        return HttpResponseBadRequest()



# 新增维修记录
@login_required()
@require_http_methods(["GET", "POST"])
def repair_add(request,device_id):
    if request.method == 'GET':
        device = get_object_or_404(Device,pk=device_id)
        return render(request,'lab/repair.html',{'device':device})
    else:
        device = get_object_or_404(Device,pk=device_id)
        form = RepairForm(request.POST)
        if form.is_valid():
            record = Repair()
            record.device = device
            record.price = form.cleaned_data['price']
            record.person_in_charge = form.cleaned_data['person_in_charge']
            record.repair_manufacturer = form.cleaned_data['repair_manufacturer']
            record.start_at = timezone.now()
            record.save()
            device.status = 1
            device.save()
            return HttpResponseRedirect('/repair/'+str(record.id)+'?msg=add repair record success')
        else:
            return HttpResponseRedirect('/device/'+str(device.id)+'/reapir?msg='+str(form.errors))

# 维修记录列表
@login_required()
@require_http_methods(["GET"])
def repair_list(request):
    repairs = Repair.objects.all().order_by('status','-start_at')
    paginator = Paginator(repairs, 10)
    page = request.GET.get('page')
    try:
        repair_list = paginator.page(page)
    except PageNotAnInteger:
        repair_list = paginator.page(1)
    except EmptyPage:
        repair_list = paginator.page(paginator.num_pages)
    return render(request,'lab/repair_list.html',{'repair_list': repair_list})

# 维修记录详情
@login_required()
@require_http_methods(["GET"])
def repair_detail(request,repair_id):
    repair = get_object_or_404(Repair,pk=repair_id)
    return render(request,'lab/repair_detail.html',{'repair': repair})

# 完成维修
@login_required()
@require_http_methods(["POST"])
def finish_repair(request,repair_id):
    repair = get_object_or_404(Repair,pk=repair_id)
    if repair.status == 0:
        repair.status = 1
        repair.device.status = 0
        repair.device.save()
        repair.finish_at =  timezone.now()
        repair.save()

        return HttpResponseRedirect('/repair/'+str(repair.id)+'?msg=finish repair success')
    else:
        return HttpResponseBadRequest()


# 新增报废记录
@login_required()
@require_http_methods(["GET", "POST"])
def scrap_add(request,device_id):
    if request.method == 'GET':
        device = get_object_or_404(Device,pk=device_id)
        return render(request,'lab/scrap.html',{'device':device})
    else:
        device = get_object_or_404(Device,pk=device_id)
        form = ScrapForm(request.POST)
        if form.is_valid():
            record = Scrap()
            record.device = device
            record.scrap_at = timezone.now()
            record.reason = form.cleaned_data['reason']
            record.save()
            device.status = 2
            device.save()
            return HttpResponseRedirect('/scrap/'+str(record.id)+'?msg=scrap success')
        else:
            return HttpResponseRedirect('/device/'+str(device.id)+'/scrap?msg='+str(form.errors))

# 报废记录列表
@login_required()
@require_http_methods(["GET"])
def scrap_list(request):
    scraps = Scrap.objects.all()
    paginator = Paginator(scraps, 10)
    page = request.GET.get('page')
    try:
        scrap_list = paginator.page(page)
    except PageNotAnInteger:
        scrap_list = paginator.page(1)
    except EmptyPage:
        scrap_list = paginator.page(paginator.num_pages)
    return render(request,'lab/scrap_list.html',{'scrap_list': scrap_list})

# 报废记录详情
@login_required()
@require_http_methods(["GET"])
def scrap_detail(request,scrap_id):
    scrap = get_object_or_404(Scrap,pk=scrap_id)
    return render(request,'lab/scrap_detail.html',{'scrap': scrap})