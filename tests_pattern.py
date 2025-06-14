import pytest
from pattern import Book, BookCollection, BookIterator, Iterator
from typing import Any


# --- Positive Tests ---
def test_empty_collection_gof_iterator():
    """
    Test that a GoF-style iterator for an empty collection correctly
    reports no elements.
    """
    collection = BookCollection()
    iterator = collection.create_iterator()
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.__next__()


def test_single_element_gof_iteration():
    """
    Test GoF-style iteration over a collection with a single element.
    """
    collection = BookCollection()
    book = Book("The Catcher in the Rye", "J.D. Salinger")
    collection.add_book(book)

    iterator = collection.create_iterator()
    assert iterator.has_next()
    assert iterator.__next__() == book
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.__next__()


def test_multiple_elements_gof_iteration():
    """
    Test GoF-style iteration over a collection with multiple elements.
    """
    collection = BookCollection()
    book1 = Book("Pride and Prejudice", "Jane Austen")
    book2 = Book("To Kill a Mockingbird", "Harper Lee")
    book3 = Book("The Great Gatsby", "F. Scott Fitzgerald")
    collection.add_book(book1)
    collection.add_book(book2)
    collection.add_book(book3)

    expected_books = [book1, book2, book3]
    actual_books = []

    iterator = collection.create_iterator()
    while iterator.has_next():
        actual_books.append(iterator.__next__())

    assert actual_books == expected_books
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.__next__()  # Next call should raise StopIteration


def test_multiple_iterators_for_same_collection():
    """
    Test that multiple GoF-style iterators can traverse
    the same collection independently.
    """
    collection = BookCollection()
    book1 = Book("Moby Dick", "Herman Melville")
    book2 = Book("Don Quixote", "Miguel de Cervantes")
    collection.add_book(book1)
    collection.add_book(book2)

    iterator1 = collection.create_iterator()
    iterator2 = collection.create_iterator()

    # Iterate independently
    assert iterator1.__next__() == book1
    assert iterator2.__next__() == book1
    assert iterator1.__next__() == book2
    assert iterator2.__next__() == book2

    assert not iterator1.has_next()
    assert not iterator2.has_next()


def test_pythonic_iteration_forward():
    """
    Test iteration using Python's built-in 'for'
    loop (via __iter__ and __next__).
    """
    collection = BookCollection()
    book1 = Book("Python Crash Course", "Eric Matthes")
    book2 = Book("Fluent Python", "Luciano Ramalho")
    collection.add_book(book1)
    collection.add_book(book2)

    expected_books = [book1, book2]
    actual_books = [book for book in collection]  # Uses __iter__ and __next__

    assert actual_books == expected_books


def test_reverse_iterator_gof_style():
    """
    Test GoF-style reverse iteration.
    """
    collection = BookCollection()
    book1 = Book("Book A", "Author X")
    book2 = Book("Book B", "Author Y")
    book3 = Book("Book C", "Author Z")
    collection.add_book(book1)
    collection.add_book(book2)
    collection.add_book(book3)

    expected_books = [book3, book2, book1]  # Reversed order
    actual_books = []

    reverse_iterator = collection.get_reverse_iterator()
    while reverse_iterator.has_next():
        actual_books.append(reverse_iterator.__next__())

    assert actual_books == expected_books
    assert not reverse_iterator.has_next()
    with pytest.raises(StopIteration):
        reverse_iterator.__next__()


def test_reverse_iterator_pythonic_style_not_directly_supported():
    """
    Note: Python's 'for item in reversed(collection)' typically
    requires __reversed__.
    This test clarifies that __iter__ still gives forward for `for`
    loop unless __reversed__ is implemented.
    However, the `BookIterator` itself can be set to reverse.
    """
    collection = BookCollection()
    book1 = Book("Book 1", "Auth 1")
    collection.add_book(book1)

    actual_books_forward = [book for book in collection]
    assert actual_books_forward == [book1]

    # To get reverse, we explicitly ask for the reverse iterator
    reverse_iter = collection.get_reverse_iterator()
    assert reverse_iter.__next__() == book1


