from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, ChangePasswordSerializer
from patients.serializers import ClientPatientSerializer, PatientSerializer
from employees.serializers import EmployeeSerializer
from medical_records.serializers import MedicalRecordSerializer

# EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm

# Respuesta
def create_response(success, message, data=None, errors=None, status_code=status.HTTP_200_OK):
    return Response({
        'success': success,
        'message': message,
        'data': data,
        'errors': errors,
    }, status=status_code)

# RESET PASSWOR EMAIL (COMPLETE)
class PasswordResetRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return create_response(False, 'Email requerido', status_code=status.HTTP_400_BAD_REQUEST)

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

        return create_response(True, 'Si existe una cuenta con ese correo, recibirá un correo con instrucciones.')

# CONFIRM PASSWORD (COMPLETE)
class PasswordResetConfirmAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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
            return create_response(True, 'La contraseña se ha restablecido correctamente', status_code=status.HTTP_200_OK)
        else:
            return create_response(False, 'Token o ID de usuario no válido', status_code=status.HTTP_400_BAD_REQUEST)

#REGISTRO DE CUENTA PARA PACIENTE-CLIENTE (COMPLETE)
class UserPatientRegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    
    @transaction.atomic
    def post(self, request):
        #Registro de usuario
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        #Registro de paciente
        patient_data = request.data.get('patient')
        patient_data['user'] = user.id
        patient_serializer = ClientPatientSerializer(data=patient_data)
        patient_serializer.is_valid(raise_exception=True)
        patient = patient_serializer.save()
        
        # Registro de Historia clinica
        medical_record_data = {'patient': patient.id}
        medical_history_serializer = MedicalRecordSerializer(data=medical_record_data)
        medical_history_serializer.is_valid(raise_exception=True)
        medical_history_serializer.save()
        
        # Tokens de acceso
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response = create_response(True, 'Usuario registrado exitosamente', data=data, status_code=status.HTTP_201_CREATED)
        response.set_cookie(key='access_token', value=data['access'], httponly=True, secure=True)
        return response

#LOGIN (COMPLETE)
class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        # VALIDACIONES
        if not user_instance:
            return create_response(False, 'Credenciales inválidas', status_code=status.HTTP_403_FORBIDDEN)
        if not user_instance.is_active:
            return create_response(False, 'Usuario inactivo', status_code=status.HTTP_403_FORBIDDEN)
        
        if request.data.get('type') == 'P' and not user_instance.is_staff:
            return create_response(False, 'Acceso denegado, no es parte del personal', status_code=status.HTTP_403_FORBIDDEN)
        elif request.data.get('type') == 'C' and user_instance.is_staff:
            return create_response(False, 'Acceso denegado, no es parte del cliente', status_code=status.HTTP_403_FORBIDDEN)
        
        if user_instance.is_staff:
            name = user_instance.employee.first_name
            id = user_instance.employee.id
        elif not user_instance.is_staff:
            name = user_instance.patient.first_name
            id = user_instance.patient.id
        
        refresh = RefreshToken.for_user(user_instance)
        response_data = {
            'id': id,
            'name': name,
            'user': UserSerializer(user_instance).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return create_response(True, 'Bienvenido', data=response_data)
        '''response.set_cookie(
            key='access_token', 
            value=str(refresh.access_token), 
            httponly=True, 
            secure=True, 
            samesite='Lax',
            domain='localhost'
        )'''

#PERFIL (COMPLETE)
class UserViewAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        if not user.is_staff:
            patient = user.patient
            person = PatientSerializer(patient).data
        else:
            employee = user.employee
            person = EmployeeSerializer(employee).data
        
        response_data = {
            'person': person,
            'user': UserSerializer(user).data,
        }
        return create_response(True, 'Perfil', data=response_data)

# CERRAR SESION (COMPLETE - REVOQUE TOKEN REFRESH)
class UserLogoutViewAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Obtener el token de refresco del usuario
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return create_response(False, 'Se requiere token de actualización.', status_code=status.HTTP_400_BAD_REQUEST)

            # Invalidar el token de refresco
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Eliminacion de cookie
            response = create_response(True, 'Se ha cerrado sesión correctamente.', status_code=status.HTTP_200_OK)
            response.delete_cookie('access_token')

            return response

        except Exception as e:
            return create_response(False, str(e), status_code=status.HTTP_400_BAD_REQUEST)

# RESTABLECER CONTRASEÑA (COMPLETE)
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Check old password
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return create_response(False, 'Contraseña anterior incorrecta.', status_code=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return create_response(True, 'Contraseña actualizada exitosamente', status_code=status.HTTP_200_OK)
        
        return create_response(False, 'Error al actualizar la contraseña', errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)