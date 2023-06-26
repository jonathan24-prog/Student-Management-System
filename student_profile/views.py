from django.shortcuts import render,redirect,get_object_or_404
from .forms import StudentForm, EnrollForm, SubjectLoadForm,CurriculumForm,UploadExcelForm,SubjectForm,IDsNameForm,StudentFormUpdate
from .mixins import AjaxFormMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models  import ActiveSem, DaySched, TimeSched, Room, InstructorLoadSubject, AOSF, Instructor, EnrollbyStudent, Student,Major, Academic_year, Year_level,Course, SubjectsLoaded,Subject,Curriculum,IDandFullname
from django.conf import settings
from .serializers import ActiveSemSerializer, InstructorLoadSubjectWithObjectSerializer, RoomSerializer, DaySchedSerializer, TimeSchedSerializer, InstructorLoadSubjectSerializer, AOSFSerializer, StudentsEnrollSerializer, CurriculumSerializer,CurriculumsSerializer, IDandFullnameSerializer, EnrollStudSerlizer, SubjectSerializer,InstructorSerializer, StudentEnrollSerializer, SubjectsLoadedSerializer, CourseSerializer, Academic_yearSerializer, MajorSerializer,Year_levelSerializer,StudentSerializer,SubjectEnrollSerializer
from rest_framework import generics
# import numpy as np
# import pandas as pd
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets

import os
from os.path import expanduser

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
# from xhtml2pdf import pisa
# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
# import numpy as np
# from openpyxl import load_workbook
# Create your views here.



# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     # use short variable names
#     sUrl = settings.STATIC_URL      # Typically /static/
#     sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
#     mUrl = settings.MEDIA_URL       # Typically /static/media/
#     mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

#     # convert URIs to absolute system paths
#     if uri.startswith(mUrl):
#         path = os.path.join(mRoot, uri.replace(mUrl, ""))
#     elif uri.startswith(sUrl):
#         path = os.path.join(sRoot, uri.replace(sUrl, ""))
#     else:
#         return uri  # handle absolute uri (ie: http://some.tld/foo.png)

#     # make sure that file exists
#     if not os.path.isfile(path):
#             raise Exception(
#                 'media URI must start with %s or %s' % (sUrl, mUrl)
#             )
#     return path




# def render_pdf_view(request,pk):
# 	enroll_stud=get_object_or_404(EnrollbyStudent,pk=pk)
# 	subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll_stud,status="enrolled")
# 	template_path = 'student_profile/user_printer.html'
# 	now = datetime.now(timezone.utc)
# 	total_units=0
# 	for sub in subjects:
# 		total_units=total_units+sub.subject.unit
# 	context = {'enroll': enroll_stud,'subjects': subjects,'time':now.strftime('%b %d, %Y'),'total_units':total_units}
# 	# Create a Django response object, and specify content_type as pdf
# 	response = HttpResponse(content_type='application/pdf')
# 	# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
# 	# find the template and render it.
# 	template = get_template(template_path)
# 	html = template.render(context)

# 	# create a pdf
# 	pisaStatus = pisa.CreatePDF(
# 	html, dest=response, link_callback=link_callback)
# 	# if error then show some funy view
# 	if pisaStatus.err:
# 		return HttpResponse('We had some errors <pre>' + html + '</pre>')
# 	return response


class enrollFormView(AjaxFormMixin, FormView):
    form_class = EnrollForm
    template_name  = 'forms/ajax.html'
    success_url = '/form-success/'


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def enrollSTudAPI(request,pk):

	if request.method=='POST':
		form=EnrollForm(request.POST)
		if form.is_valid():
			student=get_object_or_404(Student,pk=pk)
			enroll_key=student.student_id+str(form.cleaned_data['academic_year'])+str(form.cleaned_data['course'])+str(form.cleaned_data['semister'])
			student_enrollKey=EnrollbyStudent.objects.filter(enrollment_key=enroll_key)
			if not student_enrollKey.exists():
				enroll=form.save(commit=False)
				enroll.student=student
				enroll.enrollment_key=enroll_key
				enroll.save()


				enrollRes={'pk': enroll.pk,'message':'enrolled successfully','is_save':True}
				return Response(enrollRes)
			else:
				enrollRes={'message':'already enrolled on this semister','is_save':False}
				return Response(enrollRes)
		return Response({'message':'invalid forms'})
	return Response({'message':'get request'})



@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def updateStatusAPI(request,pk):
	enroll=get_object_or_404(EnrollbyStudent,pk=pk)
	subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll)
	if request.method=='POST':
		if subjects.exists():
			enroll.status='approved'
			enroll.date_created=datetime.now(timezone.utc)
			enroll.save()
			serialize_subjects=[]
			for subject_loaded in subjects:
				subject_loaded.status="enrolled"
				subject_loaded.save()


				subject_enroll={'pk':str(subject_loaded.pk),'subject_pk':str(subject_loaded.subject.pk),'code':subject_loaded.subject.code,
					'description':subject_loaded.subject.description,'unit':subject_loaded.subject.unit,'status':subject_loaded.status}
				serialize_subjects.append(subject_enroll)

			return Response({'message':'ok','enroll_status':'approved','subjects':serialize_subjects})
		return Response({'message':'you don\'t have subjects added'})
	return Response({'message':'get request'})



