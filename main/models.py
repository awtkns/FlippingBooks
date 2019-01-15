from django.db import models
from .map import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Prof(models.Model):
    """
    This model contains all profs in the system.
    Each prof has a first name and last name, they are not associated with a single school
    """
    ProfID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50, null=False)

    class Meta:
        unique_together = ("FirstName", "LastName")

    def __str__(self):
        return self.FirstName + ' ' + self.LastName


class Book(models.Model):
    """
    This model contains the books. Each book is registered via their ISBN
    """
    ISBN = models.BigIntegerField(primary_key=True)
    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Edition = models.CharField(max_length=255)

    def __str__(self):
        return str(self.ISBN)


class School(models.Model):
    """
    This model stores the schools.
    Each school with multiple campuses will be stored separately.
    """
    SchoolID = models.AutoField(primary_key=True)
    SchoolName = models.CharField(max_length=50, null=False, unique=True)
    Address = models.CharField(max_length=255)

    def __str__(self):
        return self.SchoolName


class Listing(models.Model):
    """
    Listing of books from users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='username')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='ISBN')
    ListingID = models.AutoField(primary_key=True)
    Price = models.IntegerField(null=False)
    BookCondition = models.CharField(max_length=40, choices=condition)


class Course(models.Model):
    """
    courses, these are associated with a school.
    Each school can not have a course with the same department and course number
    """
    CourseID = models.AutoField(primary_key=True)
    Department = models.CharField(max_length=255)
    CourseNumber = models.IntegerField(null=False)
    CourseName = models.CharField(max_length=255)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE, db_column='SchoolID')

    class Meta:
        unique_together = ("Department", "CourseNumber", "SchoolID")

    def __str__(self):
        return str(self.CourseNumber) + ' ' + self.Department + ' - ' + str(self.SchoolID)


class Section(models.Model):
    """
    Each course can have 0 or more sections per term.
    This model is a weak entity to Courses
    A course can not have the same section in one term.
    """
    SectionID = models.AutoField(primary_key=True)
    SectionNumber = models.IntegerField(null=False)
    Term = models.CharField(max_length=20, null=False)
    Year = models.IntegerField(null=False)
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseID')
    ProfID = models.ForeignKey(Prof, on_delete=models.CASCADE, db_column='ProfID')

    class Meta:
        unique_together = ("SectionNumber", "Term", "Year", "CourseID")

    def __str__(self):
        return str(self.SectionNumber) + ' ' + self.Term + ' ' + str(self.Year) + ' ' + str(self.CourseID)


class BooksInSection(models.Model):
    """
    stores a lise of books used in each section of a course in a specific term
    """
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='ISBN')
    SectionID = models.ForeignKey(Section, on_delete=models.CASCADE, db_column='SectionID')
