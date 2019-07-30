from .models import Student,EnrollbyStudent,IDandFullname, SubjectsLoaded,Curriculum,Subject,UploadExcel,IDandFullname
from django import forms
from django.db.models import Q



class IDsNameForm(forms.ModelForm):
    class Meta:
        model=IDandFullname
        fields=['student_id','first_name','last_name']
        widgets={
                'student_id':forms.TextInput(attrs={'class':'form-control form-control validate'}),
                'first_name':forms.TextInput(attrs={'class':'form-control form-control validate'}),
                'last_name':forms.TextInput(attrs={'class':'form-control form-control validate'}),

                }





class UploadExcelForm(forms.ModelForm):
    class Meta:
        model=UploadExcel
        fields=['file',]
        widgets={
                'file':forms.FileInput(attrs={'class':'form-control form-control-sm validate', 'accept':'.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'}),
                }

class CurriculumForm(forms.ModelForm):
    class Meta:
        model=Curriculum
        fields=['course','major','subjects','semister','year_level']
        widgets={

                'course':forms.Select(attrs={'class':'form-control form-control validate'}),
                'year_level':forms.Select(attrs={'class':'form-control form-control validate'}),
                'semister':forms.Select(attrs={'class':'form-control form-control validate'}),
                'major':forms.Select(attrs={'class':'form-control form-control validate'}),
                'subjects':forms.CheckboxSelectMultiple(attrs={'class':'form-check-input validate','type':"checkbox"}),
                }

    def __init__(self,*args,**kwargs):
        super(CurriculumForm, self).__init__(*args, **kwargs)
        self.fields['year_level'].empty_label = "Year level"
        self.fields['year_level'].widget.choices = self.fields['year_level'].choices
        self.fields['course'].empty_label = "Course"
        self.fields['course'].widget.choices = self.fields['course'].choices
        self.fields['major'].empty_label = "Major"
        self.fields['major'].widget.choices = self.fields['major'].choices
        self.fields['semister'].empty_label = "Semester"
        self.fields['semister'].widget.choices = [('','Select a semester'),('1st','First Semester'),('2nd','Second Semester'),('summer','Summer Term')]



class SubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields=['code','description','unit']

        widgets={
                'code':forms.TextInput(attrs={'class':'form-control form-control validate'}),
                'description':forms.TextInput(attrs={'class':'form-control form-control validate'}),
                'unit':forms.NumberInput(attrs={'class':'form-control form-control validate'}),
                }


class SubjectLoadForm(forms.ModelForm):
    class Meta:
        model=SubjectsLoaded
        fields=['subject']
        widgets={
               'subject':forms.Select(attrs={'class':'form-control search-select form-control validate'}),
                           }
    def __init__(self,*args,**kwargs):
        super(SubjectLoadForm, self).__init__(*args, **kwargs)

        self.fields['subject'].empty_label = "Subject"
        self.fields['subject'].widget.choices = self.fields['subject'].choices


class EnrollForm(forms.ModelForm):
    class Meta:
        model=EnrollbyStudent
        fields=['course','major','academic_year','year_level','semister',]
        widgets={
               'course':forms.Select(attrs={'class':'form-control form-control'}),
               'major':forms.Select(attrs={'class':'form-control form-control validate'}),
               'academic_year':forms.Select(attrs={'class':'form-control form-control validate'}),
               'year_level':forms.Select(attrs={'class':'form-control form-control validate'}),
               'semister':forms.Select(attrs={'class':'form-control form-control validate'}),
        }
    def __init__(self,*args,**kwargs):
        super(EnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].empty_label = "Select a Course"
        self.fields['course'].widget.choices = self.fields['course'].choices
        self.fields['course'].empty_label = "Select a Course"
        self.fields['course'].widget.choices = self.fields['course'].choices
        self.fields['major'].empty_label = "Select a major"
        self.fields['major'].widget.choices = self.fields['major'].choices
        self.fields['academic_year'].empty_label = "Select a academic year"
        self.fields['academic_year'].widget.choices = self.fields['academic_year'].choices
        self.fields['year_level'].empty_label = "Select a year"
        self.fields['year_level'].widget.choices = self.fields['year_level'].choices
        self.fields['semister'].empty_label = "Select a semister"
        self.fields['semister'].widget.choices = [('','Select a semester'),('1st','First Semester'),('2nd','Second Semester'),('summer','Summer Term')]

