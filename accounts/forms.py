from django import forms
from django.contrib.auth import (	
	authenticate,
	get_user_model,
	login,
	logout,
)


from .models import CustomUser
from student_profile.models import IDandFullname
User=get_user_model()
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
import sys




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'student_id', 'teacher_id')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'student_id', 'teacher_id')



class UserLoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)
	username.widget.attrs.update({'class':'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',})
	password.widget.attrs.update({'class':'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',})

	def clean(self,*args,**kwargs):

		username=self.cleaned_data.get('username')
		password=self.cleaned_data.get('password')
		
		if username and password:
			user=authenticate(username=username,password=password)
			if not user:
				raise forms.ValidationError('this user does not exist')

			if not user.check_password(password):
				raise forms.ValidationError('Incorrect Password')

			if not user.is_active:
				raise forms.ValidationError('this user is no longer active')
		return super(UserLoginForm,self).clean(*args,**kwargs)


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=[
		'username',
		'first_name',
		'last_name',
		'email',
		'is_superuser',
		'is_active',
		'is_staff',
		'is_dean',
		'is_teacher',
		'is_student',
		'is_admin'
		]


		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control validate'}),
		    'first_name': forms.TextInput(attrs={'class':'form-control validate',}),
		    'last_name': forms.TextInput(attrs={'class':'form-control validate'}),
		    'email': forms.EmailInput(attrs={'class':'form-control'}),
		    'is_superuser': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_active': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_staff': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_dean': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_teacher': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_student': forms.CheckboxInput(attrs={'class':'form-control'}),
			'is_admin': forms.CheckboxInput(attrs={'class':'form-control'}),
		}

	def clean_is_superuser(self,request):
		username=self.cleaned_data.get('username')
		is_superuser=self.cleaned_data.get('is_superuser')
		if request.user==username:
			raise forms.ValidationError('you cant change the superuser')

		return is_superuser 





		

class UserRegisterForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	password.widget.attrs.update({'class':'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',})
	class Meta:
		model=CustomUser
		fields=[
			'username',
			'password',
			'student_id',
			'first_name',
			'last_name',
			'email',
			'is_dean',
			'is_teacher',
			'is_student',
			'is_admin'
		]

		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control validate'}),
			'student_id':forms.TextInput(attrs={'class':'form-control validate'}),
			'first_name':forms.TextInput(attrs={'class':'form-control validate'}),
			'last_name':forms.TextInput(attrs={'class':'form-control validate'}),
			'email':forms.TextInput(attrs={'class':'form-control validate'}),
			'is_dean': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_teacher': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_student': forms.CheckboxInput(attrs={'class':'form-control'}),
			'is_admin': forms.CheckboxInput(attrs={'class':'form-control'}),
		}
	def clean_student_id(self):
		student_id=self.cleaned_data['student_id']
		try:
			first_name=self.data.get('first_name')
			last_name=self.data.get('last_name')
			qs_student_id=CustomUser.objects.filter(student_id=student_id)
			id_owner=IDandFullname.objects.filter(student_id=student_id.strip(),first_name__iexact=first_name.strip(),last_name__iexact=last_name.strip())
			
				
			if student_id:
				if not id_owner.exists():
					raise forms.ValidationError(' number must match your name, go to registrar to fix')

				if qs_student_id.exists():
					raise forms.ValidationError('User Id already exists')
				else:
					return student_id
		except UnicodeEncodeError:
			return student_id





# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',
#     }))
    
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username', 'password', 'student_id', 'first_name', 'last_name', 
#             'email', 'is_dean', 'is_teacher', 'is_student', 'is_admin'
#         ]
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control validate'}),
#             'student_id': forms.TextInput(attrs={'class': 'form-control validate'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control validate'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control validate'}),
#             'email': forms.TextInput(attrs={'class': 'form-control validate'}),
#             'is_dean': forms.CheckboxInput(attrs={'class': 'form-control'}),
#             'is_teacher': forms.CheckboxInput(attrs={'class': 'form-control'}),
#             'is_student': forms.CheckboxInput(attrs={'class': 'form-control'}),
#             'is_admin': forms.CheckboxInput(attrs={'class': 'form-control'}),
#         }

#     def clean_student_id(self):
#         student_id = self.cleaned_data.get('student_id', '').strip()
#         first_name = self.cleaned_data.get('first_name', '').strip()
#         last_name = self.cleaned_data.get('last_name', '').strip()
#         is_student = self.cleaned_data.get('is_student', False)
#         is_teacher = self.cleaned_data.get('is_teacher', False)
#         is_admin = self.cleaned_data.get('is_admin', False)

#         # Check if student ID matches first and last name in IDandFullname
#         id_owner = IDandFullname.objects.filter(
#             student_id=student_id, 
#             first_name__iexact=first_name, 
#             last_name__iexact=last_name
#         )
#         if not id_owner.exists():
#             raise forms.ValidationError(' ID must match your name. Please contact the registrar.')

#         # Check if the ID already exists in the system for a different role
#         existing_user = CustomUser.objects.filter(student_id=student_id).first()

#         if existing_user:
#             # Handle case if a student is using a teacher's ID or vice versa
#             if is_student and existing_user.is_teacher:
#                 raise forms.ValidationError(f'This ID belongs to a teacher. Please use your correct student ID.')
#             if is_student and existing_user.is_admin:
#                 raise forms.ValidationError(f'This ID is assigned to an admin. Please use your correct student ID.')
#             if is_teacher and existing_user.is_student:
#                 raise forms.ValidationError(f'This ID belongs to a student. Please use the correct teacher ID.')
#             if is_teacher and existing_user.is_admin:
#                 raise forms.ValidationError(f'This ID is assigned to an admin. Please use your correct teacher ID.')

#             # Add more conditions if needed for other roles
#             raise forms.ValidationError('User ID already exists with a different role.')

#         return student_id




		



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control validate'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control validate'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control validate'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser




from django import forms
from student_profile.models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'ext_name', 'gender', 'last_name', 'birth_date', 
            'address', 'brgy', 'street', 'city', 'province', 'place_of_birth', 'mobile_no',
            'guardian', 'relationship', 'guardian_address', 'guardian_contact', 'occupation', 
            'religion', 'zip_code', 'course', 'major', 'primary', 'elementary', 'highschool', 
            'senior_highschool', 'degree_completed', 'degree_year_attended', 'name_of_school', 
            'primary_completed', 'elementary_completed', 'highschool_completed', 
            'senior_highschool_completed', 'civil_status', 'nationality', 'email_add', 
            'lrn_num', 'is_conditional', 'date_accepted'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'date_accepted': forms.DateInput(attrs={'type': 'date'}),
        }



from django import forms
from student_profile.models import Instructor

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'address', 'contact']
