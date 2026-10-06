from processing.validation import validate_record

def valid_book():
    return {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/a",
        "name_or_title": "Book",
        "price": 10.0,
        "rating": 4,
        "author": None,
    }

def test_valid_record():
    assert validate_record(valid_book()) == []

def test_invalid_url_and_rating():
    rec = valid_book()
    rec["source_url"] = "bad"
    rec["rating"] = 6
    problems = validate_record(rec)
    assert "invalid_url" in problems
    assert "invalid_rating" in problems
