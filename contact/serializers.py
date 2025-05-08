from rest_framework import serializers

class ContactUsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    # subject = serializers.CharField(max_length=150)
    message = serializers.CharField()