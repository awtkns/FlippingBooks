from django import forms
from .models import *


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""ADD FORMS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class AddBookForm(forms.Form):
    """
    Form to add a book
    """
    isbn = forms.IntegerField(label="ISBN", required=True)
    title = forms.CharField(label="Title", required=True)
    author = forms.CharField(label="Author", required=True)
    edition = forms.IntegerField(label="Edition", required=True)

    class Meta:
        fields = ['isbn', 'title', 'author', 'edition', ]


class AddProfForm(forms.Form):
    """
    Form to add a prof
    """
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)

    class Meta:
        fields = ['first_name', 'last_name', ]


class AddCourseForm(forms.Form):
    """
    Form to add a course
    """
    department = forms.ChoiceField(label="Department", choices=department, required=True)
    number = forms.IntegerField(label="Number", required=True)
    name = forms.CharField(label="Name", required=True)
    school = forms.ChoiceField(label="School", choices=Ddl.schools(), required=True)

    class Meta:
        fields = ['department', 'number', 'name', 'school', ]


class AddSectionForm(forms.Form):
    """
    Form to add a Listing
    """
    school = forms.ChoiceField(label="School", choices=Ddl.schools())
    department = forms.ChoiceField(label="Department", choices=department, required=True)
    course_number = forms.IntegerField(label="Course Number", required=True)
    section = forms.IntegerField(label="Section", required=True)
    term = forms.ChoiceField(label="Term", choices=terms, required=True)
    year = forms.ChoiceField(label="Year", choices=years, required=True)
    prof = forms.IntegerField(label="ProfID", required=True)

    class Meta:
        fields = ['school', 'department', 'course_number', 'section', 'term', 'year', 'prof']


class AddBookInSectionForm(forms.Form):
    """
    Form to add a book to a section
    """
    isbn = forms.IntegerField(label="ISBN", required=True)
    sectionid = forms.IntegerField(label="Section ID", required=True)

    class Meta:
        fields = ['isbn', 'sectionid']


class AddListingForm(forms.Form):
    """
    Form to add a Listing
    """

    def __init__(self, *args, **kwargs):
        super(AddListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'] = forms.ChoiceField(label="Book Title", choices=Ddl.add_listing(), required=True)
        self.fields['price'] = forms.IntegerField(label="Price", required=True)
        self.fields['condition'] = forms.ChoiceField(label="Condition", choices=condition, required=True)

    class Meta:
        fields = ['isbn', 'price', 'condition', ]


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""UPDATE FORMS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class UpdateListingForm(forms.Form):
    """
    Form to update a listing
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'] = forms.ChoiceField(label="Book Title", choices=Sql.get_delete_ddl(user), required=True)
        self.fields['price'] = forms.IntegerField(label="Price", required=True)
        self.fields['condition'] = forms.ChoiceField(label="Condition", choices=condition, required=True)

    class Meta:
        fields = ['isbn', 'price', 'condition', ]


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""DELETE FORMS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DeleteListingForm(forms.Form):
    """
    Form to delete a Listing
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'] = forms.ChoiceField(label="Book Title", choices=Sql.get_delete_ddl(user), required=True)

    class Meta:
        fields = ['isbn']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""OTHER FORMS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class SearchForm(forms.Form):
    """"
    This form is for searching book listings in the database
    Only registered users can access this form
    """
    book_title = forms.CharField(label="Book Title", max_length=255, required=False)
    ISBN = forms.IntegerField(label="ISBN", required=False)
    price = forms.ChoiceField(label="Price Range", choices=price_range, initial=-1)
    condition_form = forms.ChoiceField(label="Condition", choices=search_condition, initial="Any")

    class Meta:
        fields = ['book_title', 'ISBN', 'price', 'condition_form', ]


class AdvancedSearchForm(SearchForm):
    """
    The advanced search form which extends the basic one
    """
    department = forms.ChoiceField(label="Department", choices=search_department, required=False, initial="Any")
    course_number = forms.IntegerField(label="Course Number", required=False)
    school = forms.ChoiceField(label="School", choices=[('Any', 'Any')] + Ddl.schools(), initial="Any")
    prof_lastname = forms.CharField(label="Prof's Last Name", required=False)
    find_min = forms.BooleanField(label="Find Lowest Price", required=False)
    not_mine = forms.BooleanField(label="Exclude My Listings", required=False)

    class Meta:
        fields = ['book_title', 'ISBN', 'price', 'condition_form',
                  'department', 'course_number', 'school', 'prof_lastname', 'find_min', 'not_mine']


class UserRegistrationForm(forms.ModelForm):
    """
    This form is for registering a user
    """

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'confirm_password', ]

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match")

        return self.cleaned_data
