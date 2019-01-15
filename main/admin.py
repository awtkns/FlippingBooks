from django.contrib import admin
from .startup import *
from .models import *
from django.apps import apps


"""
run system checks
"""
start_up_commands()


app_models = apps.get_app_config('main').get_models()


class BookAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'Title', 'Author', 'Edition')
admin.site.register(Book, BookAdmin)


class ProfAdmin(admin.ModelAdmin):
    list_display = ('ProfID', 'FirstName', 'LastName')
admin.site.register(Prof, ProfAdmin)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('SchoolID', 'SchoolName', 'Address')
admin.site.register(School, SchoolAdmin)


class ListingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ISBN', 'ListingID', 'Price', 'BookCondition')
admin.site.register(Listing, ListingAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('CourseID', 'Department', 'CourseNumber', 'CourseName', 'SchoolID')
admin.site.register(Course, CourseAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('SectionID', 'SectionNumber', 'Term', 'Year', 'CourseID', 'ProfID')
admin.site.register(Section, SectionAdmin)


class BooksInSectionAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'SectionID')
admin.site.register(BooksInSection, BooksInSectionAdmin)

