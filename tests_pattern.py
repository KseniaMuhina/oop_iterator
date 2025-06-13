"""
Pytest tests for the Iterator Design Pattern implementation.
"""

import pytest
from pattern import Book, BookCollection, BookIterator, Iterator, Iterable


# --- Positive Tests ---

def test_empty_collection_iterator():
    """
    Test that an iterator for an empty collection correctly reports no elements.
    """
    collection = BookCollection()
    iterator = collection.create_iterator()
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.next()

def test_single_element_collection_iteration():
    """
    Test iteration over a collection with a single element.
    """
    collection = BookCollection()
    book = Book("The Catcher in the Rye", "J.D. Salinger")
    collection.add_book(book)

    iterator = collection.create_iterator()
    assert iterator.has_next()
    assert iterator.next() == book
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.next()

def test_multiple_elements_collection_iteration():
    """
    Test iteration over a collection with multiple elements.
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
        actual_books.append(iterator.next())
    
    assert actual_books == expected_books
    assert not iterator.has_next() # After full iteration, has_next should be False
    with pytest.raises(StopIteration):
        iterator.next() # Next call should raise StopIteration

def test_multiple_iterators_for_same_collection():
    """
    Test that multiple iterators can traverse the same collection independently.
    """
    collection = BookCollection()
    book1 = Book("Moby Dick", "Herman Melville")
    book2 = Book("Don Quixote", "Miguel de Cervantes")
    collection.add_book(book1)
    collection.add_book(book2)

    iterator1 = collection.create_iterator()
    iterator2 = collection.create_iterator()

    # Iterate independently
    assert iterator1.next() == book1
    assert iterator2.next() == book1
    assert iterator1.next() == book2
    assert iterator2.next() == book2

    assert not iterator1.has_next()
    assert not iterator2.has_next()

# --- Negative Tests ---

def test_next_on_empty_collection_raises_stopiteration():
    """
    Test that calling next() on an empty collection immediately raises StopIteration.
    """
    collection = BookCollection()
    iterator = collection.create_iterator()
    with pytest.raises(StopIteration):
        iterator.next()

def test_next_after_full_iteration_raises_stopiteration():
    """
    Test that calling next() after the iterator has reached the end raises StopIteration.
    """
    collection = BookCollection()
    collection.add_book(Book("The Martian", "Andy Weir"))
    iterator = collection.create_iterator()
    iterator.next() # Consume the only element
    
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.next()

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
        return self.mock_title == other.mock_title and self.mock_author == other.mock_author

class MockBookCollection(BookCollection):
    """
    A mock collection that interacts with "external" MockBook resources.
    We'll override `get_book` to simulate fetching a mock object.
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
        self._books = self._mock_data_source # Pretend these are fetched from external resource

    def get_book(self, index: int) -> MockBook:
        """
        Overrides the base method to return a MockBook, simulating an external resource.
        """
        if 0 <= index < len(self._books):
            # Simulate some "external" processing or transformation
            original_mock_book = self._books[index]
            return MockBook(f"Processed: {original_mock_book.mock_title}", original_mock_book.mock_author)
        raise IndexError("Mock book index out of bounds.")
    
    def count(self) -> int:
        """Returns the number of mock books in the collection."""
        return len(self._books)

    def create_iterator(self) -> Iterator:
        """
        Creates and returns a concrete iterator for this mock collection.
        The iterator should work with the mock's `get_book` method.
        """
        return BookIterator(self) # Reusing the original BookIterator

def test_iterator_with_mock_object():
    """
    Test the iterator's logic when the underlying collection interacts
    with a 'mock' external resource (simulated by MockBookCollection).
    """
    mock_collection = MockBookCollection()
    iterator = mock_collection.create_iterator()

    # Expected books based on the mock_collection's `get_book` logic
    expected_processed_books = [
        MockBook("Processed: Mock Book 1", "Mock Author A"),
        MockBook("Processed: Mock Book 2", "Mock Author B"),
        MockBook("Processed: Mock Book 3", "Mock Author C"),
    ]
    
    actual_processed_books = []
    while iterator.has_next():
        actual_processed_books.append(iterator.next())
    
    assert len(actual_processed_books) == len(expected_processed_books)
    for actual, expected in zip(actual_processed_books, expected_processed_books):
        assert actual.mock_title == expected.mock_title
        assert actual.mock_author == expected.mock_author
    
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        iterator.next()
