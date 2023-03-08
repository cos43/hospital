import random
from app.models import Medicine, Department, Doctor

hospital_departments = ['急诊科', '内科', '外科', '儿科', '妇产科', '眼科', '耳鼻喉科', '口腔科', '皮肤科', '康复科']
surnames = ['张', '王', '李', '赵', '陈', '刘', '周', '黄', '吴', '许']
names = ['明', '红', '华', '建', '子', '文', '博', '艳', '志', '鑫']


def get_name():
    surname = random.choice(surnames)
    name = random.choice(names)
    full_name = surname + name
    while Doctor.objects.filter(username=full_name).exists():
        surname = random.choice(surnames)
        name = random.choice(names)
        full_name = surname + name
    return full_name


medicine_list = [
    {'name': '阿司匹林', 'price': 9.99},
    {'name': '对乙酰氨基酚', 'price': 7.99},
    {'name': '布洛芬', 'price': 12.50},
    {'name': '氨酚烷胺', 'price': 8.80},
    {'name': '头孢克洛', 'price': 28.90},
    {'name': '罗红霉素', 'price': 15.60},
    {'name': '克拉霉素', 'price': 20.30},
    {'name': '阿奇霉素', 'price': 34.50},
    {'name': '酚麻美敏', 'price': 18.20},
    {'name': '替硝唑', 'price': 10.70},
    {'name': '左氧氟沙星', 'price': 36.80},
    {'name': '注射用头孢曲松钠', 'price': 65.90},
    {'name': '注射用氨苄西林钠', 'price': 28.60},
    {'name': '诺氟沙星', 'price': 22.40},
    {'name': '乳酸菌素片', 'price': 9.90},
    {'name': '硫酸氢氯吡格雷', 'price': 23.50},
    {'name': '普萘洛尔', 'price': 13.80},
    {'name': '硝酸甘油', 'price': 7.20},
    {'name': '厄贝沙坦', 'price': 26.70},
    {'name': '氯吡格雷', 'price': 16.90},
    {'name': '依托利定', 'price': 29.80},
    {'name': '拉莫三嗪', 'price': 11.50},
    {'name': '阿莫西林', 'price': 16.20},
    {'name': '曲安奈德', 'price': 21.00},
    {'name': '盐酸左西替利嗪片', 'price': 32.40},
    {'name': '注射用甲磺酸氨卡西平', 'price': 49.60},
    {'name': '蒙脱石散', 'price': 6.60},
    {'name': '阿替洛尔', 'price': 14.90},
    {'name': '氯丙嗪', 'price': 8.30},
    {'name': '非那雄胺', 'price': 38.70}
]


# 随机生成Medicine
def generate_medicine():
    for m in medicine_list:
        medicine = Medicine()
        medicine.name = m['name']
        medicine.price = m['price']
        medicine.unit = "瓶"
        medicine.stock = random.randint(1, 20)
        medicine.save()


def generate_department():
    for d in hospital_departments:
        department = Department()
        department.name = d
        department.registration_fee = random.randint(10, 100)
        department.save()
        generate_doctor(department)


def generate_doctor(department):
    for i in range(2):
        doctor = Doctor()
        doctor.username = get_name()
        doctor.department = department
        doctor.sex = random.choice([1, 2])
        doctor.phone = f'1{random.randint(100000000, 999999999)}'
        doctor.age = random.randint(20, 60)
        doctor.limit = random.randint(10, 100)
        doctor.set_password('123456')
        random5 = random.randint(10000, 99999)
        doctor.id_card = f'123456{random5}2345678'
        doctor.save()


def generate_data():
    Medicine.objects.all().delete()
    Department.objects.all().delete()
    Doctor.objects.all().delete()
    generate_medicine()
    generate_department()
