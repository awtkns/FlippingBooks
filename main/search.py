class Search:

    def __init__(self, book_name_is_empty=True, bookname="", isbn_is_empty=True, isbn=0,
                 pricerange=None, condition=""):
        self.bookName = bookname
        self.isbn = isbn
        self.bookNameIsEmpty = book_name_is_empty
        self.isbnIsEmpty = isbn_is_empty
        self.priceRange = pricerange
        self.condition = condition

    def build_sql_query(self):
        string = "SELECT"

