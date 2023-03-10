from django.urls import path
from .views import LoginView, PatientIndexView, PatientHistoryView, DoctorHistoryView, DoctorIndexView, RegisterView, \
    DepartmentAPIView, DoctorAPIView, OrderAPIView,LogoutView,MedicineAPIView

app_urls = [
    path("", LoginView.as_view(), name="login"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("patient/", PatientIndexView.as_view(), name="patientIndex"),
    path("patient/history/", PatientHistoryView.as_view(), name="patientHistory"),
    path("doctor/", DoctorIndexView.as_view(), name="doctorIndex"),
    path("doctor/history/", DoctorHistoryView.as_view(), name="doctorHistory"),
    path("api/department/", DepartmentAPIView.as_view(), name="department"),
    path("api/doctor/", DoctorAPIView.as_view(), name="doctor"),
    path("api/order/", OrderAPIView.as_view(), name="order"),
    path("api/medicine/", MedicineAPIView.as_view(), name="medicine"),
]
