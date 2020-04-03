from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import FloorPass, Department, Location, Log, User
import requests
import json
from django.utils import timezone


def get_json(id):
    url = "http://idcsi-officesuites.com:8080/hrms/api.php"
    payload = {'what': 'getinfo',
               'field': 'fpass',
               'idno': id,
               'apitoken': 'IUQ0PAI7AI3D162IOKJH',
               }  # 'search': 'FERNANDEZ'
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()


# Create your views here.
def index(request):
    return render(request, 'login.html',
                  {'location_list': Location.objects.all, 'department_list': Department.objects.all})


def login(request):
    data = get_json(request.POST['employee_id'])

    if data['code'] == 0 and not request.POST.get('department_id', '') == '' \
            and not request.POST.get('location_id', '') == '':

        request.session['admin_id'] = request.POST['employee_id']
        request.session['admin_name'] = str(
            '{}, {}'.format(data['message'][0]['last_name'], data['message'][0]['first_name']))
        request.session['location_id'] = request.POST['location_id']
        request.session['department_id'] = request.POST['department_id']

        if request.POST['type'] == '0':
            return HttpResponseRedirect(reverse('floorpass:manager', args=(40,)))
        elif request.POST['type'] == '1':
            return HttpResponseRedirect(reverse('floorpass:log'))
        else:
            return HttpResponse(request.POST['type'], )
    request.session['message'] = 'Invalid Credentials.'
    return HttpResponseRedirect(reverse('floorpass:index'))


def log(request):
    location = get_object_or_404(Location, pk=request.session['location_id'])
    latest_floorpass_list = location.floorpass_set.order_by(
        '-latest_log_date')
    context = {'latest_floorpass_list': latest_floorpass_list, 'guard_id': request.session['employee_id'],
               'location_id': request.session['location_id'], 'message': request.session.get('message', '')}
    return render(request, 'log.html', context)


def log_add(request):
    new_log = Log()
    new_log.logdatetime = timezone.now()
    new_log.location = request.session['location_id']
    new_log.guard_id = request.session['admin_id']
    new_log.floorpass = get_object_or_404(FloorPass, pk=request.POST['ref_id'])
    new_log.floorpass.latest_log_date = timezone.now()
    new_log.floorpass.save()
    new_log.save()

    return HttpResponseRedirect(reverse('floorpass:log'))


def manager(request):
    department = get_object_or_404(Department, pk=request.session['department_id'])
    latest_floorpass_list = department.floorpass_set.order_by(
        '-latest_log_date')
    context = {'latest_floorpass_list': latest_floorpass_list, 'department_list': Department.objects.all,
               'message': request.session.get('message', '')}
    return render(request, 'manager.html', context)


def manager_edit(request, ref_id):
    department = get_object_or_404(Department, pk=request.session['department_id'])
    latest_floorpass_list = department.floorpass_set.order_by(
        '-latest_log_date')
    context = {'latest_floorpass_list': latest_floorpass_list, 'department_list': Department.objects.all,
               'ref_id': ref_id,
               'message': request.session.get('message', '')}
    return render(request, 'manager.html', context)


def verify(request, ref_id):
    emp_inf = get_json(request.POST.get('requestor_employee_ids', ''))
    user = User()
    user.floorpass = get_object_or_404(FloorPass, pk=ref_id)

    if emp_inf['code'] != 0:
        request.session['message'] = 'Invalid Credentials, use a valid Employee ID.'
        return HttpResponseRedirect(reverse('floorpass:manager', args=(ref_id,)))
    elif len(User.objects.filter(employee_id=request.POST['requestor_employee_ids'],
                                 floorpass=ref_id)) > 0:
        request.session['message'] = 'Invalid Credentials, duplicate ID.'
        return HttpResponseRedirect(reverse('floorpass:manager', args=(ref_id,)), request)
    else:
        user.employee_id = request.POST['requestor_employee_ids']
        user.employee_name = str(
            '{}, {}'.format(emp_inf['message'][0]['last_name'], emp_inf['message'][0]['first_name']))
        user.floorpass.latest_log_date = timezone.now()
        user.floorpass.save()
        user.save()

        request.session['message'] = 'Invalid Credentials, duplicate ID.'
        return HttpResponseRedirect(reverse('floorpass:manager', args=(ref_id,)))


def generate_floorpass_id(request):
    if request.POST.get('requestor_department_id', '') == '' and request.POST.get('requestor_purpose', '') == '':
        request.session['message'] = 'Invalid Credentials, input purpose and department..'
        return HttpResponseRedirect(reverse('floorpass:manager'))
    else:
        floorpass = FloorPass()
        floorpass.department = get_object_or_404(Department, pk=request.POST['requestor_department_id'])
        floorpass.location = get_object_or_404(Location, pk=request.session['location_id'])
        floorpass.supervisor = request.session['admin_name']

        floorpass.purpose = request.POST['requestor_purpose']
        floorpass.status = 0

        floorpass.latest_log_date = timezone.now()
        floorpass.save()

        return HttpResponseRedirect(reverse('floorpass:manager', args=(floorpass.id,)))