# --- Negative Tests ---
def test_next_on_empty_collection_raises_stopiteration():
    """
    Test that calling __next__() on an empty collection
    immediately raises StopIteration.
    """
    collection = BookCollection()
    iterator = collection.create_iterator()
    with pytest.raises(StopIteration):
        iterator.__next__()


def test_next_after_full_iteration_raises_stopiteration():
    """
    Test that calling __next__() after the iterator
    has reached the end raises StopIteration.
    """
    collection = BookCollection()
    collection.add_book(Book("The Martian", "Andy Weir"))
    iterator = collection.create_iterator()
    iterator.__next__()  # Consume the only element

    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.__next__()


# --- Mock Object Test ---
class MockBook:
    """A mock object for the Book class to simulate external resource."""
    def __init__(self, mock_title: str, mock_author: str):
        self.mock_title = mock_title
        self.mock_author = mock_author

    def __str__(self):
        return f"'{self.mock_title}' by {self.mock_author} (Mock)"

    def __eq__(self, other):
        if not isinstance(other, MockBook):
            return NotImplemented
        return (
            self.mock_title == other.mock_title
            and self.mock_author == other.mock_author
        )

    def __hash__(self):
        return hash((self.mock_title, self.mock_author))


class MockBookCollection(BookCollection):
    """
    A mock collection that interacts with "external" MockBook resources.
    We'll override `__getitem__` to simulate fetching a mock object.
    """
    def __init__(self):
        super().__init__()
        # In a real scenario, this might connect to a mock database or API
        self._mock_data_source = [
            MockBook("Mock Book 1", "Mock Author A"),
            MockBook("Mock Book 2", "Mock Author B"),
            MockBook("Mock Book 3", "Mock Author C"),
        ]
        # For simplicity, we just use a subset for our mock test
        self._books = self._mock_data_source

    def __getitem__(self, index: int) -> MockBook:
        """
        Overrides the base method to return a MockBook,
        simulating an external resource.
        """
        if 0 <= index < len(self._books):
            # Simulate some "external" processing or transformation
            original_mock_book = self._books[index]
            return MockBook(
                f"Processed: {original_mock_book.mock_title}",
                original_mock_book.mock_author)
        raise IndexError("Mock book index out of bounds.")

    def __len__(self) -> int:
        """Returns the number of mock books in the collection."""
        return len(self._books)

    def create_iterator(self) -> Iterator:
        """
        Creates and returns a concrete iterator for this mock collection.
        The iterator should work with the mock's `__getitem__` method.
        """
        return BookIterator(self)  # Reusing the original BookIterator

    def __iter__(self) -> Any:
        return BookIterator(self)


def test_iterator_with_mock_object():
    """
    Test the iterator's logic when the underlying collection interacts
    with a 'mock' external resource (simulated by MockBookCollection).
    """
    mock_collection = MockBookCollection()
    iterator = mock_collection.create_iterator()

    # Expected books based on the mock_collection's `__getitem__` logic
    expected_processed_books = [
        MockBook("Processed: Mock Book 1", "Mock Author A"),
        MockBook("Processed: Mock Book 2", "Mock Author B"),
        MockBook("Processed: Mock Book 3", "Mock Author C"),
    ]

    actual_processed_books = []
    while iterator.has_next():  # Test GoF style
        actual_processed_books.append(iterator.__next__())

    assert len(actual_processed_books) == len(expected_processed_books)
    for actual, expected in zip(actual_processed_books,
                                expected_processed_books):
        assert actual.mock_title == expected.mock_title
        assert actual.mock_author == expected.mock_author

    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.__next__()

    # Test Pythonic style with mock
    actual_processed_books_pythonic = [book for book in mock_collection]
    assert (
        len(actual_processed_books_pythonic)
        == len(expected_processed_books)
    )
    for actual, expected in zip(actual_processed_books_pythonic,
                                expected_processed_books):
        assert actual.mock_title == expected.mock_title
        assert actual.mock_author == expected.mock_author
