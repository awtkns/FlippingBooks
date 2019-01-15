from django.db import connection


class Sql:

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """GENERAL SQL (ANY TABLE)"""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    @staticmethod
    def get_all(table):
        """
        SELECT * from the specified table
        :param table: table to get all from
        """
        db = connection.cursor()
        sql = "SELECT * FROM %s" % table

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_count(table):
        """
        SELECT COUNT(*) from the specified table
        :param table: table to get count from
        """
        db = connection.cursor()
        sql = "SELECT COUNT(*) FROM %s" % table

        db.execute(sql)
        return db.fetchall()


    @staticmethod
    def delete_entire_table(table):
        """
        Deletes all the tuples in a table
        DO NOT USE UNLESS YOU BREAK THE TABLE
        (Adam breaks tables)
        """
        db = connection.cursor()
        sql = "DELETE FROM %s" % table
        db.execute(sql)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """GET SQL"""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def default_unregistered():
        """
        This method does a default query of all listings
        :return: a simple query of all listings
        """
        db = connection.cursor()
        db.execute(
            'SELECT b.Title, b.Author, b.Edition, l.Price, l.BookCondition '
            'FROM main_Listing l '
            'JOIN main_Book b on l.ISBN = b.ISBN ORDER BY l.price ASC')

        return db.fetchall()

    @staticmethod
    def default_registered():
        """
        This method does a default query of all listings
        INCLUDES THE USER ID
        :return: a simple query of all listings
        """
        db = connection.cursor()
        sql = "SELECT  b.Title, b.Author, b.Edition, l.Price, l.BookCondition, u.email " \
              "FROM main_Book b " \
              "JOIN main_Listing l ON l.ISBN = b.ISBN " \
              "JOIN auth_user u ON l.username = u.id ORDER BY l.price ASC"

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def my_listings(current_user):
        """
        All listing made by user
        :param current_user: user to search for
        :return: all listing made by user
        """

        # returns all listings made by the user
        db = connection.cursor()
        sql = "SELECT b.isbn, b.Title, b.Author, b.Edition, l.Price, l.BookCondition " \
               "FROM main_Listing l, main_Book b " \
               "WHERE l.ISBN = b.ISBN " \
               "AND l.username = " + sql_str(current_user) + " ORDER BY l.price ASC "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_all_listings_join():
        """
        Get all listings by all users
        :return: all listings joined with selling user and book
        """
        db = connection.cursor()

        # Get All
        sql = "SELECT b.ISBN, b.Title, b.Author, b.Edition, l.Price, l.BookCondition, u.email " \
              "FROM main_Book b " \
              "JOIN main_Listing l ON l.ISBN = b.ISBN " \
              "JOIN auth_user u ON l.username = u.id "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_all_advanced_listings_join():
        """
        Default sql for advanced search page
        """
        db = connection.cursor()
        sql = "SELECT b.ISBN, b.Title, b.Author, b.Edition, c.department, c.coursenumber, " \
              "p.lastname, sh.schoolname, l.Price, l.BookCondition, u.email " \
              "FROM main_listing l " \
              "JOIN auth_user u ON l.username = u.id " \
              "JOIN main_book b ON l.isbn = b.isbn " \
              "LEFT JOIN main_booksinsection bs ON bs.isbn = l.isbn " \
              "LEFT JOIN main_section s ON bs.sectionID = s.sectionid " \
              "LEFT JOIN main_course c ON s.courseid = c. courseid " \
              "LEFT JOIN main_prof p ON s.profid = p.profid " \
              "LEFT JOIN main_school sh ON c.schoolid = sh.schoolid"

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_all_school():
        """
        Get all schools for the drop down list
        """
        db = connection.cursor()
        sql = "SELECT schoolid, schoolname " \
              "FROM main_school"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_courseid(dept, number, school):
        """
        Gets the course id of a course
        """
        db = connection.cursor()
        sql = "SELECT courseid " \
              "FROM main_course " \
              "WHERE department = %s AND coursenumber = %s AND schoolid = %s" % (sql_str(dept), sql_str(number), sql_str(school))
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_section_join():
        """
        Query to display section information
        """
        db = connection.cursor()

        # Get All
        sql = "SELECT s.sectionid, c.department, c.coursenumber, s.sectionnumber, " \
              "s.term, s.year, p.lastname, sh.schoolname " \
              "FROM main_section s " \
              "JOIN main_course c ON s.courseid = c.courseid " \
              "JOIN main_prof p ON s.profid = p.profid " \
              "JOIN main_school sh ON c.schoolid = sh.schoolid "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_bookinsection_join():
        """
        Join the book and section table
        """
        db = connection.cursor()

        # Get All
        sql = "SELECT b.isbn, b.title, c.department, c.coursenumber, s.sectionnumber, " \
              "s.term, s.year, sh.schoolname " \
              "FROM main_booksinsection bs " \
              "JOIN main_section s ON bs.sectionid = s.sectionid " \
              "JOIN main_course c ON s.courseid = c.courseid " \
              "JOIN main_book b ON bs.isbn = b.isbn " \
              "JOIN main_school sh ON c.schoolid = sh.schoolid "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_num_unique_books_listed():
        """
        Gets the number of unique books listed
        """
        db = connection.cursor()
        sql = "SELECT COUNT(DISTINCT isbn) FROM main_listing"

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_max_avg_book_isbn():
        """
        Gets the book with the maximum avg price of a it's listings
        """
        db = connection.cursor()
        sql = "SELECT l.isbn, AVG(l.price) " \
              "FROM main_listing l " \
              "GROUP BY l.isbn " \
              "ORDER BY AVG(l.price) DESC LIMIT 1"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_min_avg_book_isbn():
        """
        Gets the book with the minimum avg price of a it's listings
        """
        db = connection.cursor()
        sql = "SELECT l.isbn, AVG(l.price) " \
              "FROM main_listing l " \
              "GROUP BY l.isbn " \
              "ORDER BY AVG(l.price) ASC LIMIT 1"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_avg_book_price():
        """
        Gets the avg listing price
        """
        db = connection.cursor()
        sql = "SELECT AVG(price) FROM main_listing"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_book_title(isbn):
        """
        Gets the title of the book
        """
        db = connection.cursor()
        sql = "SELECT title FROM main_book WHERE isbn = " + sql_str(isbn)
        db.execute(sql)
        return db.fetchall()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """IS (Returns if it exists in the table)"""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def is_listed(isbn, user):
        """
        Checks if a isbn is listed by a user
        :param isbn:
        :return: the listing
        """
        db = connection.cursor()

        sql = "SELECT * " \
              "FROM main_Listing l " \
              "WHERE l.ISBN = " + sql_str(isbn) + " "\
              "AND l.username = " + sql_str(user)

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_book(isbn):
        """
        Returns true if the isbn is a book
        """
        db = connection.cursor()
        sql = "SELECT ISBN " \
              "FROM main_book " \
              "WHERE ISBN = " + sql_str(isbn)

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_prof(first, last):
        """
        Returns true if it is a prof
        """
        db = connection.cursor()
        sql = "SELECT ProfID " \
              "FROM main_prof p GROUP BY p.firstname, p.lastname " \
              "HAVING lower(p.firstname) = " + sql_str(first.lower()) + " AND lower(p.lastname) = " + sql_str(
            last.lower())

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_profid_valid(prof_id):
        """
        Returns true if it is a prof
        """
        db = connection.cursor()
        sql = "SELECT * " \
              "FROM main_prof " \
              "WHERE profid = " + sql_str(prof_id)

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_course(dept, number, school):
        """
        Returns true if it is a course
        """
        db = connection.cursor()
        sql = "SELECT courseID " \
              "FROM main_course " \
              "WHERE department = " + sql_str(dept) + " AND coursenumber = " + sql_str(number) + " AND schoolid = " + sql_str(
            school)

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_section(section, term, year, dept, course_number, school):
        """
        Returns true if it is a section
        """
        if not Sql.is_course(dept, course_number, school):
            return False

        else:
            db = connection.cursor()
            sql = "SELECT * FROM main_section s " \
                  "WHERE s.courseid = (" \
                  "SELECT c.courseid FROM main_course c " \
                  "WHERE department = " + sql_str(dept) + \
                  " AND coursenumber = " + sql_str(course_number) + \
                  " AND schoolid = " + sql_str(school) + \
                  ") AND s.sectionid = " + sql_str(section) + \
                  " AND s.term = " + sql_str(term) + \
                  " AND s.year = " + sql_str(year)

            db.execute(sql)
            return len(db.fetchall()) > 0

    @staticmethod
    def is_sectionid_valid(section_id):
        """
        Returns true if it is a section
        """
        db = connection.cursor()
        sql = "SELECT * " \
              "FROM main_section " \
              "WHERE sectionid = " + sql_str(section_id)

        db.execute(sql)
        return len(db.fetchall()) > 0

    @staticmethod
    def is_bookinsection(isbn, section_id):
        """
        Returns true if the book is in a section
        """
        db = connection.cursor()
        sql = "SELECT * " \
              "FROM main_booksinsection " \
              "WHERE isbn = " + sql_str(isbn) + " AND sectionid = " + sql_str(section_id)

        db.execute(sql)
        return len(db.fetchall()) > 0

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """INSERT """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def add_listing(user, isbn, price, condition):
        """
        Adds a listing to the table
        """
        db = connection.cursor()
        sql = "INSERT INTO main_listing (username, isbn, price, bookcondition) " \
              "VALUES ('" + str(user) + "', " + str(isbn) + ", " + str(price) + ", '" + condition + "')"

        db.execute(sql)

    @staticmethod
    def add_book(isbn, title, author, edition):
        """
        Adds a book to the table
        """
        db = connection.cursor()
        sql = "INSERT INTO main_book (ISBN, Title, Author, Edition) " \
              "VALUES (" + sql_str(isbn) + ", " + sql_str(title) + \
              ", " + sql_str(author) + ", " + sql_str(edition) + ")"

        db.execute(sql)

    @staticmethod
    def add_prof(first, last):
        """
        Adds a prof to the table
        """
        db = connection.cursor()
        sql = "INSERT INTO main_prof (FirstName, LastName) " \
              "VALUES (" + sql_str(first) + ", " + sql_str(last) + ")"

        db.execute(sql)

    @staticmethod
    def add_course(dept, number, name, school):
        """
        Adds a course to the table
        """
        db = connection.cursor()
        sql = "INSERT INTO main_course (department, coursenumber, coursename, schoolid) " \
              "VALUES (" + sql_str(dept) + ", " + sql_str(number) + ", " + sql_str(name) + ", " + sql_str(school) + ")"

        db.execute(sql)

    @staticmethod
    def add_section(section, term, year, course_id, profid):
        db = connection.cursor()
        sql = "INSERT INTO main_section (sectionnumber, term, year, courseid, profid) " \
              "VALUES (" + sql_str(section) + ", " + sql_str(term) + \
              ", " + sql_str(year) + ", " + sql_str(course_id) + ", " + sql_str(profid) + ")"

        db.execute(sql)

    @staticmethod
    def add_bookinsection(isbn, sectionid):
        """
        Links a book to a section
        """
        db = connection.cursor()
        sql = "INSERT INTO main_booksinsection (isbn, sectionid) " \
              "VALUES (" + sql_str(isbn) + ", " + sql_str(sectionid) + ")"

        db.execute(sql)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """UPDATE """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def update_listing(user, isbn, price, condition):
        """
        Updates a listing
        """
        db = connection.cursor()
        sql = "UPDATE main_listing " \
              "SET price = " + sql_str(price) + ", BookCondition = " + sql_str(condition) + " " \
              "WHERE isbn = " + sql_str(isbn) + " AND username = " + sql_str(user)
        db.execute(sql)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """DELETE """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def delete_listing(isbn, user):
        """
        Deletes a listing
        """
        db = connection.cursor()
        sql = "DELETE FROM main_listing WHERE isbn = " + sql_str(isbn) + " and username = " + sql_str(user)

        db.execute(sql)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """OTHER """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    @staticmethod
    def search(title, isbn, price, condition):
        """
        This method does a Search query of all listings
        :return: a search of all listings
        """

        db = connection.cursor()

        # Get All
        sql = "SELECT b.ISBN, b.Title, b.Author, b.Edition, l.Price, l.BookCondition, u.email " \
               "FROM main_Book b " \
               "JOIN main_Listing l ON l.ISBN = b.ISBN " \
               "JOIN auth_user u ON l.username = u.id " \
               "WHERE b.title LIKE " + sql_str('%' + title + '%')

        if isbn is not None:
            sql += " AND l.isbn LIKE " + sql_str('%' + sql_str(isbn) + '%')

        if price is not None:
            if price == '100':
                sql += " AND l.Price >= 0 AND l.Price <= 100"

            elif price == '200':
                sql += " AND l.Price > 100 AND l.Price <= 200"

        if condition is not None:
            if condition != "Any":
                sql += " AND l.bookcondition = " + sql_str(condition)

        sql += " ORDER BY l.price ASC "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def advanced_search(title, isbn, price, condition, dept, course_number,
                        school, prof_lastname, find_min, not_mine, user):
        """
        This method does a search query of all like listings
        """

        db = connection.cursor()
        sql = "SELECT b.ISBN, b.Title, b.Author, b.Edition, c.department, c.coursenumber, " \
              "p.lastname, sh.schoolname, l.Price, l.BookCondition, u.email " \
              "FROM main_listing l " \
              "JOIN auth_user u ON l.username = u.id " \
              "JOIN main_book b ON l.isbn = b.isbn " \
              "LEFT JOIN main_booksinsection bs ON bs.isbn = l.isbn " \
              "LEFT JOIN main_section s ON bs.sectionID = s.sectionid " \
              "LEFT JOIN main_course c ON s.courseid = c. courseid " \
              "LEFT JOIN main_prof p ON s.profid = p.profid " \
              "LEFT JOIN main_school sh ON c.schoolid = sh.schoolid " \
              "WHERE b.title LIKE " + sql_str('%' + title + '%')

        # filter by isbn
        if isbn is not None:
            sql += " AND l.isbn LIKE " + sql_str('%' + sql_str(isbn) + '%')

        # filter by price
        if price is not None:
            if price == '100':
                sql += " AND l.Price >= 0 AND l.Price <= 100"

            elif price == '200':
                sql += " AND l.Price > 100 AND l.Price <= 200"

        # filter by condition
        if condition is not None:
            if condition != "Any":
                sql += " AND l.bookcondition = " + sql_str(condition)

        # filter by dept
        if dept is not None:
            if dept != 'Any':
                sql += " AND c.department = " + sql_str(dept)

        # filter by course number
        if course_number is not None:
            sql += " AND c.coursenumber LIKE " + sql_str('%' + sql_str(course_number) + '%')

        # filter by school
        if school is not None:
            if school != 'Any':
                sql += " AND sh.schoolid = " + sql_str(school)

        # filter by prof
        if prof_lastname is not None:
            if prof_lastname != '':
                sql += " AND p.lastname LIKE " + sql_str('%' + prof_lastname + '%')

        # filter by min price
        if find_min:
            sql += " AND l.price = ("
            sql += "SELECT MIN(price) FROM main_listing minl WHERE minl.isbn = l.isbn "

            if not_mine:
                sql += "AND minl.username != " + sql_str(user)

            sql += ") "


        # filter by not my listings
        if not_mine:
            sql += "EXCEPT "
            sql += "SELECT b.ISBN, b.Title, b.Author, b.Edition, c.department, c.coursenumber, " \
                   "p.lastname, sh.schoolname, l.Price, l.BookCondition, u.email " \
                   "FROM main_listing l " \
                   "JOIN auth_user u ON l.username = u.id " \
                   "JOIN main_book b ON l.isbn = b.isbn " \
                   "LEFT JOIN main_booksinsection bs ON bs.isbn = l.isbn " \
                   "LEFT JOIN main_section s ON bs.sectionID = s.sectionid " \
                   "LEFT JOIN main_course c ON s.courseid = c. courseid " \
                   "LEFT JOIN main_prof p ON s.profid = p.profid " \
                   "LEFT JOIN main_school sh ON c.schoolid = sh.schoolid  " \
                   "WHERE l.username = " + sql_str(user)

        sql += " ORDER BY l.price ASC "

        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_delete_ddl(user):
        """
        Dynamic drop down list for update / delete mylisting
        """
        db = connection.cursor()
        sql = "SELECT l.isbn, b.title " \
              "FROM main_listing l " \
              "JOIN main_book b ON l.isbn = b.isbn " \
              "WHERE l.username = " + sql_str(user) + " ORDER BY b.title ASC"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_add_ddl():
        """
        Dynamic drop down list for adding a listing
        """
        db = connection.cursor()
        sql = "SELECT isbn, title " \
              "FROM main_book ORDER BY title ASC"
        db.execute(sql)
        return db.fetchall()


def sql_str(text):
    """
    Parse's text into sql format.  Safeguards against injection
    """
    if type(text) is int:
        return str(text)
    else:
        text = text.replace('\'', '\'\'')
        return '\'' + text + '\''
