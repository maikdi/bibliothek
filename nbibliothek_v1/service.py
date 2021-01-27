import configparser, datetime,os

from nbibliothek_v1.database import BibliothekDB
from nbibliothek_v1.ui import BibliothekUI


class AbstractDatabaseObserver:
    def call(self, title):
        pass


class TrendingBookObserver(AbstractDatabaseObserver):
    def __init__(self, title):
        self.title = title
        self.count = 0

    def call(self, title):
        if self.count >= 5:
            print("[EMAIL] Pustakawan, buku berjudul {} sudah dicari oleh orang lebih dari 5x.".format(title))
        else:
            pass


class AvailableBookObserver(AbstractDatabaseObserver):
    def __init__(self, service):
        self.service = service

    def call(self, title):
        borrowed = self.service.get_book_amount_borrowed_by_title(title)
        print("[EMAIL] Buku berjudul {} sudah dapat dipinjam ({}/5).".format(title, 5 - borrowed))


class BibliothekService:
    def __init__(self, url , lang="IN"):
        self.__db = BibliothekDB(url)
        self.__lang = lang
        self._lang_key = self.__create_key()
        # self.__ui = BibliothekUI(self)
        self._observers = []
        self.__add_observer(AvailableBookObserver(self))
        self._trending_observer = {}

    def init_db(self):
        self.__db.init()

    def run(self):

        library = BibliothekUI(self)
        library.show()

    def __create_key(self):
        project_path = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_path)
        keys = configparser.ConfigParser()
        keys.read(base_dir + "\_resources\language.ini")
        return keys

    def get_lang_pack(self):
        return self._lang_key["IN"]

    def __add_observer(self, observer):
        self._observers.append(observer)

    def search_book(self, title):
        book = self.__db.get_book_by_title(title)
        if len(book) == 0 and title != "":
            if title not in self._trending_observer.keys():
                self._trending_observer[title] = TrendingBookObserver(title)
                self._trending_observer[title].count += 1
            else:
                self._trending_observer[title].count += 1
                self._trending_observer[title].call(title)
        return book

    def search_member(self, nim):
        return self.__db.get_member_by_nim(nim)

    def get_lang(self):
        return self.__lang

    def borrow_book(self, nim, title, return_date):
        self.begin_transaction()
        self.__db.borrow_book_by_title(title)
        self.__db.insert_borrowing(nim, title, return_date)
        self.commit()

    def return_book(self, nim, title):
        self.begin_transaction()
        self.__db.remove_borrowing(nim, title)
        self.__db.return_book_by_title(title)
        for i in range(len(self._observers)):
            self._observers[i].call(title)
        self.commit()

    def get_book_amount_borrowed_by_title(self, title):
        return self.__db.get_book_borrowed_amount_by_title(title)

    def get_borrowed_amount(self, nim):
        return self.__db.count_borrowed_by_nim(nim)

    def get_borrowed_book(self, nim):
        return self.__db.get_borrowed_books_by_nim(nim)

    def get_datereturn(self, nim):
        return self.__db.get_timereturn_books_by_nim(nim)

    def get_report(self):
        report_date = datetime.datetime.today().strftime('%m.%Y')
        popular_dto = self.get_popular_books()
        popular_books = [popular_dto._book1, popular_dto._book2, popular_dto._book3, popular_dto._book4,
                         popular_dto._book5]
        print("5 Buku terpopuler dalam bulan {}".format(report_date))
        if popular_books == [("","")] * 5:
            popular_dto = self.__db.dummy_report()
            popular_books = [popular_dto._book1, popular_dto._book2, popular_dto._book3, popular_dto._book4,
                             popular_dto._book5]
            for book, author in popular_books:
                print("Judul: {}".format(book))
                print("Pengarang: {}".format(author))
                print("")
        else:
            for book, author in popular_books:
                print("Judul: {}".format(book))
                print("Pengarang: {}".format(author))
                print("")

    def get_popular_books(self):
        return self.__db.get_populer_books()

    def begin_transaction(self):
        # print("begin transaction")
        pass

    def commit(self):
        # print("commited")
        pass
