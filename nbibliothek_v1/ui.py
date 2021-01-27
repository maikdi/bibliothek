from datetime import date, timedelta
from tkinter import Tk, Label, Entry, Button, ttk
import configparser


class BibliothekUI:
    def __init__(self, service):
        self.__title = "Neugierig Bibliothek"
        self.__root = Tk()
        self.__service = service
        self.__keys = self.__create_key()
        self.__key_lang = self.__service.get_lang_pack()
        self._header = self.__create_header()  # Title, header, and date
        self._tabs = self.__create_window_tab()  # Frames for tab1 and tab2
        self.__book_tab = self.__create_book_tab()
        self.__member_tab = self.__create_member_tab()
        self.__book_desc = self.grid_book_desc(self.__book_tab)
        self.__member_desc = self.grid_member_desc(self.__member_tab)
        self.__borrowed_books_desc = self.grid_borrowed_desc(self.__member_tab)
        self.__return_books_desc = self.grid_return_button(self.__member_tab)
        self.__book_search_button = self.__create_book_search_button()
        self.__member_search_button = self.__create_member_search_button()
        self.__borrow_book_button = self.__create_borrow_book_button()
        self.__popular_book_tab = self.popular_book_tab()
        self.__popular_book_desc = self.popular_book_label()

        self.__load_popular_books()


    def __load_popular_books(self):
        popular_books = self.__service.get_popular_books()

        self.config_popular_book(popular_books._book1,
                                 popular_books._book2,
                                 popular_books._book3,
                                 popular_books._book4,
                                 popular_books._book5
                                 )

    def __create_window_title(self):
        self.__root.title(self.__title)

    def __create_key(self):
        keys = configparser.ConfigParser()
        keys.read('language.ini')
        return keys

    def __create_header(self):
        title = Label(self.__root, text="Neugierig Bibliothek", font=("Gotham Narrow Ultra", 14), anchor="w", bg="#e8e8e8")
        addresss = Label(self.__root, text="Ilse. Str No.21\n"
                                           "Berlin - 12053", font=("Comic Sans MS", 14),
                         anchor="w", bg="#e8e8e8")

        dates = date.today()
        dates = Label(self.__root, text="{}".format(dates), font=("Gotham Narrow Ultra", 14), anchor="e", bg="#e8e8e8")

        title.grid(row=0, column=0, sticky="snew")
        addresss.grid(row=1, rowspan=2, column=0, sticky="snew")
        dates.grid(row=0, column=0, sticky="e")
        return title, addresss, date

    def __create_window_tab(self):
        tab_control = ttk.Notebook(self.__root)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)

        tab_control.add(tab1, text=self.__key_lang["tab1"])
        tab_control.add(tab2, text=self.__key_lang['tab2'])
        tab_control.grid(row=3, column=0, sticky="snew")

        return tab1, tab2

    def __create_error_label(self, master, row, column):
        error_label = Label(master, text="")
        error_label.grid(row=row, column=column)
        return error_label

    # Grids
    def grid_book_desc(self, master):
        row = 0
        title = ttk.Label(master, text="")
        title.grid(row=row, column=1)
        author = ttk.Label(master, text="")
        author.grid(row=row + 1, column=1)
        publisher = ttk.Label(master, text="")
        publisher.grid(row=row + 2, column=1)
        class_no = ttk.Label(master, text="")
        class_no.grid(row=row + 3, column=1)
        barcode = ttk.Label(master, text="")
        barcode.grid(row=row + 4, column=1)
        exemplar = ttk.Label(master, text="")
        exemplar.grid(row=row + 5, column=1)
        return title, author, publisher, class_no, barcode, exemplar

    def grid_member_desc(self, master):
        row = 0
        blank = Label(master, text="", width=27)
        blank.grid(row=row, column=1)
        name = ttk.Label(master, text="")
        name.grid(row=row, column=1)
        nim = ttk.Label(master, text="")
        nim.grid(row=row + 1, column=1)
        return_date = ttk.Label(master, text="")
        return_date.grid(row=row + 2, column=1)
        return name, nim, return_date

    def grid_borrowed_desc(self, master):
        row = 6
        borrowed_1 = ttk.Label(master, text="")
        borrowed_1.grid(row=row + 4, column=1)
        borrowed_2 = Label(master, text="")
        borrowed_2.grid(row=row + 5, column=1)
        borrowed_3 = Label(master, text="")
        borrowed_3.grid(row=row + 6, column=1)

        timer_borrowed_1 = ttk.Label(master, text="")
        timer_borrowed_1.grid(row=row + 4, column=0)
        timer_borrowed_2 = Label(master, text="")
        timer_borrowed_2.grid(row=row + 5, column=0)
        timer_borrowed_3 = Label(master, text="")
        timer_borrowed_3.grid(row=row + 6, column=0)

        return borrowed_1, borrowed_2, borrowed_3, timer_borrowed_1, timer_borrowed_2, timer_borrowed_3

    def grid_return_button(self, master):
        row = 6
        book1_label, book2_label, book3_label, time1, time2, time3 = self.__borrowed_books_desc

        return_1 = Button(master, text=self.__key_lang['return_button'], fg="#ff0000", bg="white", anchor="e",
                          command=lambda: self.__return_book_click(book1_label, time1))
        return_1.grid(row=row + 4, column=3, sticky="se")
        return_2 = Button(master, text=self.__key_lang['return_button'], fg="#ff0000", bg="white",
                          command=lambda: self.__return_book_click(book2_label, time2))
        return_2.grid(row=row + 5, column=3)
        return_3 = Button(master, text=self.__key_lang['return_button'], fg="#ff0000", bg="white",
                          command=lambda: self.__return_book_click(book3_label, time3))
        return_3.grid(row=row + 6, column=3)
        return return_1, return_2, return_3

    # Tabs
    def __create_member_tab(self):
        tab_control = ttk.Notebook(self._tabs[0])
        member_tab = ttk.Frame(tab_control)

        tab_control.add(member_tab, text=self.__key_lang['member_tab'])
        tab_control.grid(row=9, column=0, columnspan=3, sticky="swen")

        row = 0
        name_label = ttk.Label(member_tab, text=self.__key_lang["member_name"], width=30)
        name_label.grid(row=row, column=0)
        nim_label = ttk.Label(member_tab, text=self.__key_lang["member_nim"], width=30)
        nim_label.grid(row=row + 1, column=0)
        returns_label = ttk.Label(member_tab, text=self.__key_lang["member_return_date"], width=30)
        returns_label.grid(row=row + 2, column=0)
        borrowed_label = ttk.Label(member_tab, text=self.__key_lang["member_borrowing"], width=30)
        borrowed_label.grid(row=row + 3, column=0)
        borrowed_date_per_book = ttk.Label(member_tab, text=self.__key_lang["member_borrowed_date"], width=30)
        borrowed_date_per_book.grid(row=row + 4, column=0)

        self.__member_error_label = self.__create_error_label(self._tabs[0], row + 1, 1)

        return member_tab

    def __create_book_tab(self):
        tab_control = ttk.Notebook(self._tabs[0])
        book_tab = ttk.Frame(tab_control)

        tab_control.add(book_tab, text=self.__key_lang['book_tab'])
        tab_control.grid(row=3, column=0, columnspan=3, sticky="snew")

        row = 0
        title_label = ttk.Label(book_tab, text=self.__key_lang['book_title'], width=30)
        title_label.grid(row=row, column=0)
        author_label = ttk.Label(book_tab, text=self.__key_lang['book_author'], width=30)
        author_label.grid(row=row + 1, column=0)
        publisher_label = ttk.Label(book_tab, text=self.__key_lang['book_publisher'], width=30)
        publisher_label.grid(row=row + 2, column=0)
        class_no_label = ttk.Label(book_tab, text=self.__key_lang['book_classification'], width=30)
        class_no_label.grid(row=row + 3, column=0)
        barcode_label = ttk.Label(book_tab, text=self.__key_lang['book_barcode'], width=30)
        barcode_label.grid(row=row + 4, column=0)
        copies_label = ttk.Label(book_tab, text=self.__key_lang['exemplar'], width=30)
        copies_label.grid(row=row + 5, column=0)

        self.__book_error_label = self.__create_error_label(self._tabs[0], 1, 1)

        return book_tab

    # Books
    def __create_book_search_button(self):
        master = self._tabs[0]
        entry_label = Label(master, text=self.__key_lang['book_search'], borderwidth=1, anchor="e")
        entry_label.grid(row=0, column=0)

        blank = Label(master, text="")
        blank.grid(row=1, column=0)

        self.book_entry_box = Entry(master, borderwidth=2, width=40)
        self.book_entry_box.grid(row=0, column=1)

        search_button = Button(master, text=self.__key_lang['search_button'], fg="#0090d1", bg="white", borderwidth=1,
                               command=lambda: self.__book_search_click(self.book_entry_box.get()), width=10)
        search_button.grid(row=0, column=2)
        return search_button

    def __book_search_click(self, entry):
        row = 0
        book_dto = self.__service.search_book(entry)
        if len(book_dto) == 0:
            if entry == "":
                self.__book_error_label.grid_remove()
                self.write_book_desc("", "", "", "", "", "", "")
                pass
            else:
                self.__book_error_label.grid_remove()
                self.write_book_desc("", "", "", "", "", "", "")
                self.__book_error_label = self.__create_error_label(self._tabs[0], row + 1, 1)
                self.__config_book_error_message(entry)
        else:
            self.__book_error_label.grid_remove()
            book_dto = book_dto[0]
            self.write_book_desc(
                book_dto._title,
                book_dto._author,
                book_dto._publisher,
                book_dto._classification,
                book_dto._barcode,
                book_dto._borrowed_amount,
                book_dto._copies
            )

    def write_book_desc(self, title, author, publisher, class_no, barcode, borrowed, available):
        title_label, author_label, publisher_label, class_no_label, barcode_label, exemplar_label = self.__book_desc
        title_label.configure(text="{}".format(title))
        author_label.configure(text="{}".format(author))
        publisher_label.configure(text="{}".format(publisher))
        class_no_label.configure(text="{}".format(class_no))
        barcode_label.configure(text="{}".format(barcode))
        if borrowed == "" and available == "":
            exemplar_label.configure(text="{}{}".format(borrowed, available))
        else:
            exemplar_label.configure(text="{}/{}".format(available - borrowed, available))

    def __config_book_error_message(self, message):
        self.__book_error_label.configure(
            bg="red",
            text=self.__key_lang['no_book'].format(message))

    # Members
    def __create_member_search_button(self):
        row = 6
        master = self._tabs[0]
        entry_label = Label(master, text=self.__key_lang['member_nim'], borderwidth=1, anchor="e")
        entry_label.grid(row=row, column=0)

        self.member_entry_box = Entry(master, borderwidth=2, width=40)
        self.member_entry_box.grid(row=row, column=1)

        search_button = Button(master, text=self.__key_lang['search_button'], fg="#0090d1", bg="white", borderwidth=1,
                               width=10,
                               command=lambda: self.__member_search_click(self.member_entry_box.get()))

        search_button.grid(row=row, column=2)
        return search_button

    def __member_search_click(self, entry):
        row = 6
        member_dto = self.__service.search_member(entry)
        current_time = date.today()
        return_time = self.update_datetime_by_a_week(current_time)
        books_borrowed = self.__service.get_borrowed_amount(entry)
        if books_borrowed == 3:
            self.__disable_borrow_button()
        else:
            self.__enable_borrow_button()
            self.__borrow_error_label.grid_remove()

        if len(member_dto) == 0:
            if entry == "":
                self.__member_error_label.grid_remove()
                self.write_member_desc("", "", "")
                self.write_books_borrowed("", "", "", "", "", "")
                pass
            else:
                self.__member_error_label.grid_remove()
                self.write_member_desc("", "", "")
                self.write_books_borrowed("", "", "", "", "", "")
                self.__member_error_label = self.__create_error_label(self._tabs[0], row + 1, 1)
                self.__config_member_error_message(entry)
        else:
            self.__member_error_label.grid_remove()
            member_dto = member_dto[0]
            self.write_member_desc(member_dto._name,
                                   member_dto._nim,
                                   # member_dto._tanggal_kembali,
                                   return_time
                                   )
            borrowed_books = self.__service.get_borrowed_book(member_dto._nim)
            book1, book2, book3 = borrowed_books._book1, borrowed_books._book2, borrowed_books._book3

            timer = self.__service.get_datereturn(member_dto._nim)
            time1x, time2x, time3x = timer._time1, timer._time2, timer._time3
            self.write_books_borrowed(book1, book2, book3, time1x, time2x, time3x)

    def write_member_desc(self, name, nim, returns):
        name_label, nim_label, return_date = self.__member_desc
        name_label.configure(text="{}".format(name))
        nim_label.configure(text="{}".format(nim))
        return_date.configure(text="{}".format(returns))

    def __config_member_error_message(self, message):
        self.__member_error_label.configure(
            bg="red",
            text=self.__key_lang['no_member'].format(message))

    # borrows
    def __create_borrow_book_button(self):
        row = 7
        master = self._tabs[0]
        self.__borrow_error_label = Label(master, bg="red", text=self.__key_lang['borrow_limit_exceed'])
        borrow_button = Button(master, text=self.__key_lang['borrow_button'], fg="#008554", bg="white", borderwidth=2,
                               width=10,
                               command=lambda: self.__borrow_book_click()
                               )

        borrow_button.grid(row=row, column=2)
        return borrow_button

    def __borrow_book_click(self):
        row = 7

        title = self.__book_desc[0]['text']
        nim = self.__member_desc[1]['text']

        book_dto = self.__service.search_book(title)
        member_dto = self.__service.search_member(nim)

        member_borrowed = self.__service.get_borrowed_amount(nim)
        current_time = date.today()
        return_time = self.update_datetime_by_a_week(current_time)

        if member_borrowed == 3:
            self.__disable_borrow_button()
        else:
            self.__enable_borrow_button()
        if len(member_dto) == 0 or len(book_dto) == 0:
            if nim == "" or title == "":
                # print("nothing")
                self.__borrow_error_label.grid_remove()
            pass

        elif member_borrowed == None or member_borrowed < 3:
            # print("book borrowed")
            borrowed_books_total = self.__service.get_book_amount_borrowed_by_title(title)
            if borrowed_books_total < 5:

                self.__service.borrow_book(nim, title, return_time)
                borrowed_books = self.__service.get_borrowed_book(nim)
                book1, book2, book3 = borrowed_books._book1, borrowed_books._book2, borrowed_books._book3

                timer = self.__service.get_datereturn(nim)
                time1x, time2x, time3x = timer._time1, timer._time2, timer._time3
                # update ui
                book_dto = book_dto[0]
                self.__borrow_error_label.config(text=self.__key_lang['book_borrowed'], bg="green")
                self.__borrow_error_label.grid(row=row, column=1)
                self.write_book_desc(
                    book_dto._title,
                    book_dto._author,
                    book_dto._publisher,
                    book_dto._classification,
                    book_dto._barcode,
                    book_dto._borrowed_amount + 1,
                    book_dto._copies
                )
                self.write_books_borrowed(book1,
                                          book2,
                                          book3,
                                          time1x,
                                          time2x,
                                          time3x)
                self.__load_popular_books()

            else:
                self.__borrow_error_label.grid_remove()
                self.__borrow_error_label = Label(self._tabs[0], bg="red", text=self.__key_lang['no_more_book'])
                self.__borrow_error_label.grid(row=row, column=1)

        else:
            # print("Rejected")
            self.__borrow_error_label.grid_remove()
            self.__borrow_error_label = Label(self._tabs[0], bg="red", text=self.__key_lang['borrow_limit_exceed'])
            self.__borrow_error_label.grid(row=row, column=1)

    def __disable_borrow_button(self):
        self.__borrow_book_button["state"] = "disabled"

    def write_books_borrowed(self, book1, book2, book3, time1x, time2x, time3x):
        book1_label, book2_label, book3_label, time1, time2, time3 = self.__borrowed_books_desc

        book1_label.configure(text="{}".format(book1))
        book2_label.configure(text="{}".format(book2))
        book3_label.configure(text="{}".format(book3))

        time1.config(text="{}".format(time1x))
        time2.config(text="{}".format(time2x))
        time3.config(text="{}".format(time3x))

    def __enable_borrow_button(self):
        self.__borrow_book_button["state"] = "normal"

    # Returns
    def __return_book_click(self, label, time):
        nim = self.__member_desc[1]['text']
        title = label['text']
        book_dto = self.__service.search_book(title)
        if len(book_dto) >= 1:
            book_dto = book_dto[0]
            self.write_book_desc(
                book_dto._title,
                book_dto._author,
                book_dto._publisher,
                book_dto._classification,
                book_dto._barcode,
                book_dto._borrowed_amount - 1,
                book_dto._copies
            )
            self.__borrow_error_label.grid_remove()
            self.__borrow_error_label.config(text=self.__key_lang['book_returned'], bg="green")
            self.__service.return_book(nim, title)
            self.__load_popular_books()
            label.configure(text="{}".format(""))
            time.configure(text="{}".format(""))
            self.__enable_borrow_button()

    # date thing
    def update_datetime_by_a_week(self, current_date):
        days = 7
        new_date = current_date + timedelta(days=days)
        return new_date

    # report label
    def popular_book_label(self):
        master = self._tabs[1]

        row = 0
        label_1 = Label(master, text=self.__key_lang['report_popular_book'].format(date.today().strftime('%m.%Y')),
                        width=65, bg="white")
        label_1.grid(row=row, column=1, columnspan=2)

        row = 1

        label_1 = Label(master, text=" \n ", relief="groove", width=45, justify="left",
                        anchor="w")
        label_1.grid(row=row, column=2)

        label_2 = Label(master, text=" \n ", relief="groove", width=45, justify="left",
                        anchor="w")
        label_2.grid(row=row + 1, column=2)

        label_3 = Label(master, text=" \n ", relief="groove", width=45, justify="left",
                        anchor="w")
        label_3.grid(row=row + 2, column=2)

        label_4 = Label(master, text=" \n ", relief="groove", width=45, justify="left",
                        anchor="w")
        label_4.grid(row=row + 3, column=2)

        label_5 = Label(master, text=" \n ", relief="groove", width=45, justify="left",
                        anchor="w")
        label_5.grid(row=row + 4, column=2)

        return label_1, label_2, label_3, label_4, label_5

    # popular_book
    def popular_book_tab(self):
        master = self._tabs[1]
        row = 1

        for i in range(0, 5):
            label = Label(master,
                          text=self.__key_lang['book_title'] +
                               "\n" +
                               self.__key_lang['book_author'],
                          relief="groove",
                          width=20,
                          justify="left",
                          anchor="w"
                          )
            label.grid(row=row + i, column=1)

    def config_popular_book(self, book1="", book2="", book3="", book4="", book5=""):
        label1, label2, label3, label4, label5 = self.__popular_book_desc
        list = [book1, book2, book3, book4, book5]
        label_list = [label1, label2, label3, label4, label5]
        for book in range(len(list)):
            if list[book] == "":
                label_list[book].configure(text=" \n " )
            else:
                label_list[book].configure(text="{} \n{}".format(list[book][0], list[book][1]))

    #############
    def show(self):
        self.__create_window_title()

        self.__root.mainloop()