"""
Implementation of the Iterator Design Pattern.
"""

from abc import ABC, abstractmethod

# --- Abstract Interfaces ---

class Iterator(ABC):
    """
    Abstract Iterator interface.
    Declares the interface for accessing and traversing elements.
    """
    @abstractmethod
    def has_next(self) -> bool:
        """Checks if there are more elements."""
        pass

    @abstractmethod
    def next(self):
        """Returns the next element in the collection."""
        pass


class Iterable(ABC):
    """
    Abstract Iterable interface.
    Declares the interface for creating an Iterator object.
    """
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Returns a new iterator for the collection."""
        pass


# --- Concrete Implementations ---

class Book:
    """Represents a simple Book object."""
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.author == other.author


class BookCollection(Iterable):
    """
    Concrete Aggregate that holds a collection of books.
    Implements the Iterable interface to return a concrete Iterator.
    """
    def __init__(self):
        self._books = []

    def add_book(self, book: Book):
        """Adds a book to the collection."""
        self._books.append(book)

    def get_book(self, index: int) -> Book:
        """Gets a book by its index (for internal use, not part of iterator public API)."""
        if 0 <= index < len(self._books):
            return self._books[index]
        raise IndexError("Book index out of bounds.")

    def count(self) -> int:
        """Returns the number of books in the collection."""
        return len(self._books)

    def create_iterator(self) -> Iterator:
        """
        Creates and returns a concrete iterator for this collection.
        """
        return BookIterator(self)


class BookIterator(Iterator):
    """
    Concrete Iterator that traverses the BookCollection.
    Keeps track of the current position in the traversal.
    """
    def __init__(self, collection: BookCollection):
        self._collection = collection
        self._position = 0

    def has_next(self) -> bool:
        """
        Checks if there are more books to iterate over.
        """
        return self._position < self._collection.count()

    def next(self):
        """
        Returns the next book in the collection and advances the iterator.
        Raises StopIteration if there are no more elements.
        """
        if not self.has_next():
            raise StopIteration("No more elements in the collection.")
        
        book = self._collection.get_book(self._position)
        self._position += 1
        return book


# --- Client Code Example ---
if __name__ == "__main__":
    collection = BookCollection()
    collection.add_book(Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams"))
    collection.add_book(Book("1984", "George Orwell"))
    collection.add_book(Book("Brave New World", "Aldous Huxley"))

    print("Iterating through the book collection:")
    iterator = collection.create_iterator()
    while iterator.has_next():
        book = iterator.next()
        print(f"- {book}")

    print("\nAttempting to iterate beyond the end (demonstrates StopIteration):")
    try:
        iterator.next()
    except StopIteration as e:
        print(f"Caught expected error: {e}")

    # You can also use Python's built-in iterator protocol (__iter__ and __next__)
    # For a more Pythonic approach, you'd typically implement __iter__ in BookCollection
    # and yield elements. However, for demonstrating the GoF pattern explicitly,
    # we're using the separate Iterator class.

    # Example of a Pythonic iterator (if we were to adapt BookCollection):
    # class PythonicBookCollection:
    #     def __init__(self):
    #         self._books = []
    #     def add_book(self, book: Book):
    #         self._books.append(book)
    #     def __iter__(self):
    #         for book in self._books:
    #             yield book
    
    # print("\nUsing Pythonic iteration:")
    # pythonic_collection = PythonicBookCollection()
    # pythonic_collection.add_book(Book("Dune", "Frank Herbert"))
    # pythonic_collection.add_book(Book("Foundation", "Isaac Asimov"))
    # for book in pythonic_collection:
    #     print(f"- {book}")