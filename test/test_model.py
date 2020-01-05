import pytest

from qidian.models import Book
from qidian.models import Chapter
from qidian.models import Volume


@pytest.mark.parametrize("l, r",
                         [
                             (Book.id, Volume.from_book),
                             (Book.id, Chapter.from_book),
                             (Volume.id, Chapter.from_volume)
                         ])
def test_column_types(l, r):
    assert type(l) == type(r)
