from rest_framework import serializers
from django.contrib.auth.models import User
from patients.models import Patient, Company, Location 
from medical_records.models import MedicalRecord
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

class UserAndPatientRegistrationSerializer(serializers.Serializer):
    dni = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()
    address = serializers.CharField()
    phone = serializers.CharField()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False)
    language = serializers.CharField()
    occupation = serializers.CharField()
    religion = serializers.CharField()
    education_level = serializers.CharField()
    area = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    emergency_phone = serializers.CharField(required=False)
    relationship = serializers.CharField(required=False)
    id_tutor = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("El correo electrónico ya está registrado.")
        
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            
            patient = Patient.objects.create(
                id_user=user,
                dni=validated_data['dni'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                birth_date=validated_data['birth_date'],
                address=validated_data['address'],
                phone=validated_data['phone'],
                area=validated_data['area'],
                id_company=validated_data.get('company'),
                id_location=validated_data.get('location'),
                language=validated_data['language'],
                education_level=validated_data['education_level'],
                occupation=validated_data['occupation'],
                religion=validated_data['religion'],
                email=validated_data['email']
            )
            
            last_record = MedicalRecord.objects.order_by('number').last()
            if not last_record:
                new_number = '000001'
            else:
                last_number = int(last_record.number)
                new_number = '{:06d}'.format(last_number + 1)

            MedicalRecord.objects.create(
                patient=patient,
                number=new_number
            )
            
            return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_staff']
    
    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
 
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña anterior no es correcta")
        return value