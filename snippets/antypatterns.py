

class BookService:
    def sell(self):
        # operuje na swoich danych
        pass

    # przekłądając tę metodę na życiową sytuację:
    # pracownik wchodzi do magazynu i zmienia cene na każdej z ksiązek
    # w rzeczywistosci ustaliby cene dla danego tytulu
    def change_price(self, title: str, new_price):
        # operuje na swoim zestawie danych ale istnieje złozonosc ktora nie istnieje w katalogu
        for book in Book.objects.with_title(title).filter(is_sold=False):
            book.change_price(new_price)

    # magazynu mie interesuje czy ksiazka jest sprzedana
    # (bo nie ma innych niz nie sprzedane)
    def relocate_to(self, book, shelf_number):
        # operuje na swoim zestawie danych
        # ale
        if book.is_sold:  # zlozonosc ktora nie istnieje w magazynie
            pass
            #/ ifologia


# --->


# zamowienia
class Book:
    def sell(self):
        # operuje na swoich danych
        pass


# katalog
class Book:
    def change_price(self, title: str, new_price):
        pass


# magazyn
class Book:
    def relocate_to(self, shelf_number):
        pass
