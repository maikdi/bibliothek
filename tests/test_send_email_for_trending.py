from nbibliothek_v1.service import BibliothekService
import io,sys
def test_borrow_book():
    test_service = BibliothekService("")
    test_service.init_db()
    borrowed_amount_before = test_service.get_book_amount_borrowed_by_title("Hulu Sort")
    test_service.borrow_book("10101190564","Hulu Sort","26/12/2001")
    borrowed_amount_after = test_service.get_book_amount_borrowed_by_title("Hulu Sort")
    assert borrowed_amount_before == borrowed_amount_after - 1

def test_check_trending():
    test_service = BibliothekService("")
    test_service.init_db()
    expected_return = "[EMAIL] Pustakawan, buku berjudul test_book1 sudah dicari oleh orang lebih dari 5x.\n"
    for _ in range(5):
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        test_service.check_trending("test_book1")
        sys.stdout = sys.__stdout__  # Reset redirect.
    assert expected_return == capturedOutput.getvalue()
def test_email_after_book_returned():
    test_service = BibliothekService("")
    test_service.init_db()
    expected_return = "[EMAIL] Buku berjudul The God Delusion sudah dapat dipinjam (5/5).\n"
    test_service.borrow_book("10101190564","The God Delusion","2001/12/12")
    capturedOutput = io.StringIO()  # Create StringIO object
    sys.stdout = capturedOutput  # and redirect stdout.
    test_service.return_book("10101190564","The God Delusion")
    sys.stdout = sys.__stdout__  # Reset redirect.
    assert expected_return == capturedOutput.getvalue()


