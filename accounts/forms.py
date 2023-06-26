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



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")



class UserLoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)
	username.widget.attrs.update({'class':'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',})
	password.widget.attrs.update({'class':'form-control w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500',})

	def clean(self,*args,**kwargs):
		print('ni abot')
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
		'is_staff'
		]


		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control validate'}),
		    'first_name': forms.TextInput(attrs={'class':'form-control validate',}),
		    'last_name': forms.TextInput(attrs={'class':'form-control validate'}),
		    'email': forms.EmailInput(attrs={'class':'form-control'}),
		    'is_superuser': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_active': forms.CheckboxInput(attrs={'class':'form-control'}),
		    'is_staff': forms.CheckboxInput(attrs={'class':'form-control'}),
		  
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
			'email'
		]

		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control validate'}),
			'student_id':forms.TextInput(attrs={'class':'form-control validate'}),
			'first_name':forms.TextInput(attrs={'class':'form-control validate'}),
			'last_name':forms.TextInput(attrs={'class':'form-control validate'}),
			'email':forms.TextInput(attrs={'class':'form-control validate'}),
		}
	def clean_student_id(self):
		student_id=self.cleaned_data['student_id']
		first_name=self.data.get('first_name')
		last_name=self.data.get('last_name')

		print(last_name)
		print(first_name)

		qs_student_id=CustomUser.objects.filter(student_id=student_id)
		id_owner=IDandFullname.objects.filter(student_id=student_id.strip(),first_name__iexact=first_name.strip(),last_name__iexact=last_name.strip())

			

		print(id_owner)
		if student_id:
			if not id_owner.exists():
				raise forms.ValidationError('ID number must match your name, go to registrar to fix')

			if qs_student_id.exists():
				print('already exists')
				raise forms.ValidationError('User Id already exists')
			else:
				return student_id






		






