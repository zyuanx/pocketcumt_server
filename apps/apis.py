from django.urls import path, include
from rest_framework import routers

import apps.config.views
import apps.library.views
import apps.micro.views
import apps.study.views

app_name = 'apis'
route = routers.DefaultRouter()
route.register('config/carousel', apps.config.views.CarouselViewSet, basename='config_carousel')
route.register('config/tips', apps.config.views.TipsViewSet, basename='config_tips')
route.register('library/search', apps.library.views.SearchBookViewSet, basename='library_search')
route.register('library/detail', apps.library.views.BookDetailViewSet, basename='library_detail')
route.register('mirco/dorm', apps.micro.views.DormViewSet, basename='mirco_dorm')
route.register('study/login', apps.study.views.LoginViewSet, basename='study_login')
route.register('study/course', apps.study.views.CourseViewSet, basename='study_course')
route.register('study/grade', apps.study.views.GradeViewSet, basename='study_grade')
route.register('study/detail_grade', apps.study.views.GradeDetailViewSet, basename='study_detail')
route.register('study/exam', apps.study.views.ExamViewSet, basename='study_exam')
route.register('study/teacher_tel', apps.study.views.TeaTelViewSet, basename='study_teacher')
route.register('study/classroom', apps.study.views.ClassroomViewSet, basename='study_classroom')

urlpatterns = [
    path('', include(route.urls)),
]
