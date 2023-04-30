from rest_framework import serializers

from choco_life.models import Event, Company, EventCategory, Certificate, UserCertificate


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class UserCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertificate
        fields = '__all__'


class CertificateBuySerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    certificate = serializers.PrimaryKeyRelatedField(
        queryset=Certificate.objects.all()
    )

    def create(self, validated_data):
        user_certificate = UserCertificate.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        user_certificate.save()
        return user_certificate