@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def returnForCorrectionAPI(request,pk):
	enroll=get_object_or_404(EnrollbyStudent,pk=pk)
	subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll)
	if request.method=='POST':
		if subjects.exists():
			enroll.status='returned for correction'
			enroll.save()
			serialize_subjects=[]
			for subject_loaded in subjects:
				subject_loaded.status="returned for correction"
				subject_loaded.save()


				subject_enroll={'pk':str(subject_loaded.pk),'subject_pk':str(subject_loaded.subject.pk),'code':subject_loaded.subject.code,
					'description':subject_loaded.subject.description,'unit':subject_loaded.subject.unit,'status':subject_loaded.status}
				serialize_subjects.append(subject_enroll)

			return Response({'message':'ok','enroll_status':enroll.status,'subjects':serialize_subjects})
		return Response({'message':'you don\'t have subjects added'})
	return Response({'message':'get request'})




@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def displayAllEnrollAPI(request):
	enrollees=EnrollbyStudent.objects.all()
	enroll_dic_list=[]

	for enrollee in enrollees:
		enroll_dic_list.append({'student_id':str(enrollee.student.student_id),
			'fullname': enrollee.student.first_name + " " + enrollee.student.middle_name +" "+enrollee.student.last_name,
			'course':enrollee.course.code, 'ay':enrollee.academic_year.ay,'semister':enrollee.semister,'status':enrollee.status})
	context={'enrollees':enroll_dic_list}
	return Response(context)







@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def forwardForApprovalAPI(request,pk):
	enroll=get_object_or_404(EnrollbyStudent,pk=pk)
	subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll)
	if request.method=='POST':
		if subjects.exists():
			enroll.status='forwarded'
			enroll.save()
			serialize_subjects=[]
			for subject_loaded in subjects:
				subject_loaded.status="forwarded"
				subject_loaded.save()


				subject_enroll={'pk':str(subject_loaded.pk),'subject_pk':str(subject_loaded.subject.pk),'code':subject_loaded.subject.code,
					'description':subject_loaded.subject.description,'unit':subject_loaded.subject.unit,'status':subject_loaded.status}
				serialize_subjects.append(subject_enroll)

			return Response({'is_forwarded': True,'message':'forward successfully','enroll_status':'forwarded','subjects':serialize_subjects})
		return Response({'message':'you don\'t have subjects added','is_forwarded': False})
	return Response({'message':'get request'})







def viewEnrolledStudentAdmin(request):
	enroll_students=EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").all()

	context={'enroll_students':enroll_students}
	

	return render(request,'student_profile/enroll_students.html',{})


def manageGrade(request):
	return render(request,'student_profile/manage_grades.html',{})



	
def viewEnrolledStudent(request,pk):
	student=get_object_or_404(Student,pk=pk)
	enroll_students=EnrollbyStudent.objects.filter(student=student)
	context={'enroll_students':enroll_students,'student':student}
	return render(request,'student_profile/byStudentEnrollList.html',context)
def viewEnrolledStudentByStudentId(request,student_id):
	student=get_object_or_404(Student,student_id=student_id)
	enroll_students=EnrollbyStudent.objects.filter(student=student)
	context={'enroll_students':enroll_students,'student':student}
	return render(request,'student_profile/byStudentEnrollList.html',context)

def enrollstud(request,pk):
	return render(request,'student_profile/enrollstud.html',{'student_id':pk})

