from django.contrib import admin
from .models import Course, EnrollbyStudent, Instructor, Major, Student,UploadExcel,IDandFullname, Subject, Academic_year, Year_level,Room,Subject, TimeSched, DaySched, SubjectsLoaded, Curriculum

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
admin.site.register(IDandFullname)




# Register your models here.
