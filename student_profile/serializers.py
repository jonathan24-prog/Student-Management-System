from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from accounts.models import CustomUser
from .models import DaySched, TimeSched, Room,InstructorLoadSubject, AOSF, IDandFullname,StudentProfile, EnrollbyStudent,Announcement,Student,Subject,Course,Major,Year_level,Academic_year,SubjectsLoaded,Instructor,Curriculum, ActiveSem

































class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'start_date', 'end_date', 'created_by', 'created_at', 'updated_at']

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class DuplicateData(APIException):
    status_code = 406 
    default_detail = 'Data already Exists.'
    default_code = 'duplicate_data'

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = '__all__'

	def create(self,validated_data):
		query=Subject.objects.filter(code=validated_data.get('code', None),description=validated_data.get('description', None)).count()

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
        fields = ["id", "grade_status", "grade", "midterm_grade", "status", "enrolled_by_student", "subject", "instructor", "submit_status"]

from rest_framework import serializers
from .models import SubjectsLoaded

from django.db.models import Count

class SubjectsLoadedSerializers(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    forwarded_subject_count = serializers.SerializerMethodField()  # Forwarded subjects count
    total_subject_count = serializers.SerializerMethodField()  # Total subjects assigned to the instructor
    subject_name = serializers.CharField(source='subject.description', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    semister = serializers.CharField(source='semister.semister', read_only=True)
    academic_year = serializers.CharField(source='academic_year.ay', read_only=True)
    submission_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = SubjectsLoaded
        fields = [
            'id', 'subject_name', 'subject_code', 'semister', 'academic_year', 
            'instructor_name', 'submit_status', 'grade', 'midterm_grade', 'status', 
            'submission_time', 'forwarded_subject_count', 'total_subject_count'
        ]

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.first_name} {obj.instructor.last_name}"
        return "No instructor"

    def get_forwarded_subject_count(self, obj):
        instructor = obj.instructor
        if instructor:
            # Get all subjects assigned to this instructor in IDandFullname
            assigned_subjects = IDandFullname.objects.filter(
                instructor=instructor
            ).values_list('subjects__id', flat=True).distinct()

            # Count distinct subjects with any non-empty submit_status
            forwarded_count = SubjectsLoaded.objects.filter(
                instructor=instructor,
                submit_status__isnull=False,  # Ensure the submit_status has a value
                subject__id__in=assigned_subjects  # Only include subjects assigned to this instructor
            ).values('subject').distinct().count()

            return forwarded_count
        return 0

    def get_total_subject_count(self, obj):
        instructor = obj.instructor
        if instructor:
            id_and_fullname = IDandFullname.objects.filter(instructor=instructor).first()
            if id_and_fullname:
                related_subjects = id_and_fullname.subjects.all()
                total_subjects = related_subjects.count()
                return total_subjects
        return 0








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
		instance.student = validated_data.get('student', instance.student)
		instance.course = validated_data.get('course', instance.course)
		instance.major = validated_data.get('major', instance.major)
		instance.year_level = validated_data.get('year_level', instance.year_level)
		instance.semister = validated_data.get('semister', instance.semister)
		instance.status = validated_data.get('status', instance.status)
		instance.save()

		enroll_subjects = validated_data.get('enroll_subjects')

		for item in enroll_subjects:
			item_id = item.get('id',None)
			if item_id:
				inv_item = SubjectsLoaded.objects.get(pk=item_id)
				inv_item.subject = item.get('subject', inv_item.subject)
				inv_item.status = item.get('status', inv_item.status)
				inv_item.save()
			else:
				SubjectsLoaded.objects.create(enrolled_by_student=instance, **item)

		return instance



class StudentSerializer(serializers.ModelSerializer):
	birth_date=serializers.DateTimeField(format="%m-%d-%Y", input_formats=['%m-%d-%Y', 'iso-8601'])
	class Meta:
		model = Student
		fields = '__all__'

class AOSFSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = AOSF
		fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Room
		fields = '__all__'



class DaySchedSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = DaySched
		fields = '__all__'

class TimeSchedSerializer(serializers.ModelSerializer):
	days=DaySchedSerializer()
	class Meta:
		model = TimeSched
		fields = '__all__'

class InstructorLoadSubjectSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = InstructorLoadSubject
		fields = '__all__'

class InstructorLoadSubjectWithObjectSerializer(serializers.ModelSerializer):
	course=CourseSerializer()
	major=MajorSerializer()
	academic_year=Academic_yearSerializer()
	year_level=Year_levelSerializer()
	room = RoomSerializer()
	time = TimeSchedSerializer()
	schedule_days = DaySchedSerializer()
	instructor = InstructorSerializer()
	subject = SubjectSerializer()
	class Meta:
		model = InstructorLoadSubject
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



class StudentsEnrollSerializer(serializers.ModelSerializer):
	student=StudentSerializer()
	course=CourseSerializer()
	major=MajorSerializer()
	academic_year=Academic_yearSerializer()
	year_level=Year_levelSerializer()
	enroll_subjects=SubjectsLoadedSerializer(many=True)
	enroll_count = serializers.SerializerMethodField()

	def get_enroll_count(self, obj):

		enroll_by_students = EnrollbyStudent.objects.filter(student=obj.student, status= 'approved')
		return len(enroll_by_students)
	
	
	class Meta:
		model = EnrollbyStudent
		fields=['id','student','course','major','academic_year','year_level','semister','status','enroll_subjects','enroll_count']


class SubjectEnrollSerializer(serializers.ModelSerializer):
    enrolled_by_student = StudentEnrollSerializer()
    subject = SubjectSerializer()
    instructor = InstructorSerializer()

    class Meta:
        model = SubjectsLoaded
        fields = ['id', 'enrolled_by_student', 'grade', 'midterm_grade', 'subject', 'instructor', 'grade_status', 'status', 'submit_status']


class ActiveSemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ActiveSem
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = CustomUser
		fields = '__all__'










	




