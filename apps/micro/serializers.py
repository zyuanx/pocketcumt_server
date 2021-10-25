from rest_framework import serializers


class DormSerializer(serializers.Serializer, ):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    row = serializers.IntegerField()
    column = serializers.IntegerField()
    dorm = serializers.CharField()

    class Meta:
        fields = ['row', 'column', 'dorm']
