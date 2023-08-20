from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from.decorators import unauthenticated_user,allowed_users
from django.core.mail import send_mail
from .models import User,Attendance,Device
from main.models import Category
from .forms import CreateUserForm,NewUserForm
from django.core import serializers


# @unauthenticated_user
def index(request):
    next_url = request.GET.get('next')  # Get the value of 'next' parameter from the query string

    context = {}
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)

            if next_url:
                return redirect(next_url)  # Redirect to the URL specified in 'next' parameter
            return redirect('main:home')
        else:
            messages.info(request, " Please Provide A Valid Username And Paassword")

    return render(request,'auth/login.html',context)
    # return render(request,'accounts/login.html',context)

def logoutView(request):
    logout(request)
    return redirect('users:login')
    

def registerView(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if Group.objects.filter(name="student").exists():
                group = Group.objects.filter(name="student").first()
            else:
                group = Group.objects.create(name="student")

            # user.is_active = False
            user.groups.add(group)
            user.user_type = "STUDENT"
            user.save()

            user_email = form.cleaned_data.get("email")
            messages.success(request,"Account Has Been Created For " + user_email)
            return redirect('users:login')
        
    context = {'form': form}

    return render(request,'auth/register.html',context)
    # return render(request,'accounts/register.html',context)

@login_required(login_url='users/login')
@allowed_users(allowed_roles=["admin",'staff'])
def users_list_view(request):
    categories = Category.objects.all()
    users = User.objects.all()
        
    context = {
        "categories":categories,
        "users":users
        }

    return render(request,'accounts/users_list.html',context)

@login_required(login_url='users/login')
def users_detail_view(request,pk):
    categories = Category.objects.all()
    user = User.objects.get(id=pk)
    attendances = Attendance.objects.filter(user= user)
        
    context = {
        "categories": categories,
        "user": user,
        "attendances": attendances
        }

    return render(request,'accounts/users_detail.html',context)

@login_required(login_url='login')
def users_delete_view(request,pk): 
    user = User.objects.get(id=pk)
    user.delete()
    return JsonResponse({"message": "Successful"})


@login_required(login_url='users/login')
@allowed_users(allowed_roles=["admin"])
def users_new_view(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if Group.objects.filter(name=user.user_type.lower()).exists():
                group = Group.objects.filter(name=user.user_type.lower()).first()
            else:
                group = Group.objects.create(name=user.user_type.lower())

            # user.is_active = False
            user.groups.add(group)
            user.set_password(str(user.email))
            user.save()

            user_email = form.cleaned_data.get("email")
            messages.success(request,"Account Has Been Created For " + user_email)
            return redirect('users:user_list')
        
    context = {'form': form}

    return render(request,'accounts/users_new.html',context)


@login_required(login_url='users/login')
@allowed_users(allowed_roles=["admin",'staff'])
def attendance_list_view(request):
    results = Attendance.objects.all()
        
    context = {"results":results}

    return render(request,'attendance/index.html',context)

@login_required(login_url='users/login')
@allowed_users(allowed_roles=["admin",'staff'])
def device_list_view(request):
    results = Device.objects.all()
        
    context = {"results":results}

    return render(request,'device/index.html',context)

def users_search(request):
    name = request.GET.get("name", None)
    # print(name)
    
    results = User.objects.filter(first_name__icontains=name)

    results_data = [{
        'id': result.id,
        'name': result.name,
        'email': result.email,
        'user_type': result.user_type,
        'is_active': result.is_active,
        'created_at': result.created_at,
        } for result in results]
        
    return JsonResponse({'results': results_data})

def attendance_search(request):
    device = request.GET.get("device", None)
    # print(device)
    
    results = Attendance.objects.all()

    results_data = [{
        'id': result.id,
        'user': {
            'id': result.user.id,
            'name': result.user.name,
            'email': result.user.email,
        },
        'attendance_type': result.attendance_type,
        'activity': result.activity,
        'created_at': result.created_at,
        } for result in results]
        
    return JsonResponse({'results': results_data})


# @login_required(login_url='login')
# def user_create_view(request):
#     categories = User.objects.all()
#     form = CategoryForm()

#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             category = form.cleaned_data['title']
#             messages.success(request, category + " Has Been Added ")
#             return redirect('main:category_list')
#         else:
#             messages.error(request,"Failed To Create Category")
        
#     context = {
#         "categories":categories,
#         'form': form
#         }

#     return render(request,'main/category_new.html',context)

def send_mail_now(request):
    send_mail(
                'Hello', 
                'Your Verification OTP Code For FraudIt is',
                'myiga@sailglobalcorp.com', #Sender
                ["yigamarkgabriel333@gmail.com"], #Recipients
                fail_silently=False
                )
    return redirect('login')
    


# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
# from rest_framework.views import APIView
# from rest_framework.generics import CreateAPIView
# from rest_framework.generics import ListAPIView
# from rest_framework.generics import RetrieveAPIView
# from rest_framework.generics import UpdateAPIView
# from rest_framework.generics import DestroyAPIView
# import qrcode
# import pyotp
# import base64
# from io import BytesIO
# from django.http import HttpResponse
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status
# from django.core.mail import send_mail,EmailMessage
# from library_app.utils import generate_otp
# from django.utils import timezone
# from .models import User
# # from .serializers import RegisterSocUserSerializer
# # from .serializers import RegisterSfiUserSerializer
# # from .serializers import RegisterSfiSerializer
# # from .serializers import SfiSerializer
# # from .serializers import UserSerializer


# class LoginTokenObtainView(TokenObtainPairView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.user
#         random_otp = generate_otp()
#         user.otp_code = random_otp
#         user.save()

#         tokens = serializer.validated_data

#         # Serialize the user object
#         user_serializer = UserSerializer(user)

#         # Create the response data
#         response_data = {
#             'tokens': tokens,
#             'user': user_serializer.data
#         }

#         return Response(response_data)


# class LoginTokenRefreshView(TokenRefreshView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data) # Reauest Data Have {refresh_token : ".."}

#         try:
#             serializer.is_valid(raise_exception=True)
#         except:
#             error_message = "Token is invalid or expired"
#             return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

#         # user = serializer.user TokenRefreshSerializer -> Has no attribute user
        
#         tokens = serializer.validated_data

#         # Create the response data
#         response_data = {
#             'tokens': tokens,
#         }

#         return Response(response_data)


# class BlackListTokenView(APIView):
#     # permission_classes = [AllowAny]

#     def post(self,request):
#         try:
#             refresh_token = request.data['refresh_token']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": e},status=status.HTTP_400_BAD_REQUEST)


# class GenerateOtpView(APIView):
#     authentication_classes = [JWTAuthentication]
#     parser_classes = [JSONParser]

#     def post(self, request):
#         user = request.user
        
#         if user is not None:
            
#             # Generate OTP QR code image
#             totp = pyotp.TOTP(user.otp_secret)
#             qr = qrcode.QRCode()
#             qr.add_data(totp.provisioning_uri(user.email, issuer_name='fraudIT'))
#             qr.make(fit=True)
#             qr_img = qr.make_image(fill='black', back_color='white')

#             buffered = BytesIO()
#             qr_img.save(buffered, format='PNG')
#             qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
#             return Response({'qr_code': qr_base64})
        
#             # Create a BytesIO object to store the image data
#             # img_io = BytesIO()
#             # qr_img.save(img_io, format='PNG')
#             # img_io.seek(0)
            
#             # Return success response with the QR code image
#             # return HttpResponse(img_io, content_type='image/png')
#         else:
#             return Response({'error': 'Invalid credentials'}, status=400)


# class VerifyOTPView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         user = request.user
#         otp = request.data.get('otp')

#         # print(otp)
        
#         # Verify OTP using the user's secret key
#         # totp = pyotp.TOTP(user.otp_secret)
#         # 
#         # if totp.verify(otp):
#         #     # Generate JWT token for successful authentication
#         #     # token = default_token_generator.make_token(user)
#         #     # Return JWT token
#         #     user.last_otp_verified = timezone.now()
#         #     user.is_otp_verified = True
#         #     user.save()
#         #     user_serializer = UserSerializer(user) 
#         #     return Response({'message': "User verified successfully", 'user': user_serializer.data})
#         # else:
#         #     return Response({'error': 'Invalid OTP'}, status=400)
#         #
#         if user.otp_code != otp:
#             return Response({"error":"Invalid Code"}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message":"Code Verified Successfully"}, status=status.HTTP_200_OK);

# ####### User ####### 
# class RegisterSocUserCreateAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSocUserSerializer

# class EditSocUserUpdateAPIView(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSocUserSerializer

# class RegisterSfiUserCreateAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSfiUserSerializer

# class EditSfiUserUpdateAPIView(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSfiUserSerializer

# class UserListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserRetrieveAPIView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDestroyAPIView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# ####### Sfi #######
# class RegisterSfiCreateAPIView(CreateAPIView):
#     queryset = Sfi.objects.all()
#     serializer_class = RegisterSfiSerializer

# class EditSfiUpdateAPIView(UpdateAPIView):
#     queryset = Sfi.objects.all()
#     serializer_class = RegisterSfiSerializer

# class SfiListAPIView(ListAPIView):
#     queryset = Sfi.objects.all()
#     serializer_class = SfiSerializer

# class SfiRetrieveAPIView(RetrieveAPIView):
#     queryset = Sfi.objects.all()
#     serializer_class = SfiSerializer

# class SfiDestroyAPIView(DestroyAPIView):
#     queryset = Sfi.objects.all()
#     serializer_class = SfiSerializer


# class SendOtpEmailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     parser_classes = [JSONParser]

#     def post(self, request):
#         user = request.user
#         # print(user)
        
#         otp_code = user.otp_code
        
#         email = user.email
        
#         user_data = request.data;

#         if not user_data:
#             return Response({"error":"Missing Email , Generation code"}, status=status.HTTP_400_BAD_REQUEST)

#         if user.email != user_data["user"]["email"]:
#             return Response({"error":"Invalid Request, Mismatched credentials"}, status=status.HTTP_400_BAD_REQUEST)

#         if otp_code is None:
#             return Response({"status": "Sending Email Failed, Please Login Again!"},status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             send_mail(
#                 'Hello', 
#                 'Your Verification OTP Code For FraudIt is : ' + otp_code,
#                 'tech@sailglobalcorp.com', #Sender
#                 [email], #Recipients
#                 fail_silently=False
#                 )
#             return Response({"status" : "Email Sent Successfully!"})
#         except:
#             return Response({"error": "Sending Email Failed!"},status=status.HTTP_400_BAD_REQUEST)



# # def sendingEmail1(request):
# #     try:
# #         if request.method == 'GET':
# #             print("Her")
# #             send_mail(
# #             'Hello', 
# #             'This is a test email',
# #             'tech@sailglobalcorp.com', #Sender
# #             ['yigamarkgabriel333@gmail.com'], #Recipients
# #             # fail_silently=False,
# #             )
# #         return HttpResponse("Sent 1!!!")
# #     except Exception as e:
# #         print("ERROr")
# #         print(e)
# #         return HttpResponse("Not Sent 1!!!")


# # def sendingEmail2(request):
# #     if request.method == 'GET':
# #         mail = EmailMessage(
# #             'Hello',
# #             'Body goes here 222',
# #             'settings.EMAIL_HOST_USER', #Sender
# #             ['yigamarkgabriel333@gmail.com'], #Recipients
# #             # ['bcc@example.com'], #BCC
# #             reply_to=['another@example.com'],
# #             headers={'Message-ID': 'foo'},
# #         )
# #         mail.send()
# #     return HttpResponse("Sent 2!!!")


# # class AuthView(APIView):
# #     authentication_classes = [JWTAuthentication]
# #     parser_classes = [JSONParser]

# #     def get(self, request):
# #         # username = request.data.get('username')
# #         # password = request.data.get('password')
# #         # user = authenticate(username=username, password=password)
        
# #         # if user is not None:
# #             # Generate and store the user's OTP secret key securely
# #         totp_secret_key = pyotp.random_base32()
        
# #         # Generate OTP QR code image
# #         totp = pyotp.TOTP(totp_secret_key)
# #         qr = qrcode.QRCode()
# #         qr.add_data(totp.provisioning_uri("mariko", issuer_name='fraudIt'))
# #         qr.make(fit=True)
# #         qr_img = qr.make_image(fill='black', back_color='white')
        
# #         # Create a BytesIO object to store the image data
# #         # img_io = BytesIO()
# #         # qr_img.save(img_io, format='PNG')
# #         # img_io.seek(0)
        
# #         # Return success response with the QR code image
# #         # return HttpResponse(img_io, content_type='image/png')

# #         # Convert the image to a Base64 string
# #         buffered = BytesIO()
# #         qr_img.save(buffered, format='PNG')
# #         qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
# #         return Response({'q
