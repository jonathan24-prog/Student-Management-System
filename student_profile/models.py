from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
User = get_user_model()





class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date', '-created_at']


class Year_level(models.Model):
	code=models.CharField(max_length=6)
	description=models.CharField(max_length=100)

	def __str__(self):
		return self.description
class Course(models.Model):
	code=models.CharField(max_length=50)
	description=models.CharField(max_length=200)

	def __str__(self):
		return self.code

class Major(models.Model):
	name=models.CharField(max_length=300)
	description=models.CharField(max_length=200)
	def __str__(self):
		return self.description

class Academic_year(models.Model):
	ay=models.CharField(max_length=100)
	status=models.BooleanField(default=True, null=True)

	def __str__(self):
		return self.ay


class UploadExcel(models.Model):
	file=models.FileField(upload_to='xls/',null=True)

class ActiveSem(models.Model):
    semister = models.CharField(max_length=20, null=True)
   
    
    def __str__(self):
        return self.semister




class Subject(models.Model):
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    unit = models.FloatField(default=0)
    prerequisite = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='prerequisite_for')

    def __str__(self):
        return f"{self.code} - {self.description}"

class Curriculum(models.Model):
	slug=models.SlugField(max_length=200,null=True)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	major=models.ForeignKey(Major, on_delete=models.CASCADE,null=True,blank=True)
	semister=models.CharField(max_length=20,null=True)
	year_level=models.ForeignKey(Year_level,on_delete=models.CASCADE,null=True)
	subjects=models.ManyToManyField(Subject,related_name='Curriculum_subjects')

	def __str__(self):
		return self.course.code +"-"+self.year_level.description



class Instructor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

		
from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()

class Student(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	student_id=models.CharField(max_length=50,null=True,unique=True)
	first_name=models.CharField(max_length=100, blank=True, null=True)
	middle_name=models.CharField(max_length=100,blank=True)
	ext_name=models.CharField(max_length=10,null=True, blank=True)
	last_name=models.CharField(max_length=100, blank=True, null=True)
	birth_date=models.DateTimeField(blank=True, null=True)
	address=models.CharField(max_length=200,null=True,blank =True)
	brgy=models.CharField(max_length=200, blank=True, null=True)
	street = models.CharField(max_length=200, blank=True, null=True)
	city=models.CharField(max_length=200, blank=True, null=True)
	province=models.CharField(max_length=200, blank=True, null=True)
	place_of_birth=models.CharField(max_length=200, blank=True, null=True)
	mobile_no=models.CharField(max_length=40, blank=True, null=True)
	guardian=models.CharField(max_length=200, blank=True, null=True)
	relationship=models.CharField(max_length=200, blank=True, null=True)
	guardian_address=models.CharField(max_length=200, blank=True, null=True)
	guardian_contact=models.CharField(max_length=200, blank=True, null=True)
	occupation=models.CharField(max_length=200, blank=True, null=True)
	religion=models.CharField(max_length=200, blank=True, null=True)
	zip_code=models.CharField(max_length=20, blank=True, null=True)
	date_created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="students")
	major=models.ForeignKey(Major,on_delete=models.CASCADE,null=True,blank=True,related_name="students")
	primary=models.CharField(max_length=200, blank=True, null=True)
	elementary=models.CharField(max_length=200, blank=True, null=True)
	highschool=models.CharField(max_length=200, blank=True, null=True)
	senior_highschool=models.CharField(max_length=200,null=True, blank= True)
	degree_completed=models.CharField(max_length=200,null=True,blank=True)
	degree_year_attended=models.CharField(max_length=8,null=True,blank=True)
	name_of_school=models.CharField(max_length=200,null=True,blank=True)
	primary_completed=models.CharField(max_length=8, blank=True, null=True)
	elementary_completed=models.CharField(max_length=8, blank=True, null=True)
	highschool_completed=models.CharField(max_length=8, blank=True, null=True)
	senior_highschool_completed=models.CharField(max_length=8,null=True, blank = True)
	civil_status=models.CharField(max_length=200, blank=True, null=True)
	nationality=models.CharField(max_length=200, blank=True, null=True)
	email_add=models.CharField(max_length=200, blank=True, null=True)
	lrn_num=models.CharField(max_length=200, blank=True, null=True)
	is_conditional = models.BooleanField(default=False,  blank=True, null=True)
	date_accepted=models.DateTimeField(null=True, blank=True)
	gender=models.CharField(max_length=20 , blank=True, null=True)


	def __str__(self):
		return str(self.last_name) + ","+ str(self.first_name) + "-"+  str(self.student_id) 

	class Meta:
           ordering = ['last_name']

    
           
class Room(models.Model):
	name=models.CharField(max_length=100)

	def __str__(self):
		return self.name



class DaySched(models.Model):
	day=models.CharField(max_length=20)
	number_of_days = models.IntegerField(default=1)


	def __str__(self):
		return self.day

