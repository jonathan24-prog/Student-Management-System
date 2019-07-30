from django import forms
from django.contrib.auth import (	
	authenticate,
	get_user_model,
	login,
	logout,
)



User=get_user_model()



class UserLoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)
	username.widget.attrs.update({'class':'form-control',})
	password.widget.attrs.update({'class':'form-control',})

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
	password.widget.attrs.update({'class':'form-control',})
	class Meta:
		model=User
		fields=[
			'username',
			'password'
		]

		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control validate'}),
		   
		}





		

	




