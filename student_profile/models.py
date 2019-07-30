from django.db import models

# Create your models here.
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
	status=models.NullBooleanField(default=True)

	def __str__(self):
		return self.ay


class UploadExcel(models.Model):
	file=models.FileField(upload_to='xls/',null=True)



class Subject(models.Model):
	code=models.CharField(max_length=200)
	description=models.CharField(max_length=200)
	unit=models.FloatField(default=0)
	def __str__(self):
		return self.code + "-" + self.description

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
	first_name=models.CharField(max_length=100)
	middle_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	gender=models.CharField(max_length=20,blank=True)
	address=models.CharField(max_length=100,null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		return self.first_name + " "+ self.last_name


class Student(models.Model):
	student_id=models.CharField(max_length=50,null=True,unique=True)
	first_name=models.CharField(max_length=100)
	middle_name=models.CharField(max_length=100,blank=True)
	ext_name=models.CharField(max_length=10,null=True, blank=True)
	gender=models.CharField(max_length=20)
	last_name=models.CharField(max_length=100)
	birth_date=models.DateTimeField(null=True)
	address=models.CharField(max_length=200,null=True)
	city=models.CharField(max_length=200,null=True)
	province=models.CharField(max_length=200,null=True)
	place_of_birth=models.CharField(max_length=200,null=True)
	mobile_no=models.CharField(max_length=40,null=True)
	guardian=models.CharField(max_length=200,null=True)
	relationship=models.CharField(max_length=200,null=True)
	guardian_address=models.CharField(max_length=200,null=True)
	guardian_contact=models.CharField(max_length=200,null=True)
	occupation=models.CharField(max_length=200,null=True)
	religion=models.CharField(max_length=200,null=True)
	zip_code=models.CharField(max_length=20,null=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="students")
	major=models.ForeignKey(Major,on_delete=models.CASCADE,null=True,blank=True,related_name="students")
	primary=models.CharField(max_length=200,null=True)
	elementary=models.CharField(max_length=200,null=True)
	highschool=models.CharField(max_length=200,null=True)
	degree_completed=models.CharField(max_length=200,null=True,blank=True)
	degree_year_attended=models.CharField(max_length=8,null=True,blank=True)
	name_of_school=models.CharField(max_length=200,null=True,blank=True)
	primary_completed=models.CharField(max_length=8,null=True)
	elementary_completed=models.CharField(max_length=8,null=True)
	highschool_completed=models.CharField(max_length=8,null=True)
	civil_status=models.CharField(max_length=200,null=True)
	nationality=models.CharField(max_length=200,null=True)
	email_add=models.CharField(max_length=200,null=True)
	lrn_num=models.CharField(max_length=200,null=True)





	def __str__(self):
		return str(self.last_name) + ","+ str(self.first_name) + "-"+  str(self.student_id) 

	class Meta:
           ordering = ['last_name']

           
class Room(models.Model):
	name=models.CharField(max_length=100)

	def __str__(self):
		return self.name

class TimeSched(models.Model):
	time=models.CharField(max_length=50)

	def __str__(self):
		return self.time

class DaySched(models.Model):
	day=models.CharField(max_length=20)

	def __str__(self):
		return self.day





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

class SubjectsLoaded(models.Model):
	enrolled_by_student=models.ForeignKey(EnrollbyStudent,on_delete=models.CASCADE,null=True,related_name="enroll_subjects")
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
	instructor=models.ForeignKey(Instructor,on_delete=models.PROTECT,null=True)
	grade_status=models.CharField(max_length=100, null=True)
	grade=models.CharField(max_length=50,null=True)
	status=models.CharField(max_length=100, null=True)
	
	def __str__(self):
		return self.subject.code

	


class GradeSubmitted(models.Model):
	intructor=models.ForeignKey(Instructor, on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	grade=models.CharField(max_length=50,null=True)


class IDandFullname(models.Model):
	student_id=models.CharField(max_length=50,null=True,unique=True)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)

	def __str__(self):
		return self.first_name + " " + self.last_name

