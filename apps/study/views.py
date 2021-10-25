from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.study.serializers import *
from apps.study.tshzs import Study
from utils.auth import Authentication


class LoginViewSet(mixins.CreateModelMixin,
                   GenericViewSet):
    serializer_class = LoginSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        re = login.ty_login()
        if re['code'] == 10000:
            res = login.get_info()
            return JsonResponse(res)
        else:
            return JsonResponse(re)


class CourseViewSet(mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = CourseSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_course_list()
        return JsonResponse(res)


class GradeViewSet(mixins.CreateModelMixin,
                   GenericViewSet):
    serializer_class = GradeSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_grade()
        return JsonResponse(res)


class GradeDetailViewSet(mixins.CreateModelMixin,
                         GenericViewSet):
    serializer_class = GradeDetailSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_detail_grade()
        return JsonResponse(res)


class ExamViewSet(mixins.CreateModelMixin,
                  GenericViewSet):
    serializer_class = ExamSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_exam()
        return JsonResponse(res)


class TeaTelViewSet(mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = TeacherTelSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_teacher_tel()
        return JsonResponse(res)


class ClassroomViewSet(mixins.CreateModelMixin,
                       GenericViewSet):
    serializer_class = ClassroomSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        params_data = request.data
        login = Study(params_data)
        login.ty_login()
        res = login.get_empty_class()
        return JsonResponse(res)
