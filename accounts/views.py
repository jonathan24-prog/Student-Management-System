from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import CustomPasswordChangeForm, UserLoginForm,UserRegisterForm,UserUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.views.decorators.http import require_POST

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

# def login_view(request):
# 	form=UserLoginForm(request.POST or None)
# 	if form.is_valid():
# 		username=form.cleaned_data.get('username')
# 		password=form.cleaned_data.get('password')
# 		user_log=get_object_or_404(User,username=username)
		
# 		user=authenticate(username=username,password=password)
# 		login(request,user)
# 		return redirect('announcements')
		

# 	return render(request,'student_profile/login.html',{'form':form})





# def login_view(request):
# 	form=UserLoginForm(request.POST or None)
# 	if form.is_valid():
# 		username=form.cleaned_data.get('username')
# 		password=form.cleaned_data.get('password')
# 		user_log=get_object_or_404(User,username=username)
		
# 		user=authenticate(username=username,password=password)
# 		login(request,user)
# 		return redirect('home')
		

# 	return render(request,'student_profile/login.html',{'form':form})








def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Determine the user's role and redirect accordingly
            if user.is_dean:
                return redirect('home')  
            elif user.is_teacher:
                return redirect('home')  
            elif user.is_student:
                return redirect('home')  
            elif user.is_admin:
                return redirect('home')  
            else:
                return redirect('home') 

    return render(request, 'student_profile/login.html', {'form': form})






from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import CustomUser
from django.contrib.auth import login



from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
from student_profile.models import IDandFullname

def register_view(request):
    title = "Register"
    user_type = request.session.get('user_type', 'Guest')  # Retrieve user type from session (can be set from frontend)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)

            # Check if the student's ID and first name match an existing entry in IDandFullname
            try:
                id_and_name_match = IDandFullname.objects.get(
                    student_id=user.student_id,
                    first_name=user.first_name
                )
            except IDandFullname.DoesNotExist:
                # If no match is found, return an error or handle it appropriately
                form.add_error(None, "No matching student ID and first name found. Please check your information.")
                return render(request, 'student_profile/registerForm.html', {'form': form, 'title': title, 'user_type': user_type})

            # Set user type based on the matched IDandFullname entry
            if id_and_name_match.is_dean:
                user.is_dean = True
            elif id_and_name_match.is_teacher:
                user.is_teacher = True
            elif id_and_name_match.is_student:
                user.is_student = True
            else:
                # Handle cases where no role is found
                form.add_error(None, "User role not found.")
                return render(request, 'student_profile/registerForm.html', {'form': form, 'title': title, 'user_type': user_type})

            # Save the user
            user.save()

            # Log the user in
            login(request, user)

            # Redirect to the home page
            return redirect('home')

    else:
        form = UserRegisterForm()

    context = {'form': form, 'title': title, 'user_type': user_type}
    return render(request, 'student_profile/registerForm.html', context)







def select_user_type_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.session['user_type'] = user_type  # Store user type in session
        return redirect('register')  # Redirect to register view
    
    return render(request, 'student_profile/selectUserType.html')






# def register_view(request):
# 	title="Register"
# 	form=UserRegisterForm(request.POST or None)
# 	if form.is_valid():
	
# 		user=form.save(commit=False)
# 		password=form.cleaned_data.get('password')
# 		user.set_password(password)
# 		user.save()
		
# 		login(request,user)
# 		return redirect('home')	
# 	context={'form':form,'title':title}
# 	return render(request,'student_profile/registerForm.html',context)

def logout_view(request):
	logout(request)
	return redirect('login')






from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, InstructorProfileForm
from student_profile.models import Instructor


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, StudentProfileForm
from student_profile.models import Student

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, StudentProfileForm
from student_profile.models import Student,Instructor

def view_profile(request):
    user = request.user  # Get the logged-in user

    if not user.is_authenticated:
        return redirect('login')  # Redirect if the user is not logged in

    try:
        student_profile = Student.objects.get(user=user)  # Get the student profile for the logged-in user
    except Student.DoesNotExist:
        student_profile = None  # In case the student profile doesn't exist

    if request.method == "POST":
        # Initialize both forms (user profile and student profile)
        profile_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        student_form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)

        if profile_form.is_valid():
            # Save the user profile form (only the changed fields)
            profile_form.save()

        if student_form.is_valid():
            # Save the student profile form (only the changed fields)
            student_form.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect after successful update
        else:
            messages.error(request, 'There were errors with your submission.')

    else:
        profile_form = UserUpdateForm(instance=user)
        student_form = StudentProfileForm(instance=student_profile)

    context = {
        'profile_form': profile_form,
        'student_form': student_form,
    }

    return render(request, 'student_profile/account_profile.html', context)








from django.shortcuts import render, redirect
from django.contrib import messages


def view_instructor(request):
    user = request.user  # Get the logged-in user

    if not user.is_authenticated:
        return redirect('login')  # Redirect if the user is not logged in

    try:
        instructor_profile = Instructor.objects.get(user=user)  # Get the instructor profile for the logged-in user
    except Instructor.DoesNotExist:
        instructor_profile = None  # If the profile doesn't exist, initialize it

    if request.method == "POST":
        # Initialize both forms, but assign the user to the instructor form
        profile_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        instructor_form = InstructorProfileForm(request.POST, request.FILES, instance=instructor_profile)

        # Ensure the user is set in the instructor form
        if instructor_form.is_valid():
            # If the instructor form is new (None), create it with the user
            if not instructor_profile:
                instructor_form.instance.user = user

            # Save both forms
            profile_form.save()
            instructor_form.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profiles')  # Redirect to the same page
        else:
            messages.error(request, 'There were errors with your submission.')

    else:
        profile_form = UserUpdateForm(instance=user)
        instructor_form = InstructorProfileForm(instance=instructor_profile)

    context = {
        'profile_form': profile_form,
        'instructor_form': instructor_form,
    }

    return render(request, 'student_profile/account_instruct.html', context)

