from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from .sql import *

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""SHARED VIEWS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def about(request):
    """
    About us w/stats
    """

    # Stats
    num_users = Sql.get_count("auth_user")[0][0]
    num_listings = Sql.get_count("main_listing")[0][0]
    num_unique_books_listed = Sql.get_num_unique_books_listed()[0][0]
    avg_book_price = round(Sql.get_avg_book_price()[0][0], 2)

    highest_avg_price_book_isbn = Sql.get_max_avg_book_isbn()
    highest_avg_price_book_price = round(highest_avg_price_book_isbn[0][1], 2)
    highest_avg_price_book_title = Sql.get_book_title(highest_avg_price_book_isbn[0][0])[0][0]

    lowest_avg_price_book_isbn = Sql.get_min_avg_book_isbn()
    lowest_avg_price_book_price = round(lowest_avg_price_book_isbn[0][1], 2)
    lowest_avg_price_book_title = Sql.get_book_title(lowest_avg_price_book_isbn[0][0])[0][0]

    stats = [
            num_users,
            num_listings,
            num_unique_books_listed,
            avg_book_price,
            highest_avg_price_book_title,
            highest_avg_price_book_price,
            lowest_avg_price_book_title,
            lowest_avg_price_book_price
    ]

    if request.user.is_authenticated:
        return render(request, 'main/registered/about_r.html', context={'stats': stats})
    else:
        return render(request, 'main/unregistered/about.html', context={'stats': stats})


def contact(request):
    """
    Contact us
    """
    if request.user.is_authenticated:
        return render(request, 'main/registered/contact_r.html')
    else:
        return render(request, 'main/unregistered/contact.html')


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""REGISTERED USER'S VIEWS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def index(request):
    """
    Registered home page
    """
    if request.user.is_authenticated:
        listing = Sql.default_registered()
        stats = Sql.get_count('main_listing')
        if len(stats) > 0:
            stats = stats[0][0]
        else:
            stats = 0
        return render(request, 'main/registered/index.html', context={'listings': listing, 'stats': stats})
    else:
        return login_r(request)


def my_listing(request):
    """
    Shows the users listings
    """
    if request.user.is_authenticated:
        current_user = str(request.user.id)
        add_form = AddListingForm()
        delete_form = DeleteListingForm(user=current_user)
        update_form = UpdateListingForm(user=current_user)
        error_message = None

        if request.method == 'POST':

            if 'add' in request.POST:

                add_form = AddListingForm(request.POST)

                if add_form.is_valid():
                    data = add_form.cleaned_data
                    listing_isbn = data['isbn']
                    listing_price = data['price']
                    listing_condition = data['condition']

                    if Sql.is_book(listing_isbn):
                        if not Sql.is_listed(listing_isbn, current_user):
                            Sql.add_listing(current_user, listing_isbn, listing_price, listing_condition)
                        else:
                            error_message = "You already have that book listed!"
                    else:
                        error_message = "Not a book!"

            if 'update' in request.POST:

                update_form = UpdateListingForm(request.POST, user=current_user)

                if update_form.is_valid():
                    data = update_form.cleaned_data
                    listing_isbn = data['isbn']
                    listing_price = data['price']
                    listing_condition = data['condition']

                    if Sql.is_book(listing_isbn):
                        if Sql.is_listed(listing_isbn, current_user):
                            Sql.update_listing(current_user, listing_isbn, listing_price, listing_condition)
                        else:
                            error_message = "You don't have that book listed!"
                    else:
                        error_message = "Not a book!"

            if 'delete' in request.POST:

                delete_form = DeleteListingForm(request.POST, user=current_user)

                if delete_form.is_valid():
                    data = delete_form.cleaned_data
                    listing_isbn = data['isbn']

                    if Sql.is_book(listing_isbn):
                        if Sql.is_listed(listing_isbn, current_user):
                            Sql.delete_listing(listing_isbn, current_user)
                        else:
                            error_message = "You don't have that book listed!"
                    else:
                        error_message = "Not a book!"

        mine = Sql.my_listings(current_user)
        return render(request, 'main/registered/mylisting.html',
                      context={'listings': mine, 'add': add_form, 'delete': delete_form,
                               'update': update_form, 'error_message': error_message})
    else:
        return login_r(request)


def logout_r(request):
    """
    Logout
    """
    logout(request)
    listing = Sql.default_unregistered()
    return render(request, 'main/unregistered/home.html', context={'listings': listing})


def search(request):
    """
    Search for specific books
    """
    if request.user.is_authenticated:
        basic_form = SearchForm()
        advanced_form = AdvancedSearchForm()
        listings = Sql.get_all_listings_join()

        if request.method == 'POST':

            if 'basic' in request.POST:
                basic_form = SearchForm(request.POST)

                if basic_form.is_valid():
                    data = basic_form.cleaned_data
                    book_title = data['book_title']
                    book_isbn = data['ISBN']
                    book_price = data['price']
                    book_condition = data['condition_form']

                    listings = Sql.search(book_title, book_isbn, book_price, book_condition)

            elif 'advanced' in request.POST:
                advanced_form = AdvancedSearchForm(request.POST)

                if advanced_form.is_valid():
                    data = advanced_form.cleaned_data
                    book_title = data['book_title']
                    book_isbn = data['ISBN']
                    book_price = data['price']
                    book_condition = data['condition_form']
                    book_department = data['department']
                    course_number = data['course_number']
                    school = data['school']
                    prof_lastname = data['prof_lastname']
                    find_min = data['find_min']
                    not_mine = data['not_mine']
                    current_user = str(request.user.id)

                    advanced_listings = Sql.advanced_search(book_title, book_isbn, book_price, book_condition,
                                                            book_department, course_number, school,
                                                            prof_lastname, find_min, not_mine, current_user)

                    return render(request, 'main/registered/search.html',
                                  context={'form_basic': basic_form, 'form_advanced': advanced_form,
                                           'advanced_listings': advanced_listings})

        return render(request, 'main/registered/search.html',
                      context={'form_basic': basic_form, 'form_advanced': advanced_form,
                               'listings': listings})
    else:
        return login_r(request)