class StudentForm(forms.ModelForm):
    first_name=forms.CharField()
    first_name.widget.attrs.update({'class':'form-control','placeholder':'first name'})
  
    class Meta:
        model=Student
        fields=('student_id','first_name','middle_name','birth_date',
            'address','city','province','zip_code','last_name','gender',
            'address','course','major','place_of_birth','mobile_no','guardian',
            'relationship','guardian_address','guardian_contact','occupation',
            'religion','primary','elementary','highschool','degree_completed',
            'degree_year_attended','name_of_school','primary_completed','elementary_completed',
            'highschool_completed','civil_status','nationality','email_add','ext_name','lrn_num')

        widgets={
                'student_id':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'student id'}),
                'gender':forms.Select(attrs={'class':'form-control form-control-sm validate','placeholder':'gender'}),
                'first_name':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'first name'}),
                'middle_name':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'middle name'}),
                'last_name':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'last name'}),
                'ext_name':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'ext. name e.g JR/SR'}),
                'address':forms.TextInput(attrs={'class':'form-control form-control-sm validate' ,'placeholder':'street address, barangay'}),
                'city':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'city/municipality'}),
                'province':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'province'}),
                'zip_code':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'zip code'}),
                'place_of_birth':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'birth place'}),
                'birth_date':forms.DateInput(attrs={'type':'date','class':'form-control form-control-sm datepicker','placeholder':'select a date'}),
                'course': forms.Select(attrs={'class':'form-control form-control-sm validate'}),
                'major': forms.Select(attrs={'class':'form-control form-control-sm validate'}),
                'mobile_no':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'mobile number'}),
                'guardian':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'guardian'}),
                'relationship':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'relationship'}),
                'guardian_address':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'parents/guardians address'}),
                'occupation':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'occupation'}),
                'religion':forms.TextInput(attrs={'class':'form-control form--sm validate','placeholder':'religion'}),
                'primary':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'primary'}),
                'elementary':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'elementary'}),
                'highschool':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'highschool'}),
                'degree_completed':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'degree completed'}),
                'degree_year_attended':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'year attended'}),
                'name_of_school':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'name of school'}),
                'primary_completed':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'year completed'}),
                'elementary_completed':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'year completed'}),
                'highschool_completed':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'year completed'}),
                'civil_status':forms.Select(attrs={'class':'form-control form-control-sm validate','placeholder':'civil status'}),
                'nationality':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'nationality'}),
                'email_add':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'email address'}),
                'guardian_contact':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'mobile number'}),
                'lrn_num':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'lrn number'}),



            }

    def clean_student_id(self):
        student_id=self.cleaned_data['student_id']
        first_name=self.data.get('first_name')
        last_name=self.data.get('last_name')

        print(last_name)
        print(first_name)
   
        qs_student_id=Student.objects.filter(student_id=student_id)
    
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


    def __init__(self,*args,**kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['course'].empty_label = "Select a Course"
        self.fields['course'].widget.choices = self.fields['course'].choices
        self.fields['major'].empty_label = "Select a Major"
        self.fields['major'].widget.choices = self.fields['major'].choices

        self.fields['gender'].widget.choices = [('','Select Gender'),('Male','Male'),('Female','Female')]
        self.fields['civil_status'].widget.choices = [('','Select Civil Status'),('Single','Single'),('Married','Married')]




class StudentFormUpdate(forms.ModelForm):
    first_name=forms.CharField()
    first_name.widget.attrs.update({'class':'form-control','placeholder':'first name'})
  
    class Meta:
        model=Student
        fields=('student_id','first_name','middle_name','birth_date',
            'address','city','province','zip_code','last_name','gender',
            'address','course','major','place_of_birth','mobile_no','guardian',
            'relationship','guardian_address','guardian_contact','occupation',
            'religion','primary','elementary','highschool','degree_completed',
            'degree_year_attended','name_of_school','primary_completed','elementary_completed',
            'highschool_completed','civil_status','nationality','email_add','ext_name','lrn_num')

        widgets={
                'student_id':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'student id'}),
                'gender':forms.Select(attrs={'class':'form-control form-control validate','placeholder':'gender'}),
                'first_name':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'first name'}),
                'middle_name':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'middle name'}),
                'last_name':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'last name'}),
                'ext_name':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'ext. name e.g JR/SR'}),
                'address':forms.TextInput(attrs={'class':'form-control form-control validate' ,'placeholder':'street address, barangay'}),
                'city':forms.TextInput(attrs={'class':'form-control form-control-sm validate','placeholder':'city/municipality'}),
                'province':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'province'}),
                'zip_code':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'zip code'}),
                'place_of_birth':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'birth place'}),
                'birth_date':forms.DateInput(attrs={'type':'date','class':'form-control datepicker','placeholder':'select a date'}),
                'course': forms.Select(attrs={'class':'form-control form-control validate'}),
                'major': forms.Select(attrs={'class':'form-control form-control validate'}),
                'mobile_no':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'mobile number'}),
                'guardian':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'guardian'}),
                'relationship':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'relationship'}),
                'guardian_address':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'parents/guardians address'}),
                'occupation':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'occupation'}),
                'religion':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'religion'}),
                'primary':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'primary'}),
                'elementary':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'elementary'}),
                'highschool':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'highschool'}),
                'degree_completed':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'degree completed'}),
                'degree_year_attended':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'year attended'}),
                'name_of_school':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'name of school'}),
                'primary_completed':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'year completed'}),
                'elementary_completed':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'year completed'}),
                'highschool_completed':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'year completed'}),
                'civil_status':forms.Select(attrs={'class':'form-control form-control validate','placeholder':'civil status'}),
                'nationality':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'nationality'}),
                'email_add':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'email address'}),
                'guardian_contact':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'mobile number'}),
                'lrn_num':forms.TextInput(attrs={'class':'form-control form-control validate','placeholder':'lrn number'}),



            }

    # def clean_student_id(self):
    #     student_id=self.cleaned_data['student_id']
    #     first_name=self.data.get('first_name')
    #     last_name=self.data.get('last_name')

    #     print(last_name)
    #     print(first_name)
   
    #     qs_student_id=Student.objects.filter(student_id=student_id)
    
    #     id_owner=IDandFullname.objects.filter(student_id=student_id,first_name__iexact=first_name,last_name__iexact=last_name)
     
          

        # print(id_owner)
        # if student_id:
        #     if not id_owner.exists():
        #         raise forms.ValidationError('ID number must match your name, go to registrar to fix')


        #     if qs_student_id.exists():
        #         print('already exists')
        #         raise forms.ValidationError('User Id already exists')
        #     else:
        #         return student_id


    def __init__(self,*args,**kwargs):
        super(StudentFormUpdate, self).__init__(*args, **kwargs)

        self.fields['course'].empty_label = "Select a Course"
        self.fields['course'].widget.choices = self.fields['course'].choices
        self.fields['major'].empty_label = "Select a Major"
        self.fields['major'].widget.choices = self.fields['major'].choices

        self.fields['gender'].widget.choices = [('','Select Gender'),('Male','Male'),('Female','Female')]
        self.fields['civil_status'].widget.choices = [('','Select Civil Status'),('Single','Single'),('Married','Married')]


        #CHOICES = Province.objects.values_list('id', 'name')
