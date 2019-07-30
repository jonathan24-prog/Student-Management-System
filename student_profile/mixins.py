
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import EnrollbyStudent, Student,Major, Academic_year, Year_level,Course
from datetime import datetime, timezone


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            
            student=get_object_or_404(Student,pk=self.request.POST.get('pk'))
            major=get_object_or_404(Major,pk=self.request.POST.get('major'))
            academic_year=get_object_or_404(Academic_year,pk=self.request.POST.get('academic_year'))
            year_level=get_object_or_404(Year_level,pk=self.request.POST.get('year_level'))
            course=get_object_or_404(Course, pk=self.request.POST.get('course'))
            semister=form.cleaned_data['semister']

            student_enrollKey=EnrollbyStudent.objects.filter(enrollment_key=student.student_id+academic_year.ay+course.code+semister)
            if not student_enrollKey.exists():
                enroll=EnrollbyStudent.objects.create(student=student,course=course,
                                                        major=major,
                                                        academic_year=academic_year,
                                                        year_level=year_level,
                                                        semister=semister,
                                                        enrollment_key=student.student_id+academic_year.ay+course.code+semister)
                
                enrollRes={'pk': enroll.pk,'message':'enrolled successfully','is_save':True}
                return JsonResponse(enrollRes,safe=False)
            else:
                enrollRes={'message':'already enrolled on this semister','is_save':False}
                return JsonResponse(enrollRes,safe=False)

        
        else:
            return response

