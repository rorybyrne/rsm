from msr.model import URL
from msr.service.url_service import UrlService


def test_store_url():
    """The URL service should store a URL"""
    url = URL('https://howdy.doody')
    service = UrlService()
    service.store_url(url)

    urls = service.registry.get_all()
    assert urls[0].href == url.href

    service.registry.clear()
    assert not service.registry._storage_exists()


def test_allow_repeat_urls():
    """The URL service should not raise an exception when repeat URLs are stored"""
    url = URL('https://howdy.doody')
    service = UrlService()
    service.store_url(url)
    service.store_url(url)

    urls = service.registry.get_all()
    assert len(urls) == 1

    service.registry.clear()
    assert not service.registry._storage_exists()


def test_fetch_urls():
    service = UrlService()
    urls = [
        URL('https://howdy.doody/index.html'),
        URL('https://foo.bar/index.html'),
        URL('https://bar.baz/index.html'),
    ]

    for url in urls:
        service.store_url(url)

    urls = service.fetch_urls()
    assert urls[0].domain == 'howdy.doody'
    service.registry.clear()
