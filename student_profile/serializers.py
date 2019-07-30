from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import IDandFullname, EnrollbyStudent,Student,Subject,Course,Major,Year_level,Academic_year,SubjectsLoaded,Instructor,Curriculum

class DuplicateData(APIException):
    status_code = 406 
    default_detail = 'Data already Exists.'
    default_code = 'duplicate_data'

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = '__all__'

	def create(self,validated_data):
		print(validated_data.get('code', None))

		query=Subject.objects.filter(code=validated_data.get('code', None),description=validated_data.get('description', None)).count()
		print(query)
		if query == 0:
			return Subject.objects.create(**validated_data)
		raise  DuplicateData()


class IDandFullnameSerializer(serializers.ModelSerializer):
	class Meta:
		model = IDandFullname
		fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instructor
		fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Major
		fields = '__all__'

class Year_levelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Year_level
		fields = '__all__'

class Academic_yearSerializer(serializers.ModelSerializer):

	class Meta:
		model = Academic_year
		fields = '__all__'


class SubjectsLoadedSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	class Meta:
		model = SubjectsLoaded
		fields = ["id","grade_status","grade","status","enrolled_by_student","subject","instructor"]

class CurriculumSerializer(serializers.ModelSerializer):
	# subjects=SubjectSerializer(many=True)
	class Meta:
		model = Curriculum
		fields = '__all__'

class CurriculumsSerializer(serializers.ModelSerializer):
	subjects=SubjectSerializer(many=True)
	class Meta:
		model = Curriculum
		fields = '__all__'


class EnrollStudSerlizer(serializers.ModelSerializer):
	enroll_subjects=SubjectsLoadedSerializer(many=True)
	
	class Meta:
		model = EnrollbyStudent
		fields=['id','student','course','major','academic_year','year_level','semister','status','enroll_subjects']
	
	def create(self, validated_data):
		enroll_subjects = validated_data.pop('enroll_subjects')
		#query=EnrollbyStudent.objects.filter()
		enroll = EnrollbyStudent.objects.create(**validated_data)
		for enroll_data in enroll_subjects:
			SubjectsLoaded.objects.create(enrolled_by_student=enroll, **enroll_data)
		return enroll

	def update(self, instance, validated_data):
		print(instance)

		instance.student = validated_data.get('student', instance.student)
		instance.course = validated_data.get('course', instance.course)
		instance.major = validated_data.get('major', instance.major)
		instance.year_level = validated_data.get('year_level', instance.year_level)
		instance.semister = validated_data.get('semister', instance.semister)
		instance.status = validated_data.get('status', instance.status)
		instance.save()

		enroll_subjects = validated_data.get('enroll_subjects')

		for item in enroll_subjects:
			print(item)
			item_id = item.get('id',None)
			print(item_id)
			if item_id:
				inv_item = SubjectsLoaded.objects.get(pk=item_id)
				inv_item.subject = item.get('subject', inv_item.subject)
				inv_item.status = item.get('status', inv_item.status)
				inv_item.save()
			else:
				SubjectsLoaded.objects.create(enrolled_by_student=instance, **item)

		return instance



class StudentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Student
		fields = '__all__'





class StudentEnrollSerializer(serializers.ModelSerializer):
	student=StudentSerializer()
	course=CourseSerializer()
	major=MajorSerializer()
	academic_year=Academic_yearSerializer()
	year_level=Year_levelSerializer()
	
	class Meta:
		model = EnrollbyStudent
		fields=['id','student','course','major','academic_year','year_level','semister','status']


class SubjectEnrollSerializer(serializers.ModelSerializer):
	enrolled_by_student=StudentEnrollSerializer()
	subject=SubjectSerializer()
	instructor=InstructorSerializer()
	class Meta:
		model=SubjectsLoaded
		fields = ['id','enrolled_by_student','grade','subject','instructor','grade_status','status',]







	




