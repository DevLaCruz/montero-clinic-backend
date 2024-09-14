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
from django.contrib.auth import get_user_model
User = get_user_model()

def response(data=None, detail=None, status_code=status.HTTP_200_OK):
    if detail:
        return Response({'detail': detail}, status=status_code)
    return Response(data, status=status_code)

# EVIAR GMAIL PARA RESTABLECER (COMPLETE)
class PasswordResetRequestAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return response(detail='Email requerido', status_code=status.HTTP_400_BAD_REQUEST)

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
            return response(data={'message': 'Revise su correo para el restablecimiento de contraseña'}, status_code=status.HTTP_200_OK)

        return response(detail='El correo no se encuentra registrado (Verifique su correo)', status_code=status.HTTP_400_BAD_REQUEST)

# RESTABLECER PASSWORD (COMPLETE)
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
            return response(data={'message': 'Contraseña actualizada'}, status_code=status.HTTP_200_OK)
        else:
            return response(detail='Token o ID de usuario no válido', status_code=status.HTTP_401_UNAUTHORIZED)

#REGISTRO DE CUENTA PARA PACIENTE-CLIENTE ()
class UserPatientRegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    
    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        #Registro de paciente
        request.data['user'] = user.id
        patient_serializer = ClientPatientSerializer(data=request.data)
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
            'user': {
                'id': patient.id,
                'name': patient.first_name,
                'email': user.email,
                'is_worker': user.is_worker,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)
        #response.set_cookie(key='access_token', value=data['access'], httponly=True, secure=True)
        #return response

#LOGIN (COMPLETE)
class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = authenticate(username=request.data.get('email'), password=request.data.get('password'))
        
        # VALIDACIONES
        if not user_instance:
            return response(detail='Credenciales inválidas', status_code=status.HTTP_403_FORBIDDEN)
        if not user_instance.is_active:
            return response(detail='Usuario inactivo', status_code=status.HTTP_403_FORBIDDEN)
        
        if request.data.get('type') == 'P' and not user_instance.is_worker:
            return response(detail='Acceso denegado, no es parte del personal', status_code=status.HTTP_403_FORBIDDEN)
        elif request.data.get('type') == 'C' and user_instance.is_worker:
            return response(detail='Acceso denegado, no es parte del cliente', status_code=status.HTTP_403_FORBIDDEN)
        
        if user_instance.is_worker:
            name = user_instance.employee.first_name
            id = user_instance.employee.id
        elif not user_instance.is_worker:
            name = user_instance.patient.first_name
            id = user_instance.patient.id
        
        refresh = RefreshToken.for_user(user_instance)
        response_data = {
            'user': {
                'id': id,
                'name': name,
                'email': user_instance.email,
                'is_worker': user_instance.is_worker,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response(data=response_data)
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
        if not user.is_worker:
            patient = user.patient
            person = PatientSerializer(patient).data
        else:
            employee = user.employee
            person = EmployeeSerializer(employee).data
        
        response_data = {
            'person': person,
            'user': UserSerializer(user).data,
        }
        return response(data=response_data)

# CERRAR SESION ( - REVOQUE TOKEN REFRESH)
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

# NUEVA CONTRASEÑA (COMPLETE)
class ChangePasswordView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        # Dejamos que DRF maneje las validaciones automáticamente
        serializer.is_valid(raise_exception=True)
        
        # Si es válido, actualizamos la contraseña
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)