@api_view(['GET'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def getEnrolledCount(request, pk):
	student = get_object_or_404(Student,pk=pk)
	enroll_by_students = EnrollbyStudent.objects.filter(student=student, status= 'approved')
	return Response({'enroll_count':len(enroll_by_students)})






class ByCourseStudentEnrollList(generics.ListAPIView):
	serializer_class = StudentsEnrollSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes=(SessionAuthentication,)

	def get_queryset(self):
		ay_pk=self.kwargs['ay']
		course_pk=self.kwargs['course']
		sem=self.kwargs['sem']
		major_pk = self.kwargs['major']
		if major_pk != "0":
			course=get_object_or_404(Course,pk=course_pk)
			ay=get_object_or_404(Academic_year,pk=ay_pk)
			major = get_object_or_404(Major,pk=major_pk)
			return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(semister=sem,course=course,academic_year=ay,status="approved", major=major).order_by('year_level','major', 'student__last_name')
		else:
			course=get_object_or_404(Course,pk=course_pk)
			ay=get_object_or_404(Academic_year,pk=ay_pk)
	
			return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(semister=sem,course=course,academic_year=ay,status="approved").order_by('year_level','major', 'student__last_name')
	


class SubjectsList(generics.ListAPIView):
	serializer_class = SubjectSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes=(SessionAuthentication,)

	def get_queryset(self):
		return Subject.objects.all()

class StudentEnrollListByAcademicYear(generics.ListAPIView):
	serializer_class = StudentEnrollSerializer
	
	def get_queryset(self):
		ayId = self.kwargs['ay']
		ay = get_object_or_404(Academic_year,pk=ayId)
		return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(academic_year=ay)



class StudentEnrollList(generics.ListAPIView):
	serializer_class = StudentEnrollSerializer
	
	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").all()

class AllStudentEnrollBySYAndSEM(generics.ListAPIView):
	serializer_class = StudentEnrollSerializer
	
	def get_queryset(self):
		sem=self.kwargs['sem']
		ayId = self.kwargs['ay']
		coursePk = self.kwargs['course']
		yearPk = self.kwargs['year']
		majorPk = self.kwargs['major']
		ay = get_object_or_404(Academic_year,pk=ayId)
		course = get_object_or_404(Course,pk=coursePk)
		year = get_object_or_404(Year_level,pk=yearPk)
		results = []
		if majorPk != '-1':
			major = get_object_or_404(Major, pk = majorPk)
			results = EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(major = major,academic_year=ay, semister = sem, course = course, year_level= year, status ='approved').all()
			if len(results) != 0:
				return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(major = major,academic_year=ay, semister = sem, course = course, year_level= year, status ='approved').all()
			
			return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(academic_year=ay, semister = sem, course = course, year_level= year, status ='approved').all()
				
		return EnrollbyStudent.objects.select_related("student").select_related("year_level").select_related("academic_year").select_related("major").select_related("course").filter(academic_year=ay, semister = sem, course = course, year_level= year, status ='approved').all()
		




class SubjectbyCurriculum(generics.ListAPIView):
	serializer_class= SubjectSerializer
	def get_queryset(self):
		major_pk=self.kwargs['major']
		course_pk=self.kwargs['course']
		sem=self.kwargs['sem']
		yearpk=self.kwargs['year']
		if major_pk != "0":
			year=get_object_or_404(Year_level,pk=yearpk)
			major=get_object_or_404(Major,pk=major_pk)
			course=get_object_or_404(Course,pk=course_pk)
			return  Curriculum.objects.filter(course=course,year_level=year,semister=sem,major=major).first().subjects.all()

		
		year=get_object_or_404(Year_level,pk=yearpk)
		course=get_object_or_404(Course,pk=course_pk)
		return Curriculum.objects.filter(course=course,year_level=year,semister=sem).first().subjects.all()

class SearchEnroll(generics.ListAPIView):
	serializer_class= EnrollStudSerlizer
	def get_queryset(self):
		major_pk=self.kwargs['major']
		course_pk=self.kwargs['course']
		sem=self.kwargs['sem']
		year=self.kwargs['year']
		ay = self.kwargs['ay']
		student=get_object_or_404(Student,pk=self.kwargs['id'])

		if major_pk != "0":
			
			major=get_object_or_404(Major,pk=major_pk)
			course=get_object_or_404(Course,pk=course_pk)
			year=get_object_or_404(Year_level,pk=year)
			academic_year = get_object_or_404(Academic_year,pk = ay)
			return EnrollbyStudent.objects.filter(academic_year = academic_year, student=student,semister=sem,course=course,year_level=year,major=major)


		
		course=get_object_or_404(Course,pk=course_pk)
		year=get_object_or_404(Year_level,pk=year)
		academic_year = get_object_or_404(Academic_year,pk = ay)
		return EnrollbyStudent.objects.filter(academic_year = academic_year,student=student,semister=sem,course=course,year_level=year)





		


class SubjectLoadedList(generics.ListAPIView):
	serializer_class= SubjectEnrollSerializer
	def get_queryset(self):
		sub_pk=self.kwargs['sub']
		major_pk=self.kwargs['major']
		course_pk=self.kwargs['course']
		sem=self.kwargs['sem']
		ay=self.kwargs['ay']

		if major_pk != "0":
			sub=get_object_or_404(Subject,pk=sub_pk)
			major=get_object_or_404(Major,pk=major_pk)
			course=get_object_or_404(Course,pk=course_pk)
			academic_y=get_object_or_404(Academic_year,pk=ay)
			return SubjectsLoaded.objects.select_related("enrolled_by_student").filter(enrolled_by_student__course=course,enrolled_by_student__academic_year=academic_y,enrolled_by_student__semister=sem,subject=sub,enrolled_by_student__major=major,status="enrolled")
		if major_pk == "0" and course_pk == "0":
			sub=get_object_or_404(Subject,pk=sub_pk)
			academic_y=get_object_or_404(Academic_year,pk=ay)
			return SubjectsLoaded.objects.select_related("enrolled_by_student").filter(enrolled_by_student__academic_year=academic_y,enrolled_by_student__semister=sem,subject=sub,status="enrolled")
	


		
		sub=get_object_or_404(Subject,pk=sub_pk)
		course=get_object_or_404(Course,pk=course_pk)
		academic_y=get_object_or_404(Academic_year,pk=ay)
		return SubjectsLoaded.objects.select_related("enrolled_by_student").filter(enrolled_by_student__course=course,enrolled_by_student__academic_year=academic_y,enrolled_by_student__semister=sem,subject=sub,status="enrolled")



class SubjectByStudentList(generics.ListAPIView):
	serializer_class= SubjectEnrollSerializer
	def get_queryset(self):
		stud=self.kwargs['student']
		sem=self.kwargs['sem']
		ay=self.kwargs['ay']

		student=get_object_or_404(Student,pk=stud)
		academic_y=get_object_or_404(Academic_year,pk=ay)
		return SubjectsLoaded.objects.select_related("enrolled_by_student").filter(enrolled_by_student__student=student,enrolled_by_student__academic_year=academic_y,enrolled_by_student__semister=sem,status="enrolled")


class IntructorLoadedSubjectList(generics.ListAPIView):
	serializer_class= InstructorLoadSubjectWithObjectSerializer
	def get_queryset(self):
		instruc=self.kwargs['instructor']
		sem=self.kwargs['sem']
		ay=self.kwargs['ay']

		instructor=get_object_or_404(Instructor,pk=instruc)
		academic_y=get_object_or_404(Academic_year,pk=ay)
		return InstructorLoadSubject.objects.filter(instructor=instructor,academic_year=academic_y,semister=sem)

class IntructorLoadedSubjectByClassList(generics.ListAPIView):
	serializer_class= InstructorLoadSubjectWithObjectSerializer
	def get_queryset(self):
		course_pk=self.kwargs['course']
		sem=self.kwargs['sem']
		ay=self.kwargs['ay']
		section = self.kwargs['section']
		major_pk = self.kwargs['major']
		year_level_pk = self.kwargs['year_level']
		year_level = get_object_or_404(Year_level,pk=year_level_pk)
		course=get_object_or_404(Course,pk=course_pk)
		academic_y=get_object_or_404(Academic_year,pk=ay)
		if major_pk == '-1':
			return InstructorLoadSubject.objects.filter(course=course,academic_year=academic_y,semister=sem, section=section, year_level = year_level)
		major = get_object_or_404(Major,pk=major_pk)
		return InstructorLoadSubject.objects.filter(course=course,academic_year=academic_y,semister=sem, section=section, year_level = year_level, major=major)



class GetStudentIdAnfFullnameList(generics.ListAPIView):
	serializer_class= IDandFullnameSerializer
	def get_queryset(self):
		student_id=self.kwargs['student_id']
		return IDandFullname.objects.filter(student_id=student_id)




		



class EnrollStudViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
	
    queryset = EnrollbyStudent.objects.all()
    serializer_class = EnrollStudSerlizer

class IdAndFullnameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = IDandFullname.objects.all()
    serializer_class = IDandFullnameSerializer


class CurriculumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

class CurriculumsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumsSerializer



class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Student.objects.select_related("course").select_related("major").all()
    serializer_class = StudentSerializer

class MajorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class AyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Academic_year.objects.all()
    serializer_class = Academic_yearSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class SubjectEnrollViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = SubjectsLoaded.objects.all()
    serializer_class = SubjectsLoadedSerializer

class YearLevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Year_level.objects.all()
    serializer_class = Year_levelSerializer

class AOSFViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = AOSF.objects.all()
    serializer_class = AOSFSerializer

class ActiveSemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = ActiveSem.objects.all()
    serializer_class = ActiveSemSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class =RoomSerializer

class DaySchedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = DaySched.objects.all()
    serializer_class =DaySchedSerializer

class TimeSchedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = TimeSched.objects.all()
    serializer_class =TimeSchedSerializer

class InstructorLoadSubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = InstructorLoadSubject.objects.all()
    serializer_class = InstructorLoadSubjectSerializer

class InstructorLoadSubjectWithObjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = InstructorLoadSubject.objects.all()
    serializer_class = InstructorLoadSubjectWithObjectSerializer

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def addSubjectLoadAPI(request,pk):

	enrollbyStud=get_object_or_404(EnrollbyStudent,pk=pk)
	enroll_subject=SubjectsLoaded.objects.filter(enrolled_by_student=enrollbyStud)


	if request.method == 'POST':
		form=SubjectLoadForm(request.POST)

		if form.is_valid():

			addSubject=form.save(commit=False)
			duplicate_subject=enroll_subject.filter(subject=addSubject.subject)
			if not duplicate_subject.exists():
				addSubject.enrolled_by_student=enrollbyStud
				addSubject.status="draft"
				addSubject.save()
				
				context={
						'pk':str(addSubject.pk),
						'subject_pk':str(addSubject.subject.pk),
						'code':str(addSubject.subject.code),
						'description':str(addSubject.subject.description),
						'unit':str(addSubject.subject.unit),
						'status':str(addSubject.status),
						'is_save':True}
				return Response(context)
			return Response({'message':'subject already enroll','is_save':False})
		return Response({'message':'fail','is_save':False})
	return Response({'message':'get request'})



@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def updateSubjectLoadAPI(request):

	if request.method == 'POST':
		subject_pk=request.POST
		subject=get_object_or_404(SubjectsLoaded,pk=subject_pk['is_updated'])
		form = SubjectLoadForm(request.POST, instance=subject)
		if form.is_valid():
			addSubject=form.save(commit=False)
			addSubject.save()
	
			context={
						'pk':str(addSubject.pk),
						'subject_pk':str(addSubject.subject.pk),
						'code':str(addSubject.subject.code),
						'description':str(addSubject.subject.description),
						'unit':str(addSubject.subject.unit),
						'status':str(addSubject.status),
					'is_updated':True,}
			return Response(context)

		return Response({'is_updated':False})
	return Response({'message':'get request'})








@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteSubjectLoaded(request,pk):
	subject=get_object_or_404(SubjectsLoaded,pk=pk)
	if request.method == 'POST':
		subject.delete()
		return Response({'is_delete':True})
	return Response({'is_delete':False})




@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def dropSubjectLoaded(request,pk):
	subject=get_object_or_404(SubjectsLoaded,pk=pk)
	if request.method == 'POST':
		subject.status="drop"
		subject.save()
		serializer=SubjectsLoadedSerializer(subject)
		return Response(serializer.data)
	return Response({'is_drop':False})


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def EnrolldropSubjectLoaded(request,pk):
	subject=get_object_or_404(SubjectsLoaded,pk=pk)
	if request.method == 'POST':
		subject.status="enrolled"
		subject.save()
		serializer=SubjectsLoadedSerializer(subject)
		return Response(serializer.data)
	return Response({'is_enroll':False})



@login_required(login_url=settings.LOGIN_URL)
def home(request):
	forwarded=EnrollbyStudent.objects.filter(status='forwarded')
	return render(request,'student_profile/index.html',{'user':request.user,'count':0,'forwarded':forwarded})

@login_required(login_url=settings.LOGIN_URL)
def addNewStudent(request):
	form=StudentForm()
	students=Student.objects.all()
	if request.method == "POST":

		form=StudentForm(request.POST or None)
		if form.is_valid():
			student=form.save(commit=False)
			student.save()
			return redirect('enrollstud',student.pk)
	return render(request,'student_profile/add_student.html',{'form':form,'students':students})

@login_required(login_url=settings.LOGIN_URL)
def addNewStudentAPI(request):

	return render(request,'student_profile/add_student_api.html')

@login_required(login_url=settings.LOGIN_URL)
def addStudent(request):
	form=StudentForm()
	students=Student.objects.all()
	if request.method == "POST":

		form=StudentForm(request.POST or None)
		if form.is_valid():
			student=form.save(commit=False)
			student.save()
			return redirect('home')
	return render(request,'student_profile/addStudent.html',{'form':form,'students':students})

@login_required(login_url=settings.LOGIN_URL)
def addCuriculum(request):
    form=CurriculumForm()
    curriculums=Curriculum.objects.all()
    if request.method == 'POST':
        form=CurriculumForm(request.POST)
        if form.is_valid():
            curriculum=form.save()
            # updateUnique slug for query porposes
            if curriculum.major == None:
            	curriculum.slug=str(curriculum.course.pk)+str(curriculum.year_level.pk)+str(curriculum.semister)
            else:
            	curriculum.slug=str(curriculum.course.pk)+str(curriculum.year_level.pk)+str(curriculum.semister)+str(curriculum.major.pk)  
            curriculum.save()
            return redirect('addCuriculum')
    context={'form':form,'curriculums':curriculums}
    return render(request,'student_profile/addCurriculumAPI.html',context)

@login_required(login_url=settings.LOGIN_URL)
def editCurriculum(request,pk):
	curriculum=get_object_or_404(Curriculum,pk=pk)
	form=CurriculumForm(instance=curriculum)
	if request.method == 'POST':
		form=CurriculumForm(request.POST,instance=curriculum)
		if form.is_valid():
			cur=form.save(commit=False)
			if cur.major == None:
				cur.slug=str(cur.course.pk)+str(cur.year_level.pk)+str(cur.semister)
				cur.save()
			cur.save()

			return redirect('addCuriculum')

	context={'form':form}
	return render(request,'student_profile/editCurriculum.html',context)



def editStudent(request,pk):
	student=get_object_or_404(Student,pk=pk)
	form=StudentFormUpdate(instance=student)
	if request.method == 'POST':
		form = StudentFormUpdate(request.POST,instance=student)
		if form.is_valid():
			form.save()
			return redirect('allStudent')

	context={'form':form}
	return render(request,'student_profile/edit_student.html', context)


def editIDs(request,pk):
	stud_id=get_object_or_404(IDandFullname,pk=pk)
	form=IDsNameForm(instance=stud_id)
	if request.method == 'POST':
		form = IDsNameForm(request.POST,instance=stud_id)
		if form.is_valid():
			form.save()
			return redirect('allStudent')

	context={'form':form}
	return render(request,'student_profile/edit_IDs.html', context)


@login_required(login_url=settings.LOGIN_URL)
def addSubject(request):
	form_upload=UploadExcelForm()
	form_subject=SubjectForm()
	if request.method=='POST':
		form=UploadExcelForm(request.POST,request.FILES)
		if form.is_valid():
			# excel=form.save(commit=False)
			# excel.save()
			# df = pd.read_excel('C:/Bitnami/djangostack-2.1.1-1/apps/django/django_projects/enrollment'+excel.file.url, sheet_name=0)  
			
			# for cell in df.values:
			# 	print('naka abot')
			# 	subject_exists=Subject.objects.filter(code=cell[0],description=cell[1])
			# 	if not subject_exists.exists():
			# 		Subject.objects.create(code=cell[0],description=cell[1],unit=cell[2])



			return redirect('addSubject')
	context={'form_upload':form_upload,'form_subject':form_subject,'subjects':Subject.objects.all()}
	return render(request,'student_profile/addSubject.html',context)


# @login_required(login_url=settings.LOGIN_URL)
# def addIDandName(request):
# 	form_upload=UploadExcelForm()
# 	form_subject=SubjectForm()
# 	if request.method=='POST':
# 		form=UploadExcelForm(request.POST,request.FILES)
# 		if form.is_valid():
# 			excel=form.save(commit=False)
# 			excel.save()
# 			df = pd.read_excel('C:/Bitnami/djangostack-2.1.1-1/apps/django/django_projects/enrollment'+excel.file.url, sheet_name=0)  
			
# 			for cell in df.values:
# 				print('naka abot')
# 				id_exists=IDandFullname.objects.filter(student_id=cell[0],first_name=cell[1],last_name=cell[2])
# 				if not id_exists.exists():
# 					IDandFullname.objects.create(student_id=cell[0],first_name=cell[1],last_name=cell[2])



# 			return redirect('addSubject')
# 	context={'form_upload':form_upload,'form_subject':form_subject,'subjects':Subject.objects.all()}
# 	return render(request,'student_profile/addSubject.html',context)



@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def getSubjectsByCurriculumAPI(request,*args,**kwargs):
		
	queryset = Curriculum.objects.all()
	sem = kwargs['sem']
	course_pk=kwargs['course']
	course=Course.objects.get(pk=course_pk)


	curriculums=queryset.filter(course=course,semister=sem)

	subjects=[]
	for curriculum in curriculums:
		for subject in curriculum.subjects.all():
			serializer=SubjectSerializer(subject)
			subjects.append(serializer.data)



	context={'subjects':subjects}



	return Response(context)




@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def getSubjectsByCurriculumAPIAll(request,*args,**kwargs):


	# queryset = Curriculum.objects.all()
	# sem = kwargs['sem']
	# course_pk=kwargs['course']
	# course=Course.objects.get(pk=course_pk)


	curriculums=Curriculum.objects.prefetch_related('subjects').all()


	subjects=[]
	for curriculum in curriculums:
		for subject in curriculum.subjects.all():
			serializer=SubjectSerializer(subject)
			subjects.append(serializer.data)



	context={'subjects':subjects}



	return Response(context)




def StudentByCourse(request):


	# sy=request.GET.get('ay')
	# course_pk=request.GET.get('course')

	# ay=Academic_year.objects.get(pk=sy)
	# course=Course.objects.get(pk=course_pk)
	# semister=request.GET.get('semister')



	# subjects_loaded=SubjectsLoaded.objects.all()
	# student_enroll=[]

	# if request.method == "POST":
	# 	student_enrollExcel=[]
	# 	course=Course.objects.get(pk=request.POST.get('course_pk'))
	# 	ay=Academic_year.objects.get(pk=request.POST.get('ay_pk'))

	# 	students=EnrollbyStudent.objects.filter(course=course,status="approved",academic_year=ay,semister=request.POST.get('semister'))
	
	# 	for student in students:
	# 		subjects=SubjectsLoaded.objects.filter(enrolled_by_student=student,status="enrolled")
	# 		total_units=0
	# 		course_codes=""
	# 		course_descs=""
	# 		for subject in subjects:
				
	# 			#now.strftime('%b %d, %Y')
	# 			total_units=total_units+subject.subject.unit
	# 			if course_codes == "":
	# 				course_codes=course_codes+subject.subject.code
	# 			else:
	# 				course_codes=course_codes+","+subject.subject.code

	# 			if course_descs == "":
	# 				course_descs=course_descs+subject.subject.description

	# 			else:
	# 				course_descs=course_descs+","+subject.subject.description




				
	# 		if not student.major == None:	
	# 			course_str=str(student.course) +" "+str(student.major)
	# 		else:
	# 			course_str=str(student.course)


	# 		student_enrollExcel.append([student.student.student_id,student.student.last_name,
	# 								student.student.first_name,student.student.middle_name,
	# 								student.student.ext_name,student.student.gender,student.student.address,student.student.birth_date,
	# 								course_str,student.year_level,student.student.zip_code,
	# 								student.student.email_add,student.student.mobile_no,
	# 								total_units,course_codes,course_descs])

	# 	df=pd.DataFrame(student_enrollExcel)
	# 	print(os.environ['USERPROFILE'])
	# 	home = expanduser("C:/Users/yamamz/Desktop")
	# 	writer=ExcelWriter(home+"/Report/report.xlsx")
	# 	df.to_excel(writer,'sheet1',index=False,header=False)
	# 	writer.save()






	# students=EnrollbyStudent.objects.filter(course=course,status="approved",academic_year=ay,semister=semister)
	
	# for student in students:

	# 	subjects=SubjectsLoaded.objects.filter(enrolled_by_student=student,status="enrolled")
	# 	total_units=0
	# 	course_codes=""
	# 	course_descs=""
	# 	for subject in subjects:
			
	# 		#now.strftime('%b %d, %Y')
	# 		total_units=total_units+subject.subject.unit
	# 		if course_codes == "":
	# 			course_codes=course_codes+subject.subject.code
	# 		else:
	# 			course_codes=course_codes+","+subject.subject.code

	# 		if course_descs == "":
	# 			course_descs=course_descs+subject.subject.description

	# 		else:
	# 			course_descs=course_descs+","+subject.subject.description

	# 	student_enroll.append({'student_id':student.student.student_id,'first_name':student.student.first_name,
	# 							'last_name':student.student.last_name,'middle_name':student.student.middle_name,
	# 							'ext_name':student.student.ext_name,'gender':student.student.gender,'birth_date':student.student.birth_date,
	# 							'course':student.course,'year_level':student.year_level,'zip_code':student.student.zip_code,
	# 							'email_add':student.student.email_add,'mobile_no':student.student.mobile_no,
	# 							'total_units':total_units,'course_codes':course_codes,'course_descs':course_descs})

	# context={'enroll_students':student_enroll,'course':course,'semister':semister,'ay':ay}

	return render(request,'student_profile/byCourse.html',{})






def enrollSelection(request):
	ays=Academic_year.objects.all()
	courses=Course.objects.all()
	return render(request,'student_profile/byStudCattegory.html',{'ays':ays,'courses':courses})


	
def viewGrades(request,pk):
	enroll= get_object_or_404(EnrollbyStudent, pk = pk)
	return render(request,'student_profile/view_grades.html',{'enroll':enroll})
def viewGradesStudent(request,pk):
	enroll= get_object_or_404(EnrollbyStudent, pk = pk)
	return render(request,'student_profile/view_grade_student.html',{'enroll':enroll})




@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def Apiaddsubjectbycuriculum(request,*args,**kwargs):
	major_pk=kwargs['majorpk']

	try:
		course=Course.objects.get(pk=request.POST.get('coursepk'))


		year=Year_level.objects.get(pk=request.POST.get('yearpk'))
		sem=request.POST.get('semister')
		major=Major.objects.get(pk=major_pk)
		subjects_by_curriculum= Curriculum.objects.filter(course=course,year_level=year,semister=sem,major=major)
	except Major.DoesNotExist:
		major = None

	if major == None:
		subjects_by_curriculum= Curriculum.objects.filter(course=course,year_level=year,semister=sem)



		
		


	if subjects_by_curriculum.exists():
		subjects={'status':True,'subjects':subjects_by_curriculum[0].subjects.all(),'message':'subjects added'}
		return Response(subjects)
	return Response({'status':False,'message':'curriculum does not exist'})














@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def addsubjectbycuriculumAPI(request,pk):
	enrollbyStud=get_object_or_404(EnrollbyStudent,pk=pk)
	if request.method == "POST":
		major_pk=request.POST.get('majorpk')
		if major_pk == "":
			major_pk=0

		try:
			course=Course.objects.get(pk=request.POST.get('coursepk'))


			year=Year_level.objects.get(pk=request.POST.get('yearpk'))
			sem=request.POST.get('semister')
			major=Major.objects.get(pk=major_pk)
			subjects_by_curriculum= Curriculum.objects.filter(course=course,year_level=year,semister=sem,major=major)
		except Major.DoesNotExist:
			major = None

		if major == None:
			subjects_by_curriculum= Curriculum.objects.filter(course=course,year_level=year,semister=sem)



			
			


		if subjects_by_curriculum.exists():
			
			serialize_subjects=[]
			for subject in subjects_by_curriculum[0].subjects.all():
				duplicate_subject=SubjectsLoaded.objects.filter(enrolled_by_student=enrollbyStud,subject=subject)

				
				if not duplicate_subject.exists():
					subject_loaded=SubjectsLoaded.objects.create(enrolled_by_student=enrollbyStud,subject=subject,status="draft")
					subject_enroll={'pk':str(subject_loaded.pk),'subject_pk':str(subject_loaded.subject.pk),'code':subject_loaded.subject.code,
					'description':subject_loaded.subject.description,'unit':subject_loaded.subject.unit,'status':subject_loaded.status}
					serialize_subjects.append(subject_enroll)

			subjects={'status':True,'subjects':serialize_subjects,'message':'subjects added'}
			return Response(subjects)


					

			

		return Response({'status':False,'message':'curriculum does not exist'})

	return Response({'message':'get'})


@login_required(login_url=settings.LOGIN_URL)
def enrollChoices(request):
	return render(request,'student_profile/choices.html')






@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def uploadSubjectsAPI(request):
	if request.method == 'POST':
		form=UploadExcelForm(request.POST,request.FILES)
		if form.is_valid():

			form.save()
			df = pd.read_excel('C:/Bitnami/djangostack-2.1.1-1/apps/django/django_projects/enrollment'+form.file.url, sheet_name=0)  
			for cell in df.values:
				Subject.objects.create(code=cell[0],description=cell[1],unit=cell[2])
				context={'is_save':True}
			return Response(context)

		return Response({'is_save':False})
	return Response({'message':'get'})



	







@login_required(login_url=settings.LOGIN_URL)
def enroll(request,pk):
	student=get_object_or_404(Student,pk=pk)
	form=EnrollForm()
	form2=SubjectLoadForm()
	context={'student':student,'form':form,'form2':form2}
	if request.method == 'POST':
		form= EnrollForm(request.POST)
		if form.is_valid():
			enroll=form.save(commit=False)
			enroll.student=student
			if not enroll.major == None:
				student_enroll=EnrollbyStudent.objects.filter(student=enroll.student,
															course=enroll.course,
															year_level=enroll.year_level,
															semister=enroll.semister,
															major=enroll.major)
			else:
				student_enroll=EnrollbyStudent.objects.filter(student=enroll.student,
															course=enroll.course,
															year_level=enroll.year_level,
															semister=enroll.semister)

			if not student_enroll.exists():	
				enroll.status='draft'
				enroll.save()
				return redirect('enrollDetails', pk=enroll.pk)


		student=get_object_or_404(Student,pk=pk)
		form=EnrollForm()

		context={'student':student,'form':form,'form2':form2,'message':'the student already enrolled in this course with the same acamemic year and semister'}
		return render(request,'student_profile/enroll.html',context)

	context={'student':student,'form':form}
	return render(request,'student_profile/enroll.html',context)


def enrollDetails(request,pk):
    form=SubjectLoadForm()

    enroll=get_object_or_404(EnrollbyStudent,pk=pk)
    subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll)
    form2=EnrollForm(instance=enroll)

    if request.method == 'POST':
    	form2=EnrollForm(request.POST,instance=enroll)
    	if form2.is_valid():
    		form2.save()
    		return redirect('enrollDetails',enroll.pk)

    context={'enroll':enroll,'form':form,'form2':form2,'subjects':subjects}
    return render(request,'student_profile/enrolldetailss.html',context)


def enrollDetailsAdmin(request,pk):
    form=SubjectLoadForm()
    enroll=get_object_or_404(EnrollbyStudent,pk=pk)
    subjects=SubjectsLoaded.objects.filter(enrolled_by_student=enroll)

    # if request.method == 'POST':
    total_units=0
    for sub in subjects:
    	total_units=total_units+sub.subject.unit

    context={'enroll':enroll,'form':form,'subjects':subjects,'total_units':total_units}
    return render(request,'student_profile/enrollDetailsAdmins.html',context)


def checkMyEnrollment(request):
	if request.method == 'POST':
		student_id=request.POST.get('student_id')
		try:
			student=Student.objects.get(student_id=student_id)
		except Student.DoesNotExist:
			student=None

		if not student == None:
			return redirect('allStudentEnroll-student',student.pk)
		else:
			return render(request,'student_profile/check_my_enrollment.html',{'message':'Student ID doest not exists'})



	return render(request,'student_profile/check_my_enrollment.html',{})




def registerConfirm(request):
	return render(request,'student_profile/registerConfirmation.html')


def displayAllStudent(request):
	return render(request,'student_profile/allStudent.html',{})

def schedules(request):
		return render(request,'student_profile/schedules.html',{})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'student_profile/password_reset.html'
    email_template_name = 'student_profile/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')

