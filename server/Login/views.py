from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from Login.models import Userlogin
from Login.serializers import UserloginSerializer

from DBApp.models import Student
from DBApp.serializers import TeacherSerializer, StudentSerializer, ParentSerializer, StudentparentSerializer

import server.settings as settings

# Create your views here.
@csrf_exempt
def userLoginAPI(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        if (not user_data['useremail'] or not user_data['password']):
            return JsonResponse("Bạn cần điền đầy đủ thông tin đăng nhập!.", safe=False)
        try:
            user = Userlogin.objects.get(useremail=user_data['useremail'])
            if check_password(user_data['password'], user.password):
                return JsonResponse({"message": "Đăng nhập thành công!", "username": user.username, "usertype": user.usertype}) #Dang nhap thanh cong
            else:
                return JsonResponse("Mật khẩu không đúng!",safe=False) #Mat khau sai
        except Userlogin.DoesNotExist:
            return JsonResponse("Tài khoản không tồn tại!",safe=False) #Khong co nguoi dung
    # elif request.method == 'PUT': #Thay mat khau
    #     user_data = JSONParser().parse(request) #input: new password, confirm new password
    #     if (user_data['new_password'] == user_data['confirm']): # doan nay tu thay:v


@csrf_exempt
def userRegisterAPI(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        username = user_data.get('username')
        useremail = user_data.get('useremail')
        usertype = user_data.get('usertype')

        if Userlogin.objects.filter(username=username).exists() or Userlogin.objects.filter(useremail=useremail).exists():
            return JsonResponse("Tên tài khoản này/Email này đã tồn tại, vui lòng chọn tên/email khác.", safe=False)

        related_id = None

        # Create related object depending on usertype
        if usertype == 'Teacher':
            teacher_data = {
                'teacher_name': user_data.get('teacher_name'),
                'teacher_gender': user_data.get('teacher_gender'),
                'teacher_email': user_data.get('teacher_email'),
                'teacher_profession': user_data.get('teacher_profession'),
            }
            teacher_serializer = TeacherSerializer(data=teacher_data)
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save()
                related_id = teacher.teacher_id
            else:
                return JsonResponse(teacher_serializer.errors, safe=False)

        elif usertype == 'Student':
            student_data = {
                'student_name' : user_data.get('student_name'),
                'student_dob' : user_data.get('student_dob'),
                'student_gender' : user_data.get('student_gender'),
                'student_email' : user_data.get('student_email'),
                'student_graduating_class' : user_data.get('student_graduating_class'),
                'student_phone_number' : user_data.get('student_phone_number'),
                'student_specialization' : user_data.get('student_specialization'),
                'student_is_active' : user_data.get('student_is_active'),
                'student_school' : user_data.get('student_school')
            }
            student_serializer = StudentSerializer(data=student_data)
            if student_serializer.is_valid():
                student = student_serializer.save()
                related_id = student.student_id
            else:
                return JsonResponse(student_serializer.errors, safe=False)

        elif usertype == 'Parent':
            parent_data = {
                'parent_name' : user_data.get('parent_name'),
                'parent_gender' : user_data.get('parent_gender'),
                'parent_email' : user_data.get('parent_email'),
                'parent_phone_number' : user_data.get('parent_phone_number'),
                'parent_occupation' : user_data.get('parent_occupation')
            }

            check_student_data = {
                'student' : user_data.get('student_id'),
                'relationship_to_student' : user_data.get('relationship_to_student')
            }
            try:
                student_check = Student.objects.get(student_id=check_student_data['student'])
                parent_serializer = ParentSerializer(data=parent_data)
                if parent_serializer.is_valid():
                    parent = parent_serializer.save()
                    related_id = parent.parent_id
                    check_student_data['parent'] = related_id
                    connect = StudentparentSerializer(data=check_student_data)
                    if connect.is_valid():
                        connect.save()
                    else:
                        return JsonResponse("Unknown error happen!", safe=False)
                else:
                    return JsonResponse(parent_serializer.errors, safe=False)
            except Student.DoesNotExist:
                    return JsonResponse("Không thể tạo tài khoản phụ huynh không có sinh viên trong hệ thống!", safe=False)
        else:
            return JsonResponse("Loại người dùng không hợp lệ.", safe=False)

        # Continue with creating Userlogin
        user_data['relatedid'] = related_id
        user_serializer = UserloginSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Thêm tài khoản thành công!", safe=False)
        return JsonResponse(user_serializer.errors, safe=False)

@csrf_exempt
def forgotPassword(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            user_data_by_mail = Userlogin.objects.get(useremail=user_data['useremail'])
            token = get_random_string(length=32)
            reset_link = f"https://yourdomain.com/reset-password?token={token}"  # Replace with your actual reset page

            html_content = render_to_string("login.html", {
                'username': user_data_by_mail.username,
                'reset_link': reset_link,
            })

            subject = 'Đặt lại mật khẩu'
            from_email = settings.EMAIL_HOST_USER
            to = user_data_by_mail.useremail

            email = EmailMultiAlternatives(subject, "", from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return JsonResponse("Email reset đã được gửi thành công!", safe=False)
        except Userlogin.DoesNotExist:
            return JsonResponse("Tài khoản không tồn tại!", safe=False)