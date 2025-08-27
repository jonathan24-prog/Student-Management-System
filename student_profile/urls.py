from django.contrib import admin
from django.urls import path, include
from accounts.views import (login_view, register_view, logout_view, displayAccount, view_profile,view_instructor)
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib.auth import views as auth_views
from .views import AnnouncementViewSet,ForwardedSubmitStatusView, post_announcement, announcement_list,update_announcement, delete_announcement, GenerateExcelAPIView

router = routers.DefaultRouter()
router.register(r'enrolled_students', views.EnrolledStudentsViewSet, basename='enrolled_students')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register('subjects', views.SubjectViewSet, basename='subject')
router.register('majors', views.MajorViewSet, basename='major')
router.register('ays', views.AyViewSet, basename='ay')
router.register('courses', views.CourseViewSet, basename='course')
router.register('subjectsenrolled', views.SubjectEnrollViewSet, basename='subjectenrolled')
router.register('instructors', views.InstructorViewSet, basename='instructor')
router.register('enrolls', views.EnrollStudViewSet, basename='enroll')
router.register('students', views.StudentViewSet, basename='student')
router.register('yearlevels', views.YearLevelViewSet, basename='yearlevel')
router.register('ids', views.IdAndFullnameViewSet, basename='idfullname')
router.register('curriculums', views.CurriculumViewSet, basename='curriculum')
router.register('curriculumss', views.CurriculumsViewSet, basename='curriculumss')
router.register('aosfs', views.AOSFViewSet, basename='aosf')
router.register('instructorloads', views.InstructorLoadSubjectViewSet, basename='instructorload')
router.register('instructorloads-read', views.InstructorLoadSubjectWithObjectViewSet, basename='instructorloadread')
router.register('rooms', views.RoomViewSet, basename='room')
router.register('times', views.TimeSchedViewSet, basename='time')
router.register('days', views.DaySchedViewSet, basename='day')
router.register('activeSems', views.ActiveSemViewSet, basename='activesem')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.home, name='home'),
    path('bccapi/', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('announcements/', announcement_list, name='announcement_list'),
    path('announcements/post/', post_announcement, name='post_announcement'),
    path('announcement/update/', update_announcement, name='update_announcement'),
    path('announcement/delete/', delete_announcement, name='delete_announcement'),
    path('api/', include(router.urls)),
    path('about_us/', views.about_us, name='about_us'),
    path('bccapi/IntructorLoadedSubjectByClassList/<sem>/<ay>/<course>/<major>/<section>/<year_level>', views.IntructorLoadedSubjectByClassList.as_view(), name='IntructorLoadedSubjectByClassList'),
    path('bccapi/IntructorLoadedSubjectList/<sem>/<ay>/<instructor>', views.IntructorLoadedSubjectList.as_view(), name='IntructorLoadedSubjectList'),
    path('enroll/', views.enrollChoices, name='enrollChoices'),
    path('enrollstud/<int:pk>', views.enrollstud, name='enrollstud'),

    # for re requisite check...............
    path('check_prerequisites/', views.check_prerequisites, name='check_prerequisites'),


    # for uploading grades excel..............
    path('upload-excel/<int:student_id>', views.upload_and_displaypage, name='upload_and_displaypage'),
    path('upload-excel/', views.upload_and_display, name='upload_and_display'),
    path('save_grades/', views.save_grades, name='save_grades'),
    path('check_existing_grades/', views.check_existing_grades, name='check_existing_grades'),
    path('instructor/profile/', view_instructor, name='view_instructor'),

    path('subjects/list/', views.subject_list, name='subject-list'),

    
   

    #admin side.....
    path('manage-gradesubmition/', views.manageGradesubmition, name='manage-gradesubmition'),


    #  path('schedule_gradesubmition/', views.scheduleGradesubmition, name='schedule_gradesubmition'),
    path('set-grade-submission-schedule/',views.set_grade_submission_schedule, name='set_grade_submission_schedule'),


    # dean side.....
    # path('add-role/<str:role>/', views.add_role, name='add_role'),
    # path('teacher_list', views.teacher_list, name='teacher_list'),  
    # path('manage_subject/<int:teacher_id>/', views.manage_subject, name='manage_subject'),
    path('teacher_subject/<int:student_id>/', views.teacher_subject, name='teacher_subject'),
    

    # for creating user..............
    path('add-role/<str:role>/', views.add_role, name='add_role'),
    path('teacher_list', views.teacher_list, name='teacher_list'),  


#  adding techer subject
    path('manage_subject/<int:teacher_id>/', views.manage_subject, name='manage_subject'),
    path('manage_subjects/<int:teacher_id>/', views.manage_subjects, name='manage_subjects'),
    path('api/teacher/<int:teacher_id>/subjects/', views.get_teacher_subjects, name='get_teacher_subjects'),
    path('api/search_subjects/', views.search_subjects, name='search_subjects'),
    path('api/teacher/<int:teacher_id>/subjects/<int:subject_id>/delete/', views.delete_teacher_subject, name='delete_teacher_subject'),

  

    path('teacher/<int:teacher_id>/select_subject/', views.select_subject, name='select_subject'),
    path('teacher/<int:teacher_id>/select_subject/', views.select_subject, name='select_subject'),


    path('subject_leaderboard/', views.subject_leaderboard, name='subject_leaderboard'),
    path('api/forwarded-submit-status/', ForwardedSubmitStatusView.as_view(), name='forwarded-submit-status'),


    
path('delete_role/<str:role>/<int:user_id>/', views.delete_role, name='delete_role'),

    # template download...........
    path('template/', views.templateDownload, name='templateDownload'),
    path('students-enrolled/<int:subject_id>/', views.EnrolledStudentsViewSet.as_view({'get': 'list'}), name='students-enrolled'),
    path('bccapi/generate_excel/', GenerateExcelAPIView.as_view(), name='generate_excel'),

    # for creating user..............
    path('add-role/<str:role>/', views.add_role, name='add_role'), 
    
    # profile................
    path('view_profile/', view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('profiles/', views.profiles, name='profiles'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('delete_role_entry/<int:entry_id>/', views.delete_role_entry, name='delete_role_entry'),


    path('terms-and-Conditions/', views.terms, name='terms'),
    path('privacy-policy/', views.privacy, name='privacy'),


    


    path('searchenrolllist/<id>/<course>/<major>/<sem>/<year>/<ay>', views.SearchEnroll.as_view(), name='searchenrolllist'),
    path('register/', register_view, name='register'),
    path('registerConfirm/', views.registerConfirm, name='register-confirm'),
    path('users_page/', views.users_page, name='users_page'),
    path('addStudent/', views.addNewStudent, name='add-student'),
    path('schedules/', views.schedules, name='schedules'),
    path('addNewStudent/', views.addNewStudent, name='add-new-student'),
    path('addNewStudentAPI/', views.addNewStudentAPI, name='addNewStudentAPI'),
    path('allStudent/', views.displayAllStudent, name='allStudent'),
    path('editStudent/<int:pk>', views.editStudent, name='editStudent'),
    path('editIDs/<int:pk>', views.editIDs, name='editIDs'),
    path('addCuriculum/', views.addCuriculum, name='addCuriculum'),
    path('editCuriculum/<int:pk>/', views.editCurriculum, name='editCuriculum'),
    path('addsubjectbycuriculumAPI/<int:pk>/', views.addsubjectbycuriculumAPI, name='addsubjectbycuriculumAPI'),
    path('Apiaddsubjectbycuriculum/<course>/<major>/<sem>/<year>', views.SubjectbyCurriculum.as_view(), name='Apiaddsubjectbycuriculum'),
    path('getSubjectsByCurriculumAPI/<int:course>/<sem>', views.getSubjectsByCurriculumAPI, name='getSubjectsByCurriculumAPI'),
    path('getSubjectsByCurriculumAPI/', views.getSubjectsByCurriculumAPIAll, name='getSubjectsByCurriculumAPIAll'),
    path('addSubject/', views.addSubject, name='addSubject'),
    path('students/enroll/<int:pk>/', views.viewEnrolledStudent, name='allStudentEnroll-student'),
    path('students/enroll/student/<student_id>/', views.viewEnrolledStudentByStudentId, name='allStudentEnrollByStudentId-student'),
    path('students/viewGrades/<int:pk>/', views.viewGrades, name='viewGrades'),
    path('students/viewGradesStudent/<int:pk>/', views.viewGradesStudent, name='viewGradesStudent'),
    path('student/check/', views.checkMyEnrollment, name='checkMyEnrollment'),

    path('Admin-bcc/students/enroll/', views.viewEnrolledStudentAdmin, name='allStudentEnroll'),

    path('Api/students/enroll/<int:pk>/status', views.updateStatusAPI, name='enroll-status-api'),
    path('Api/students/enroll/<int:pk>/return', views.returnForCorrectionAPI, name='enroll-return-api'),
    path('Api/students/enroll/<int:pk>/forward', views.forwardForApprovalAPI, name='enroll-forward-api'),
    path('Api/displayAllEnrollAPI', views.displayAllEnrollAPI, name='displayAllEnrollAPI'),
    path('student/<int:pk>/', views.enroll, name='enroll'),
    path('bccapi/enrollCount/<int:pk>/', views.getEnrolledCount),
    path('Api/<int:pk>/enroll/', views.enrollSTudAPI, name='enroll-api'),
    path('student/<int:pk>/enroll/', views.enrollDetails, name='enrollDetails'),

    path('Admin-bcc/student/<int:pk>/enroll/', views.enrollDetailsAdmin, name='enrollDetailsAdmin'),

    path('Api/<int:pk>/enroll/subjects/add/', views.addSubjectLoadAPI, name='subjectLoad-api'),
    path('Api/enroll/subjects/update/', views.updateSubjectLoadAPI, name='subjectLoad-update-api'),
    path('Api/uploadSubjectsAPI/', views.uploadSubjectsAPI, name='uploadSubjectsAPI'),
    path('Api/<int:pk>/enroll/subjects/delete/', views.deleteSubjectLoaded, name='delete-enroll-subject'),
    path('Api/<int:pk>/enroll/subjects/drop/', views.dropSubjectLoaded, name='drop-enroll-subject'),
    path('Api/<int:pk>/enroll/subjects/enroll/', views.EnrolldropSubjectLoaded, name='enroll-drop-enroll-subject'),
    path('Api/enrollStudent/all/', views.StudentEnrollList.as_view(), name='student-enroll-api'),
    path('Api/enrollStudent/all/<ay>', views.StudentEnrollListByAcademicYear.as_view(), name='student-enroll-api-ay'),
    path('Api/enrollStudent/student/<int:pk>', views.StudentEnrollListByStudentId.as_view(), name='StudentEnrollListByStudentId'),
    path('Api/enrollStudent/<ay>/<course>/<sem>/<major>', views.ByCourseStudentEnrollList.as_view()),
    path('enrollSelection', views.enrollSelection, name='enrollSelection'),
    path('StudentByCourse', views.StudentByCourse, name='StudentByCourse'),
    path('Admin-bcc/managegrades', views.manageGrade, name='manage-grades'),
    path('Api/subjectloaded/<sub>/<major>/<ay>/<course>/<sem>', views.SubjectLoadedList.as_view(), name="subjects_loadedapi"),
    
    path('Admin-bcc/student/<int:instructor_pk>/grade/<int:subject_pk>/', views.gradesDetailsAdmin, name='gradesDetailsAdmin'),
    path('Api/enrollbystudins/<int:instructor>/<int:subject>/', views.SubjectByInstructorListAdmin.as_view(), name="enrollbystudinss"),

    path('Api/enrollbystudins/<instructor>/<ay>/<sem>', views.SubjectByInstructorList.as_view(), name="enrollbystudins"),
    path('Api/enrollbystudsub/<student>/<ay>/<sem>', views.SubjectByStudentList.as_view(), name="enrollbystudsub"),
    path('Api/allEnrollbySemAyCourse/<ay>/<sem>/<course>/<year>/<major>', views.AllStudentEnrollBySYAndSEM.as_view(), name="allEmrollbySemAy"),
    path('bccapi/getIdAndFullname/<student_id>', views.GetStudentIdAnfFullnameList.as_view(), name="getStudentId"),
    path('bccapi/subjects', views.SubjectsList.as_view(), name='subjects-list'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('Api/StudentList', views.StudentListView.as_view(), name="StudentList"),
    path('Api/UserList', views.UserListView.as_view(), name="UserList"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)