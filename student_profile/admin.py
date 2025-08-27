from django.contrib import admin
from .models import AOSF, Course, EnrollbyStudent, Instructor, Major, Student,UploadExcel,IDandFullname, Subject, Academic_year, Year_level,Room,Subject, TimeSched, DaySched, SubjectsLoaded, Curriculum, ActiveSem

from django.contrib import admin

from .forms import ActiveSemAdminForm

class ActiveSemAdmin(admin.ModelAdmin):
    form = ActiveSemAdminForm
class IDandFullnameAdmin(admin.ModelAdmin):
    fields = ('student_id' , 'first_name','last_name', 'course')
    list_display = ('student_id' , 'first_name','last_name', 'course')
    search_fields = ('student_id' , 'first_name','last_name', 'course')


admin.site.register(Course)
admin.site.register(EnrollbyStudent)
admin.site.register(Instructor)
admin.site.register(Major)
admin.site.register(Academic_year)
admin.site.register(Student)
admin.site.register(Year_level)
admin.site.register(Room)
admin.site.register(Subject)
admin.site.register(TimeSched)
admin.site.register(DaySched)
admin.site.register(SubjectsLoaded)
admin.site.register(UploadExcel)
admin.site.register(Curriculum)
admin.site.register(IDandFullname, IDandFullnameAdmin)
admin.site.register(AOSF)
admin.site.register(ActiveSem)




# Register your models here.
