import hashlib
import random
from django.db import models
from django_jsonform.models.fields import JSONField
from django.db.models import Q


class Department(models.Model):
    name = models.CharField(max_length=50, verbose_name="科室名称", unique=True)
    registration_fee = models.FloatField(verbose_name="挂号费", default=0)

    class Meta:
        verbose_name = '科室管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AbsUser:

    @staticmethod
    def make_password(password):
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()

    def verify(self, password1, password):
        return password1 == self.make_password(password)


def make_patient_random_number():
    rd = random.randint(100000, 999999)
    while Patient.objects.filter(medical_insurance_number=rd).exists():
        rd = random.randint(100000, 999999)
    return random.randint(100000, 999999)


def make_doctor_random_number():
    rd = random.randint(100000, 999999)
    while Doctor.objects.filter(job_number=rd).exists():
        rd = random.randint(100000, 999999)
    return random.randint(100000, 999999)


# patient model(username,id_card,phone,password,sex,age)
class Patient(models.Model, AbsUser):
    sex_choice = (
        (1, '男'),
        (2, '女')
    )
    # 患者医保号
    medical_insurance_number = models.CharField(max_length=6, verbose_name="医保号", unique=True,
                                                default=make_patient_random_number)
    username = models.CharField(max_length=50, verbose_name="患者用户名", unique=True)
    id_card = models.CharField(max_length=50, verbose_name="身份证号", unique=True)
    phone = models.CharField(max_length=11, verbose_name="手机号")
    password = models.CharField(max_length=250, verbose_name="密码",
                                help_text="存储的为密文，每次保存的时候密码会自动更新")
    sex = models.IntegerField(choices=sex_choice, default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")

    @classmethod
    def login(cls, username, password):
        user = cls.objects.filter(
            Q(phone=username) | Q(medical_insurance_number=username) | Q(id_card=username)).first()
        if user and user.verify(user.password, password):
            return user
        return None

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '患者管理'
        verbose_name_plural = verbose_name


# doctor model
class Doctor(models.Model, AbsUser):
    sex_choice = (
        (1, '男'),
        (2, '女')
    )
    # 工号
    job_number = models.CharField(max_length=6, verbose_name="工号", unique=True, default=make_doctor_random_number)
    username = models.CharField(max_length=50, verbose_name="医生用户名", unique=True)
    id_card = models.CharField(max_length=50, verbose_name="身份证号", unique=True)
    phone = models.CharField(max_length=11, verbose_name="手机号")
    password = models.CharField(max_length=250, verbose_name="密码",
                                help_text="存储的为密文，每次保存的时候密码会自动更新")
    sex = models.IntegerField(choices=sex_choice, default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="科室")
    limit = models.IntegerField(verbose_name="挂号限额", default=10)

    @classmethod
    def login(cls, username, password):
        user = cls.objects.filter(
            Q(phone=username) | Q(job_number=username) | Q(id_card=username)).first()
        if user and user.verify(user.password, password):
            return user
        return None

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
            "limit": self.limit,
        }

    def set_password(self, password):
        self.password = self.make_password(password)

    @classmethod
    def get_available_doctor(cls, departmentId):
        ret = cls.objects.all()
        if departmentId:
            ret = ret.filter(department_id=departmentId)
        return ret.filter(limit__gt=0)

    class Meta:
        verbose_name = '医生管理'
        verbose_name_plural = verbose_name


# medicine model(name,price,unit,stock)
class Medicine(models.Model):
    name = models.CharField(max_length=50, verbose_name="药品名称", unique=True)
    price = models.FloatField(verbose_name="药品价格")
    unit = models.CharField(max_length=10, verbose_name="药品单位")
    stock = models.IntegerField(verbose_name="药品库存")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "unit": self.unit,
            "stock": self.stock
        }

    class Meta:
        verbose_name = '药品管理'
        verbose_name_plural = verbose_name


class Order(models.Model):
    medicine_list_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "药品名称"
                },
                "unit": {
                    "type": "string",
                    "title": "药品单位"
                },
                "amount": {
                    "type": "integer",
                    "title": "药品数量"
                },
                "price": {
                    "type": "number",
                    "title": "药品价格"
                }
            }
        }
    }
    physical_examination_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "体检项目"
                },
                "number": {
                    "type": "number",
                    "title": "数值"
                },
                "index": {
                    "type": "string",
                    "title": "指标"
                },

            }
        }
    }
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="科室")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="患者")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="医生")
    patient_description = models.TextField(max_length=250, verbose_name="患者自述情况")
    readme = models.TextField(max_length=250, verbose_name="医嘱")
    medicine_list = JSONField(schema=medicine_list_schema, verbose_name="药品列表", null=True, blank=True)
    # 体检指标
    physical_examination = JSONField(schema=physical_examination_schema, verbose_name="体检指标", null=True, blank=True)
    total_cost = models.FloatField(verbose_name="总费用", default=0)
    status = models.BooleanField(verbose_name="诊断结束", default=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="预约时间")

    @classmethod
    def create_order(cls, patient, doctor, patient_description, registration_fee):
        if Order.objects.filter(department=doctor.department, patient=patient, status=False).exists():
            return False
        order = Order()
        order.patient = patient
        order.doctor = doctor
        order.department = doctor.department
        order.total_cost = registration_fee
        order.patient_description = patient_description
        order.save()
        doctor.limit -= 1
        doctor.save()
        return True

    @classmethod
    def finish_order(cls, orderId, medicine_list, readme, total_cost):
        order = Order.objects.get(id=int(orderId))
        order.medicine_list = medicine_list
        order.readme = readme
        order.total_cost += total_cost
        order.status = True
        order.save()
        for item in medicine_list:
            medicine = Medicine.objects.filter(name=item['name']).first()
            medicine.stock -= item['amount']
            medicine.save()
        order.doctor.limit += 1
        order.doctor.save()

    def serialize(self):
        return {
            'id': self.id,
            "registration_fee": self.doctor.department.registration_fee,
            "department": self.doctor.department.name,
            'patient': self.patient.username,
            'doctor': self.doctor.username,
            'patient_description': self.patient_description,
            'readme': self.readme,
            'medicine_list': self.medicine_list,
            'total_cost': self.total_cost,
            'status': self.status,
            'add_time': self.add_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    class Meta:
        verbose_name = '预约管理'
        verbose_name_plural = verbose_name
