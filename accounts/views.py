from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import UserLoginForm,UserRegisterForm,UserUpdateForm


from django.contrib.auth import (
	
	authenticate,
	get_user_model,
	login,
	logout,
)
User=get_user_model()

# Register your models here.

def displayAccount(request,pk):
	
	user=get_object_or_404(User,pk=pk)
	if request.method=="POST":
		if request.user.is_superuser:
			form=UserUpdateForm(request.POST,instance=user)
			if form.is_valid():
				form.save()
				return redirect('ViewAccounts')
			return HttpResponse('invalid entry')
		return HttpResponse('your not autorize to update')

	form=UserUpdateForm(instance=user)
	return render(request,'student_profile/account.html',{'form':form})

def login_view(request):
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user_log=get_object_or_404(User,username=username)
		
		user=authenticate(username=username,password=password)
		login(request,user)
		print(request.user.is_authenticated)
		return redirect('home')
		

	return render(request,'student_profile/login.html',{'form':form})


def register_view(request):
	title="Register"
	form=UserRegisterForm(request.POST or None)
	if form.is_valid():
	
		user=form.save(commit=False)
		password=form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		
		login(request,user)
		return redirect('home')	
	context={'form':form,'title':title}
	return render(request,'student_profile/registerForm.html',context)

def logout_view(request):
	logout(request)
	return redirect('login')

