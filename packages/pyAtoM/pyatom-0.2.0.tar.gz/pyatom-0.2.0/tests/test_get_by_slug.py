import pytest
from pyAtoM import *


def setup():
    pass

def tear_down():
    pass


@pytest.fixture
def setup_data():
    print("\nSetting up resources...")
    setup()
    yield
    print("\nTearing down resources...")
    tear_down()


def test_get_by_slug(setup_data):
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    slug: str = "matti-nikolai-kantokoski-b-4-1-1868-father-of-juho-john-lempi-saimi-matias-matti-all-lived-in-sudbury-area-lempi-moved-to-u-s-with-wife-maria-sofia-puska"

    item = client.get(slug)

    assert item is not None

    assert item['reference_code'] == 'ON00120 016-.1-1-2-1'
    assert item['level_of_description'] == 'Item'
    assert item['parent'] == 'canada-2'


def test_get_by_slug_fr(setup_data):
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    slug: str = "matti-nikolai-kantokoski-b-4-1-1868-father-of-juho-john-lempi-saimi-matias-matti-all-lived-in-sudbury-area-lempi-moved-to-u-s-with-wife-maria-sofia-puska"

    item = client.get(slug, sf_culture='fr')

    assert item is not None

    assert item['reference_code'] == 'ON00120 016-.1-1-2-1'
    assert item['level_of_description'] == 'Pièce'
    assert item['parent'] == 'canada-2'


def test_search(setup_data):
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    assert len(list(client.search())) == 460



def test_search_1(setup_data):
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    queries = [Query(query_value="horses")]

    assert len(list(client.search(query_terms=queries))) == 2

    queries = [Query(query_value="horses", query_field=QueryField.title)]

    assert len(list(client.search(query_terms=queries))) == 1


def test_search_2(setup_data):
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    queries = [Query(query_value="horses", query_field=QueryField.title), Query(query_value='Sudbury', query_operator=QueryOperator.or_terms, query_field=QueryField.all)]

    assert len(list(client.search(query_terms=queries))) == 231

    queries.append(Query(query_value='photograph', query_field=QueryField.all, query_operator=QueryOperator.not_terms))

    assert len(list(client.search(query_terms=queries))) == 128

    assert len(list(client.search(query_terms=queries, digital_object=True))) == 46


def test_download():
    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    f = client.download("28-hockey-arena-sudbury-photo-copyright-rideau-air-photos-ltd-seeleys-bay-ont-can")
    assert f == "007-1-1-11.jpg"