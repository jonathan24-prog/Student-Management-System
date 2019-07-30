"""enrollment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import (login_view,register_view,logout_view,displayAccount)
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
router = routers.DefaultRouter()
router.register('subjects', views.SubjectViewSet)
router.register('majors', views.MajorViewSet)

router.register('ays', views.AyViewSet)
router.register('courses', views.CourseViewSet)
router.register('subjectsenrolled', views.SubjectEnrollViewSet)
router.register('instructors', views.InstructorViewSet)
router.register('enrolls', views.EnrollStudViewSet)
router.register('students', views.StudentViewSet)
router.register('yearlevels', views.YearLevelViewSet)
router.register('ids', views.IdAndFullnameViewSet)
router.register('curriculums', views.CurriculumViewSet)
router.register('curriculumss', views.CurriculumsViewSet)





urlpatterns = [
    path('', views.home,name='home'),
    path('bccapi/', include(router.urls)),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('enroll/',views.enrollChoices,name='enrollChoices'),
    path('enrollstud/<int:pk>',views.enrollstud,name='enrollstud'),
    path('searchenrolllist/<id>/<course>/<major>/<sem>/<year>',views.SearchEnroll.as_view(),name='searchenrolllist'),
    path('register/',register_view,name='register'),
    path('registerConfirm/',views.registerConfirm,name='register-confirm'),
    path('addStudent/',views.addNewStudent,name='add-student'),
    path('addNewStudent/',views.addNewStudent,name='add-new-student'),

    path('allStudent/',views.displayAllStudent,name='allStudent'),
    path('editStudent/<int:pk>',views.editStudent,name='editStudent'),
    path('editIDs/<int:pk>',views.editIDs,name='editIDs'),

    path('addCuriculum/',views.addCuriculum,name='addCuriculum'),
    path('editCuriculum/<int:pk>/',views.editCurriculum,name='editCuriculum'),
    path('addsubjectbycuriculumAPI/<int:pk>/',views.addsubjectbycuriculumAPI,name='addsubjectbycuriculumAPI'),
    path('Apiaddsubjectbycuriculum/<course>/<major>/<sem>/<year>',views.SubjectbyCurriculum.as_view(),name='Apiaddsubjectbycuriculum'),
    path('getSubjectsByCurriculumAPI/<int:course>/<sem>',views.getSubjectsByCurriculumAPI,name='getSubjectsByCurriculumAPI'),
    path('getSubjectsByCurriculumAPI/',views.getSubjectsByCurriculumAPIAll,name='getSubjectsByCurriculumAPIAll'),

    path('addSubject/',views.addSubject,name='addSubject'),
    path('students/enroll/<int:pk>/',views.viewEnrolledStudent,name='allStudentEnroll-student'),
    path('student/check/',views.checkMyEnrollment,name='checkMyEnrollment'),
    path('admin/students/enroll/',views.viewEnrolledStudentAdmin,name='allStudentEnroll'),

    path('Api/students/enroll/<int:pk>/status',views.updateStatusAPI,name='enroll-status-api'),
    path('Api/students/enroll/<int:pk>/return',views.returnForCorrectionAPI,name='enroll-return-api'),
    path('Api/students/enroll/<int:pk>/forward',views.forwardForApprovalAPI,name='enroll-forward-api'),
    path('Api/displayAllEnrollAPI',views.displayAllEnrollAPI,name='displayAllEnrollAPI'),


    path('student/<int:pk>/',views.enroll,name='enroll'),
    path('EnrollPrint/<int:pk>/',views.render_pdf_view,name='print-enroll'),

    path('Api/<int:pk>/enroll/', views.enrollSTudAPI,name='enroll-api'),
    path('student/<int:pk>/enroll/', views.enrollDetails,name='enrollDetails'),
    path('Admin/student/<int:pk>/enroll/', views.enrollDetailsAdmin,name='enrollDetailsAdmin'),
    path('Api/<int:pk>/enroll/subjects/add/', views.addSubjectLoadAPI,name='subjectLoad-api'),
    path('Api/enroll/subjects/update/', views.updateSubjectLoadAPI,name='subjectLoad-update-api'),
    path('Api/uploadSubjectsAPI/',views.uploadSubjectsAPI,name='uploadSubjectsAPI'),
    path('Api/<int:pk>/enroll/subjects/delete/',views.deleteSubjectLoaded,name='delete-enroll-subject'),
    path('Api/<int:pk>/enroll/subjects/drop/',views.dropSubjectLoaded,name='drop-enroll-subject'),
    path('Api/enrollStudent/all/',views.StudentEnrollList.as_view(),name='student-enroll-api'),
    path('Api/enrollStudent/ay/course/sem/',views.ByCourseStudentEnrollList.as_view(),name='student-enroll-api'),
    path('enrollSelection',views.enrollSelection,name='enrollSelection'),
    path('StudentByCourse',views.StudentByCourse,name='StudentByCourse'),
    path('Admin/managegrades',views.manageGrade,name='manage-grades'),
    path('Api/subjectloaded/<sub>/<major>/<ay>/<course>/<sem>',views.SubjectLoadedList.as_view(),name="subjects_loadedapi"),
    path('Api/enrollbystudsub/<student>/<ay>/<sem>',views.SubjectByStudentList.as_view(),name="enrollbystudsub")

    

    


]
