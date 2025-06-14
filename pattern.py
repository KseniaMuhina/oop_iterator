from abc import ABC, abstractmethod
from collections.abc import Iterable as PyIterable, Iterator as PyIterator
from typing import Any, List, Optional


class Iterator(ABC):
    """
    Abstract Iterator interface (GoF Style).
    Declares the interface for accessing and traversing elements.
    """
    @abstractmethod
    def has_next(self) -> bool:
        """Checks if there are more elements (GoF specific)."""
        pass

    @abstractmethod
    def __next__(self) -> Any:
        """
        Returns the next element in the sequence.
        Raises StopIteration when the end of the collection is reached.
        """
        pass

    # For Pythonic compatibility, __iter__ should return self for an iterator
    def __iter__(self) -> PyIterator:
        return self


class Iterable(ABC):
    """
    Abstract Iterable interface (GoF Style).
    Declares the interface for creating an Iterator object.
    """
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Returns a new concrete GoF Iterator object for the collection."""
        pass


# Concrete Implementations

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

    def __hash__(self):
        return hash((self.title, self.author))


class BookCollection(Iterable, PyIterable):
    """
    Concrete Aggregate that holds a collection of books.
    Implements the GoF Iterable interface and Python's Iterable protocol.
    """
    def __init__(self, collection: Optional[List[Book]] = None) -> None:
        self._books: List[Book] = collection or []

    def add_book(self, book: Book) -> None:
        """Adds a book to the collection."""
        self._books.append(book)

    def __len__(self) -> int:
        """Returns the number of books in the collection (Pythonic)."""
        return len(self._books)

    def __getitem__(self, index: int) -> Book:
        """Allows access to elements by index (Pythonic)."""
        if 0 <= index < len(self._books):
            return self._books[index]
        raise IndexError("Book index out of bounds.")

    def count(self) -> int:
        """GoF-style method to return the number of books."""
        return self.__len__()

    def create_iterator(self) -> Iterator:
        """
        Creates and returns a concrete GoF-style iterator for this collection
        (forward traversal by default).
        """
        return BookIterator(self, reverse=False)

    def get_reverse_iterator(self) -> Iterator:
        """
        Creates and returns a concrete GoF-style iterator for this collection
        (reverse traversal).
        """
        return BookIterator(self, reverse=True)

    def __iter__(self) -> PyIterator:
        """
        Returns a Pythonic iterator for the collection.
        This allows the collection to be used directly in a 'for' loop.
        """
        return BookIterator(self, reverse=False)


class BookIterator(Iterator, PyIterator):
    """
    Concrete Iterator that traverses the BookCollection.
    Keeps track of the current position in the traversal.
    Implements both GoF Iterator interface and Python's Iterator protocol.
    """
    def __init__(self,
                 collection: BookCollection,
                 reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = len(collection) - 1 if reverse else 0

    def has_next(self) -> bool:
        """
        Checks if there are more books to iterate over (GoF specific).
        """
        if self._reverse:
            return self._position >= 0
        return self._position < len(self._collection)

    def __next__(self) -> Any:
        """
        Returns the next book in the collection and advances the iterator.
        Raises StopIteration if there are no more elements.
        """
        if not self.has_next():
            raise StopIteration("No more elements in the collection.")

        book = self._collection[self._position]
        self._position += (-1 if self._reverse else 1)
        return book


if __name__ == "__main__":
    collection = BookCollection()
    collection.add_book(Book("The Hitchhiker's Guide to the Galaxy",
                             "Douglas Adams"))
    collection.add_book(Book("1984", "George Orwell"))
    collection.add_book(Book("Brave New World", "Aldous Huxley"))

    print("--- GoF-style Iteration (Forward) ---")
    gof_iterator = collection.create_iterator()
    while gof_iterator.has_next():
        book = gof_iterator.__next__()  # Using __next__ directly
        print(f"- {book}")

    print("\n--- Pythonic Iteration (Forward via 'for' loop) ---")
    for book in collection:  # Uses __iter__ and __next__ automatically
        print(f"- {book}")

    print("\n--- GoF-style Iteration (Reverse) ---")
    reverse_iterator = collection.get_reverse_iterator()
    while reverse_iterator.has_next():
        book = reverse_iterator.__next__()
        print(f"- {book}")

    print("\nAttempting to iterate beyond the end")
    try:
        iterator_beyond_end = collection.create_iterator()
        # Iterate all elements
        for _ in collection:
            pass  # Consume all elements

        # Now try to call __next__ explicitly on the exhausted iterator
        iterator_beyond_end.__next__()
    except StopIteration as e:
        print(f"Caught expected error: {e}")
