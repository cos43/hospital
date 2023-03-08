from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from .models import Patient, Doctor, Department, Order, Medicine
from django.contrib import auth
import json


# 检测用户是否登录，如果登录返回用户对象，否则返回None
def check_login(request, permit_role=None):
    # 从session中获取用户id
    if permit_role is None:
        permit_role = ["patient", "doctor"]
    if 'role' not in request.session:
        return False
    role = request.session['role']
    userId = request.session['userId']
    if not userId or role not in permit_role:
        return False
    if role == 'patient':
        return Patient.objects.get(id=int(userId))
    else:
        return Doctor.objects.get(id=int(userId))


class RegisterView(View):
    def post(self, request):
        user = Patient()
        username = request.POST.get('username')
        id_card = request.POST.get('id_card')
        phone = request.POST.get('phone')
        password = user.make_password(request.POST.get('password'))
        sex = request.POST.get("sex")
        age = request.POST.get('age')
        if Patient.objects.filter(id_card=id_card).first():
            return JsonResponse({'code': 1, 'msg': '身份证号已存在'})
        if Patient.objects.filter(phone=phone).first():
            return JsonResponse({'code': 1, 'msg': '手机号已存在'})
        user.username = username
        user.id_card = id_card
        user.phone = phone
        user.password = password
        user.sex = sex
        user.age = age
        user.save()
        return JsonResponse({'code': 0, 'msg': '注册成功'})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if role == "patient":
            user = Patient.login(username, password)
            if user:
                request.session['medical_insurance_number'] = user.medical_insurance_number
        elif role == "doctor":
            user = Doctor.login(username, password)
            if user:
                request.session['department'] = user.department.name
                request.session['job_number'] = user.job_number
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
        if user:
            # add user to session
            request.session['username'] = user.username
            request.session['role'] = role
            request.session['userId'] = user.id
            return JsonResponse({'code': 0, 'msg': '登录成功'})
        else:
            return JsonResponse({'code': 1, 'msg': '用户名或密码错误'})


class PatientIndexView(View):
    def get(self, request):
        user = check_login(request, ['patient'])
        if not user:
            return HttpResponseRedirect('/login/')
        return render(request, 'patient/index.html', context={'title': '就诊大厅', "user": user})

    def post(self, request):
        """处理病人挂号"""
        user = check_login(request, ['patient'])
        patient_description = request.POST.get('patient_description')
        department = Department.objects.get(id=int(request.POST.get('department')))
        registration_fee = department.registration_fee
        doctor = Doctor.objects.get(id=int(request.POST.get('doctor')))
        ret = Order.create_order(user, doctor, patient_description, registration_fee)
        code, msg = 0, "挂号成功"
        if not ret:
            code, msg = 1, "您已经预约了该科室的医生，不能重复预约"
        return JsonResponse({'code': code, 'msg': msg})


class PatientHistoryView(View):
    def get(self, request):
        user = check_login(request, ['patient'])
        if not user:
            return HttpResponseRedirect('/login/')
        return render(request, 'patient/history.html', context={'title': '就诊记录', "user": user})


class DoctorIndexView(View):
    def get(self, request):
        user = check_login(request, ['doctor'])
        if not user:
            return HttpResponseRedirect('/login/')
        return render(request, 'doctor/index.html', context={'title': '接诊房间', "user": user})

    def post(self, request):
        data = json.loads(request.body)
        orderId = data['orderId']
        medicine_list = data['medicine_list']
        total_cost = data['total_cost']
        readme = data['readme']
        Order.finish_order(orderId, medicine_list, readme, total_cost)
        return JsonResponse({'code': 0, 'msg': '接诊成功'})


class DoctorHistoryView(View):
    def get(self, request):
        user = check_login(request, ['doctor'])
        if not user:
            return HttpResponseRedirect('/login/')
        return render(request, 'doctor/history.html', context={'title': '接诊记录', "user": user})

    def post(self, request):
        pass


class DepartmentAPIView(View):
    def get(self, request):
        data = [{"id": dept.id, "name": dept.name, "registration_fee": dept.registration_fee} for dept in
                Department.objects.all()]
        return JsonResponse({'code': 0, 'msg': '获取成功', 'data': data})


class OrderAPIView(View):
    def get(self, request):
        user = check_login(request)
        if not user:
            return HttpResponseRedirect('/login/')
        condition = {}
        role = request.session['role']
        if role == "patient":
            condition['patient'] = user
        else:
            condition['doctor'] = user
        status = request.GET.get('status', None)
        if status:
            condition['status'] = status == '1'
        order_list = [order.serialize() for order in Order.objects.filter(**condition)]
        return JsonResponse({'code': 0, 'msg': '获取成功', 'data': order_list})


class DoctorAPIView(View):
    def get(self, request):
        deptId = request.GET.get('deptId', None)
        doc_list = [doctor.serialize() for doctor in Doctor.get_available_doctor(deptId)]
        return JsonResponse({'code': 0, 'msg': '获取成功', 'data': doc_list})


class MedicineAPIView(View):
    def get(self, request):
        medicine_list = [medicine.serialize() for medicine in Medicine.objects.filter(stock__gt=0)]
        return JsonResponse({'code': 0, 'msg': '获取成功', 'data': medicine_list})


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect('/login/')