class TimeSched(models.Model):
	time_start=models.TimeField(blank=True, null=True)
	duration_in_hour=models.FloatField(default=1)
	days = models.ForeignKey(DaySched,on_delete=models.PROTECT, null=True, blank=True)

	def __str__(self):
		return str(self.days) + ' - ' + str(self.time_start) +' - ' + str(self.duration_in_hour) + ' Hour/s'


class StudentProfile(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='profile')
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return f"Profile of {self.student.first_name} {self.student.last_name}"

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"





class EnrollbyStudent(models.Model):
	student=models.ForeignKey(Student,on_delete=models.PROTECT,related_name="enrollbyStudents")
	course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name="enrollbyStudents", null=True)
	enrollment_key=models.SlugField(null=True)
	major=models.ForeignKey(Major,on_delete=models.PROTECT,null=True,blank=True,related_name="enrollbyStudents")
	academic_year=models.ForeignKey(Academic_year,on_delete=models.PROTECT,related_name="enrollbyStudents")
	year_level=models.ForeignKey(Year_level,on_delete=models.PROTECT,null=True,related_name="enrollbyStudents")
	semister=models.CharField(max_length=20)
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	status=models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.student.last_name)+ "," + str(self.student.first_name)

	class Meta:
           ordering = ['major', 'year_level', 'student'] 

from django.db import models

from django.db import models
from datetime import datetime

from django.db import models
from datetime import datetime

class SubjectsLoaded(models.Model):
    enrolled_by_student = models.ForeignKey(EnrollbyStudent, on_delete=models.CASCADE, null=True, related_name="enroll_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, null=True)
    grade_status = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    midterm_grade = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    submit_status = models.CharField(max_length=100, null=True, blank=True)
    submission_time = models.DateTimeField(null=True, blank=True)
    academic_year = models.ForeignKey(Academic_year, on_delete=models.SET_NULL, null=True, blank=True)
    semister = models.ForeignKey(ActiveSem, on_delete=models.SET_NULL, null=True, blank=True)  # Ensure this is a ForeignKey


    def __str__(self):
        return self.subject.code






class GradeSubmitted(models.Model):
	intructor=models.ForeignKey(Instructor, on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	grade=models.CharField(max_length=50,null=True)



class IDandFullname(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
	student_id=models.CharField(max_length=50,null=True,unique=True)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	course=models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True) 
	subjects = models.ManyToManyField(Subject, related_name='teachers', null=True, blank=True)  
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True) 

	related_students = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
	added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='added_id_fillname', null=True, blank=True)
	status=models.CharField(max_length=100, null=True, blank =True)

	is_teacher = models.BooleanField(default=False)
	is_dean= models.BooleanField(default=False)
	is_student= models.BooleanField(default=False)

	def __str__(self):
		return self.first_name + " " + self.last_name
	






class AOSF(models.Model):
	athletic_fees = models.DecimalField(decimal_places = 2, max_digits = 20, default = 0.00)
	internet_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	cultural_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	guidance_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	handbook_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	laboratory_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default =0.00)
	computer_laboratory_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default =0.00)
	medical_and_dental_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	registration_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	school_id_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	entrance_exam = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	school_id_fees = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	development_fee = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	library_fee = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	tution_fee_ammount = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	insurance = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00)
	graduation_fee = models.DecimalField(decimal_places = 2,  max_digits = 20, default = 0.00,null=True,blank=True)

class InstructorLoadSubject(models.Model):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	time = models.ForeignKey(TimeSched, on_delete=models.CASCADE)
	semister = models.CharField(max_length=20)
	section = models.CharField(max_length=2,default='A')
	schedule_days = models.ForeignKey(DaySched, on_delete=models.CASCADE, null=True, blank =True)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True, blank =True)
	year_level=models.ForeignKey(Year_level,on_delete=models.CASCADE)
	academic_year=models.ForeignKey(Academic_year,on_delete=models.PROTECT, null=True, blank =True)
	is_lab = models.BooleanField(default=False, null=True)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank =True)



from django.utils import timezone
from django.db import models

class GradeSubmissionSchedule(models.Model):
	start_date = models.DateField()
	end_date = models.DateField()
	status = models.CharField(max_length=10, default='pending')
	active_semister = models.ForeignKey(
		'ActiveSem', on_delete=models.SET_NULL, null=True, related_name='schedules'
	)
	academic_year = models.ForeignKey(
		'Academic_year', on_delete=models.SET_NULL, null=True, related_name='schedules'
	)

	def update_status(self):
		today = timezone.now().date()
		if self.status == 'off':
			return
		if self.start_date <= today < self.end_date:
			self.status = 'active'
		elif today >= self.end_date:
			self.status = 'closed'
		else:
			self.status = 'pending'
		self.save() 






