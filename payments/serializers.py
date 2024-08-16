from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'status':{'required': False},
        }
    def create(self, validated_data):
        # Eliminar 'status'
        validated_data.pop('status', None)
        return super().create(validated_data)