import sqlite3


class BibliothekDB:
    def __init__(self, url):
        self.__db_file = url
        self._conn = self.__create_connection(self.__db_file)

    def __create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except:
            return conn

    def create_book_table(self):
        create_statement = """
        CREATE TABLE books (
            book_id number PRIMARY KEY,
            judul text(255),
            pengarang text(255),
            penerbit text(255),
            no_klasifikasi number,
            no_barcode number,
            jumlah_exemplar number,
            terpinjam number
        )
        """
        cursor = self._conn.cursor()
        cursor.execute(create_statement)
        self._conn.commit()

    def create_member_table(self):
        create_statement = """
        CREATE TABLE members (
            nama text(255),
            nim text(255),
            returndate DATE
        )
        """
        cursor = self._conn.cursor()
        cursor.execute(create_statement)
        self._conn.commit()

    def create_borrowing_list(self):
        create_statement = """
        CREATE TABLE borrowing_list(
            nim text(255),
            judul text(255),
            returndate DATE,
          FOREIGN KEY (nim) REFERENCES members (nim)
        )
        """
        cursor = self._conn.cursor()
        cursor.execute(create_statement)
        self._conn.commit()

    # Insert
    def insert_books(self):
        insert_statement = """
        INSERT INTO books VALUES
            (1,'The God Delusion', 'Richard Dawkins', 'Bantam Books', 211, 177013, 5,0),
            (2,'Tuhan, Penciptaan, Kemanusiaan','Moody Asyer', 'KP Literasi', 211, 271749, 5,0),
            (3,'Bodybuilding Basics', 'Rivaldo Linogi', 'Gramedia', 300, 317112, 5, 0), 
            (4,'Mendekati Hati Lewat Mengajar', 'Charis Hulu', 'Beyond n Books', 320, 280221, 5, 0),
            (5,'Mulai Investasi Bitcoin', 'Rivaldo Linogi', 'Gremadia', 700, 264480, 5, 0),
            (6,'世界の最高', 'Darren Rusly', 'KP Literasi', 700, 332361, 5,0),
            (7,'Hulu Sort', 'Charis Hulu', 'KP Literasi', 600, 140401, 5, 0),
            (8,'Hululoho Algorithm', 'Badia Sihaloho', 'KP Literasi', 610, 223510, 5,0),
            (9,'Kumpulan Puisi Zabdi', 'Christyane Zabdi', 'Beyond n Books', 800, 251885,5,0),
            (10,'Karya-Karya Elson Sensei', 'Christopher Vincent', 'Gremadia',800, 280033, 5,0)
        """
        c = self._conn.cursor()
        c.execute(insert_statement)
        self._conn.commit()

    def insert_members(self):
        insert_statement = """
        INSERT INTO members VALUES
            ('Sanga Lawalata', '0331970205','-'),
            ('Michael David', '10101190564','-'),
            ('Charis Hulu', '10101190429', '-'),
            ('Rivaldo Linogi', '10101190177','-'),
            ('Reszisca Valentiana', '10101190702' , '-'),
            ('Joy Milliaan', '10102190103', '-'),
            ('Johan Budiono', 'iya', '-'),
            ('Christyane Zabdi', '1010119018','-'),
            ('Victoriano Aribaldi' ,'10102190296','-'),
            ('Elson','10101190694','-')               
        """
        c = self._conn.cursor()
        c.execute(insert_statement)
        self._conn.commit()

    def insert_borrowing(self, nim, title, return_date):
        insert_statement = """
        INSERT INTO borrowing_list VALUES
            (?, ?, ?)
        """
        cursor = self._conn.cursor()
        cursor.execute(insert_statement, (nim, title, return_date))
        self._conn.commit()

    def init(self):
        drop_books = """
        DROP TABLE IF EXISTS books
        """
        drop_members = """
        DROP TABLE IF EXISTS members
        """
        drop_borrow = """
        DROP TABLE IF EXISTS borrowing_list
        """
        c = self._conn.cursor()
        c.execute(drop_books)
        c.execute(drop_members)
        c.execute(drop_borrow)
        self.create_book_table()
        self.insert_books()
        self.create_member_table()
        self.insert_members()
        self.create_borrowing_list()
        self._conn.commit()


    def return_book_by_title(self, title):
        update_statement = """
        UPDATE books
          SET terpinjam = terpinjam - 1
         WHERE judul = ?
        """
        cursor = self._conn.cursor()
        cursor.execute(update_statement, (title,))
        self._conn.commit()
        # book = self.get_book_by_title(title)[0]
        # observer.call(book._copies)

    def get_member_by_nim(self, nim):
        select_statement = """
        SELECT * 
          FROM members
         WHERE nim = ?
        """
        c = self._conn.cursor()
        c.execute(select_statement, (nim,))
        rows = c.fetchall()
        return self.__membertoDTO(rows)

    def get_book_by_title(self, title):
        select_statement = """
        SELECT * 
          FROM books
         WHERE judul = ? COLLATE NOCASE
        """
        c = self._conn.cursor()
        c.execute(select_statement, (title,))
        rows = c.fetchall()
        return self.__booktoDTO(rows)

    def get_book_borrowed_amount_by_title(self, title):
        select_statement = """
        SELECT * 
          FROM books
         WHERE judul = ? COLLATE NOCASE
        """
        c = self._conn.cursor()
        c.execute(select_statement, (title,))
        rows = c.fetchall()
        return rows[0][7]

    # borrowings
    def borrow_book_by_title(self, title):
        update_statement = """
        UPDATE books
          SET terpinjam = terpinjam + 1
         WHERE judul = ?
        """
        cursor = self._conn.cursor()
        cursor.execute(update_statement, (title,))
        self._conn.commit()
        # book = self.get_book_by_title(title)[0]
        # observer.call(book._copies)

    def remove_borrowing(self, nim, title):
        delete_statement = """
        DELETE
            FROM borrowing_list
              WHERE rowid in
             (SELECT rowid FROM borrowing_list
              WHERE nim = ? AND judul = ?
             LIMIT 1)
        """
        cursor = self._conn.cursor()
        cursor.execute(delete_statement, (nim, title,))
        self._conn.commit()

    def count_borrowed_by_nim(self, nim):
        select_statement = """
        SELECT COUNT(nim)
          FROM borrowing_list
         WHERE nim = ?
        """
        cursor = self._conn.cursor()
        cursor.execute(select_statement, (nim,))
        rows = cursor.fetchall()
        return rows[0][0]

    def get_borrowed_books_by_nim(self, nim):
        select_statement = """
        SELECT judul
          FROM borrowing_list
         WHERE nim = ?
        """
        c = self._conn.cursor()
        c.execute(select_statement, (nim,))
        rows = c.fetchall()
        return self.__borrowedtoDTO(rows)[0]

    #time
    def get_timereturn_books_by_nim(self, nim):
        select_statement = """
        SELECT returndate
          FROM borrowing_list
         WHERE nim = ?
        """
        c = self._conn.cursor()
        c.execute(select_statement, (nim,))
        rows = c.fetchall()
        return self.__timetoDTO(rows)[0]

    #dummy reports
    def dummy_report(self):
        select_statement = """
                SELECT judul
                  FROM books
                  LIMIT 5
                """

        c = self._conn.cursor()
        c.execute(select_statement)
        rows = c.fetchall()
        return self.__popular5toDTO(rows)[0]

    def get_populer_books(self):
        select_statement = """
        SELECT judul, COUNT(judul)
          FROM borrowing_list
         GROUP BY judul
         ORDER BY COUNT(judul) DESC
        """
        c = self._conn.cursor()
        c.execute(select_statement)
        rows = c.fetchall()
        return self.__popular5toDTO(rows)[0]

    #toDTO things
    def __booktoDTO(self, rows):
        dto_list = []
        for book_id, title, author, publisher, classification, barcode, copies, borrowed in rows:
            dto_list.append(BookDTO(title, author, publisher, classification, barcode, copies, borrowed))
        return dto_list

    def __membertoDTO(self, rows):
        dto_list = []
        for name, nim, tanggal_kembali in rows:
            dto_list.append(MemberDTO(name, nim, tanggal_kembali))
        return dto_list

    def __borrowedtoDTO(self, rows):
        borrowed_list = ["", "", ""]
        dto_list = []
        for books in range(len(rows)):
            borrowed_list[books] = rows[books][0]
        dto_list.append(BorrowedDTO(borrowed_list[0],
                                    borrowed_list[1],
                                    borrowed_list[2]
                                    ))
        return dto_list

    def __timetoDTO(self, rows):
        time_list = ["", "", ""]
        dto_list = []
        for dates in range(len(rows)):
            time_list[dates] = rows[dates][0]
        dto_list.append(TimeReturnDTO(time_list[0],
                                      time_list[1],
                                      time_list[2]
                                      ))
        return dto_list

    def __popular5toDTO(self, rows):
        popular_list = [("",""), ("",""), ("",""), ("",""), ("","")]

        dto_list = []
        for books in range(len(rows)):
            book = self.get_book_by_title(rows[books][0])
            popular_list[books] = [book[0]._title, book[0]._author]
        dto_list.append(Popular5bookDTO(popular_list[0],
                                        popular_list[1],
                                        popular_list[2],
                                        popular_list[3],
                                        popular_list[4]
                                        ))
        return dto_list


# dto class
class BookDTO:
    def __init__(self, title, author, publisher, classification, barcode, copies, borrowed):
        self._title = title
        self._author = author
        self._publisher = publisher
        self._classification = classification
        self._barcode = barcode
        self._copies = copies
        self._borrowed_amount = borrowed


class MemberDTO:
    def __init__(self, name, nim, tanggal_kembali):
        self._name = name
        self._nim = nim
        self._tanggal_kembali = tanggal_kembali


class BorrowedDTO:
    def __init__(self, book1="", book2="", book3=""):
        self._book1 = book1
        self._book2 = book2
        self._book3 = book3


class TimeReturnDTO:
    def __init__(self, time1="", time2="", time3=""):
        self._time1 = time1
        self._time2 = time2
        self._time3 = time3


class Popular5bookDTO:
    def __init__(self, book1="", book2="", book3="", book4="", book5=""):
        self._book1 = book1
        self._book2 = book2
        self._book3 = book3
        self._book4 = book4
        self._book5 = book5
