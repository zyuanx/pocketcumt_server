from rest_framework import serializers


class BaseLoginSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        abstract = True


class BaseTermSerializer(BaseLoginSerializer):
    xnm = serializers.IntegerField()
    xqm = serializers.IntegerField()

    class Meta:
        abstract = True


class LoginSerializer(BaseLoginSerializer):
    class Meta:
        fields = '__all__'


class GradeSerializer(BaseTermSerializer):
    class Meta:
        fields = '__all__'


class GradeDetailSerializer(BaseTermSerializer):
    jxb_id = serializers.CharField()

    class Meta:
        fields = '__all__'


class ExamSerializer(BaseTermSerializer):
    class Meta:
        fields = '__all__'


class CourseSerializer(BaseTermSerializer):
    class Meta:
        fields = '__all__'


class TeacherTelSerializer(BaseTermSerializer):
    tea_name = serializers.CharField()

    class Meta:
        fields = '__all__'


class ClassroomSerializer(BaseTermSerializer):
    jcd = serializers.IntegerField()
    this_local = serializers.IntegerField()
    this_week = serializers.IntegerField()
    this_day = serializers.IntegerField()

    class Meta:
        fields = '__all__'
