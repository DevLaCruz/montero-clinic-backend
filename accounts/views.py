from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserAndPatientRegistrationSerializer, ChangePasswordSerializer
from patients.serializers import PatientSerializer

# EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetRequestAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Gmail requerido'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
            mail_subject = 'Restablecer su contraseña'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(mail_subject, message, 'joseleo042001@gmail.com', [email])

        return Response({'message': 'Si existe una cuenta con ese correo, recibirá un correo con instrucciones.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'La contraseña se ha restablecido correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token o ID de usuario no válido'}, status=status.HTTP_400_BAD_REQUEST)

"""class PasswordResetConfirmAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            return render(request, 'password_reset_confirm.html', {'uid': uid, 'token': token})
        else:
            return render(request, 'password_reset_invalid.html')
    
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
            else:
                return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            return render(request, 'password_reset_invalid.html')"""

class CustomerRegistrationAPIView(APIView):
    serializer_class = UserAndPatientRegistrationSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Bienvenido!'}
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                refresh = RefreshToken.for_user(new_user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=data['access'], httponly=True, secure=True)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return Response({'message': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            data = {'message': 'Usuario registrado exitosamente'}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#LOGIN
class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        user_name = request.data.get('username', None)
        user_password = request.data.get('password', None)
        user_type = request.data.get('user_type', None)
        if not user_name or not user_password or not user_type:
            return Response({'error': 'Faltan campos obligatorios'}, status=400)
        
        user_instance = authenticate(username=user_name, password=user_password)
        
        if not user_instance:
            return Response({'error': 'Credenciales inválidas'}, status=403)

        if not user_instance.is_active:
            return Response({'error': 'Usuario inactivo'}, status=403)

        if user_type == 'P' and not user_instance.is_staff:
            return Response({'error': 'Acceso denegado, no es parte del personal'}, status=403)
        elif user_type == 'C' and user_instance.is_staff:
            #worker = user_instance.worker
            ##person = WorkerSerializer(worker).data
            return Response({'error': 'Acceso denegado, no es parte del cliente'}, status=403)

        if not user_instance.is_staff:
            patient = user_instance.patient
            person = PatientSerializer(patient).data
        else:
            #worker = user_instance.worker
            person = None
            
        refresh = RefreshToken.for_user(user_instance)
        response = Response({
            'succes': 'Bienvenido',
            'person': person,
            'user': UserLoginSerializer(user_instance).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)
        response.set_cookie(
            key='access_token', 
            value=str(refresh.access_token), 
            httponly=True, 
            secure=True, 
            samesite='Lax'
        )
        return response


class UserViewAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        if not user.is_staff:
            patient = user.patient
            person = PatientSerializer(patient).data
        else:
            #worker = user_instance.worker
            person = None
        return Response({
            'succes': 'Profile',
            'person': person,
            'user': UserLoginSerializer(user).data,
        }, status=200)


class UserLogoutViewAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.data = {'message': 'Cerró sesión exitosamente.'}
        return response
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Check old password
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return Response({'old_password': 'Contraseña incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Contraseña actualizada exitosamente'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)