def add(request):
    """
    Add page
    """
    if request.user.is_authenticated:
        books = Sql.get_all("main_book")
        courses = Sql.get_all("main_course")
        profs = Sql.get_all("main_prof")
        sections = Sql.get_section_join()
        booksinsection = Sql.get_bookinsection_join()
        error_message = None

        if request.method == 'POST':

            if 'addbook' in request.POST:
                form_book = AddBookForm(request.POST)

                if form_book.is_valid():
                    data = form_book.cleaned_data
                    isbn = data['isbn']
                    title = data['title']
                    author = data['author']
                    edition = data['edition']

                    if not Sql.is_book(isbn):
                        Sql.add_book(isbn, title, author, edition)
                        books = Sql.get_all("main_book")
                    else:
                        error_message = 'Book already exists!'

            elif 'addcourse' in request.POST:
                form_course = AddCourseForm(request.POST)

                if form_course.is_valid():
                    data = form_course.cleaned_data
                    dept = data['department']
                    number = data['number']
                    name = data['name']
                    school = data['school']

                    if not Sql.is_course(dept, number, school):
                        Sql.add_course(dept, number, name, school)
                        courses = Sql.get_all("main_course")
                    else:
                        error_message = 'Course already exists!'

            elif 'addprof' in request.POST:
                prof_form = AddProfForm(request.POST)

                if prof_form.is_valid():
                    data = prof_form.cleaned_data
                    first_name = data['first_name']
                    last_name = data['last_name']

                    if not Sql.is_prof(first_name, last_name):
                        Sql.add_prof(first_name, last_name)
                        profs = Sql.get_all("main_prof")
                    else:
                        error_message = 'Prof already exists!'

            elif 'addsection' in request.POST:
                section_form = AddSectionForm(request.POST)

                if section_form.is_valid():
                    data = section_form.cleaned_data
                    school = data['school']
                    dept = data['department']
                    course_number = data['course_number']
                    section = data['section']
                    term = data['term']
                    year = data['year']
                    prof = data['prof']

                    if Sql.is_course(dept, course_number, school):

                        if Sql.is_profid_valid(prof):

                            if not Sql.is_section(section, term, year, dept, course_number, school):
                                course_id = Sql.get_courseid(dept, course_number, school)[0][0]
                                Sql.add_section(section, term, year, course_id, prof)
                                sections = Sql.get_section_join()
                            else:
                                error_message = 'Section already exists!'
                        else:
                            error_message = 'Prof does not exist!'
                    else:
                        error_message = 'Course does not exist!'

            elif 'addbooksinsection' in request.POST:
                bookinsection_form = AddBookInSectionForm(request.POST)

                if bookinsection_form.is_valid():
                    data = bookinsection_form.cleaned_data
                    isbn = data['isbn']
                    sectionid = data['sectionid']

                    if Sql.is_book(isbn):

                        if Sql.is_sectionid_valid(sectionid):

                            if not Sql.is_bookinsection(isbn, sectionid):
                                Sql.add_bookinsection(isbn, sectionid)
                                booksinsection = Sql.get_bookinsection_join()

                            else:
                                error_message = 'Book is already in section!'
                        else:
                            error_message = 'Section does not exist!'
                    else:
                        error_message = 'Book does not exist!'

        prof_form = AddProfForm()
        book_form = AddBookForm()
        course_form = AddCourseForm()
        section_form = AddSectionForm()
        bookinsection_form = AddBookInSectionForm()

        return render(request, 'main/registered/add.html',
                      context={'books': books, 'profs': profs, 'courses': courses,
                               'sections': sections, 'booksinsection': booksinsection,
                               'form_prof': prof_form, 'form_book': book_form,
                               'form_course': course_form, 'form_section': section_form,
                               'form_booksinsection': bookinsection_form, 'error_message': error_message})
    else:
        return login_r(request)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""UNREGISTERED USER'S VIEWS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def home(request):
    """
    Returns all the books for sale without the username of the seller
    """
    listing = Sql.default_unregistered()

    return render(request, 'main/unregistered/home.html', context={'listings': listing})


def login_r(request):
    """
    Login
    """
    if request.user.is_authenticated:
        # if they somehow get to login page after already loginning in
        # log the previous user out
        logout(request)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                listing = Sql.default_registered()
                stats = Sql.get_count('main_listing')
                if len(stats) > 0:
                    stats = stats[0][0]
                else:
                    stats = 0
                return render(request, 'main/registered/index.html', context={'listings': listing, 'stats': stats})

            else:
                return render(request, 'main/unregistered/login.html',
                              {'error_message': 'Your account has been disabled'})

        else:
            return render(request, 'main/unregistered/login.html',
                          {'error_message': 'Your username/password does not match.'
                                            '<br>Don\'t have an account?'
                                            '<a href="signup">'
                                            'Click here</a> to register.'})

    return render(request, 'main/unregistered/login.html')


class UserFormView(View):
    """
    Registration form
    """
    form_class = UserRegistrationForm
    template_name = 'main/unregistered/register.html'

    def get(self, request):
        """
        Display blank form
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Receive and check data
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # user = authenticate(username=username, password=password) #debugging

            if user is not None:
                if user.is_active:
                    return redirect('login')

        return render(request, self.template_name, {'form': form})
