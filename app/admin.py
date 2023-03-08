from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = '医疗数据管理后台'  # 设置header
admin.site.site_title = '医疗数据管理后台'  # 设置title
admin.site.index_title = '医疗数据管理后台'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_fee']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['username', 'medical_insurance_number', 'phone', 'sex', 'age']

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data and len(obj.password) < 32:
            obj.password = obj.make_password(obj.password)
        obj.save()


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_filter = ['department']
    list_display = ['username', 'job_number', 'department', 'phone', 'sex', 'age', 'limit']

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data and len(obj.password) < 32:
            obj.password = obj.make_password(obj.password)
        obj.save()


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'unit', 'stock']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    search_fields = ['patient__username', 'doctor__username']
    list_display = ['patient', 'doctor', 'status', 'add_time']
