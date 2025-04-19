from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from Login.models import Userlogin
from Login.serializers import UserloginSerializer

# Create your views here.
@csrf_exempt
def userLoginAPI(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        if (user_data['username']):
            if not user_data['password']:
                return JsonResponse("Bạn cần điền đầy đủ thông tin đăng nhập!.", safe=False)
            if not user_data['usertype']:
                return JsonResponse("Bạn cần chọn vai trò đăng nhập!", safe=False)
            try:
                user = Userlogin.objects.get(username=user_data['username'])
                if user_data['usertype'] != user.usertype:
                    return JsonResponse("Bạn chọn sai vai trò!", safe=False)
                if check_password(user_data['password'], user.password):
                    return JsonResponse({"message": "Đăng nhập thành công!", "username": user.username}) #Dang nhap thanh cong
                else:
                    return JsonResponse("Mật khẩu không đúng!",safe=False) #Mat khau sai
            except Userlogin.DoesNotExist:
                return JsonResponse("Tài khoản không tồn tại!",safe=False) #Khong co nguoi dung
            
        if (user_data['useremail']):
            if not user_data['password']:
                return JsonResponse("Bạn cần điền đầy đủ thông tin đăng nhập!", safe=False)
            if not user_data['usertype']:
                return JsonResponse("Bạn cần chọn vai trò đăng nhập!", safe=False)
            try:
                user = Userlogin.objects.get(useremail=user_data['useremail'])
                if user_data['usertype'] != user.usertype:
                    return JsonResponse("Bạn chọn sai vai trò!", safe=False)
                if check_password(user_data['password'], user.password):
                    return JsonResponse({"message": "Đăng nhập thành công!", "username": user.username}) #Dang nhap thanh cong
                else:
                    return JsonResponse("Mật khẩu không đúng!",safe=False) #Mat khau sai
            except Userlogin.DoesNotExist:
                return JsonResponse("Tài khoản không tồn tại!",safe=False) #Khong co nguoi dung
        
        return JsonResponse("Bạn cần điền đầy đủ thông tin đăng nhập!", safe=False)
    # elif request.method == 'PUT': #Thay mat khau
    #     user_data = JSONParser().parse(request) #input: new password, confirm new password
    #     if (user_data['new_password'] == user_data['confirm']): # doan nay tu thay:v
            
@csrf_exempt
def userRegisterAPI(request): # thử chứ đừng dùng, bởi chỉ admin được tạo tài khoản
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            user = Userlogin.objects.get(username=user_data['username'])
            return JsonResponse("Tên tài khoản này đã tồn tại, vui lòng chọn tên khác.")
        except Userlogin.DoesNotExist:
            user_data_serializer = UserloginSerializer(data=user_data)
            if user_data_serializer.is_valid():
                user_data_serializer.save()
                return JsonResponse("Thêm tài khoản thành công!", safe=False)
            return JsonResponse("Hãy thử lại", safe=False)

@csrf_exempt
def forgotPassword(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            user_data_by_mail = Userlogin.objects.get(useremail=user_data['useremail'])
            # Generate a random token (e.g., for password reset)
            token = get_random_string(length=32)

            # You'd save this token somewhere (e.g., a reset_token field or a separate model)
            # For this example, just include it in the email
            reset_link = f"http://yourdomain.com/reset-password/{token}/" # Đây là cái trang của mình, bao giờ deploy thì dùng, tôi sẽ đổi resetlink thành rickroll:)
            reset_link = f"https://youtu.be/dQw4w9WgXcQ?si=QBse2atAbns4GNUZ"

            # Send reset email
            send_mail(
                subject='Password Reset Request',
                message=f"Hi {user_data_by_mail.username},\n\nClick the link below to reset your password:\n{reset_link}",
                from_email='vinhthanhtran03102004@gmail.com', # Sau này đây là email của mình: noreply@yourdomain.com
                recipient_list=[user_data_by_mail.useremail],
                fail_silently=False,
            )

            return JsonResponse("Email reset đã được gửi thành công!", safe=False)
        except Userlogin.DoesNotExist:
            return JsonResponse("Tài khoản không tồn tại!", safe=False)