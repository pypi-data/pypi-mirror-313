__all__ = ["GalleryURLParser"]


import re


class GalleryURLParser:
    """
    A parser for extracting gallery information from URLs of exhentai.org and e-hentai.org.
    Attributes:
        gid (int): The gallery ID extracted from the URL.
        url (str): The original URL provided.
        url_key (str): The URL key extracted from the URL.
    Methods:
        __init__(url: str) -> None:
            Initializes the GalleryURLParser with the provided URL.
            Raises a ValueError if the URL is empty or not a valid gallery URL.
    """

    __slots__ = ["gid", "url", "url_key"]

    def __init__(self, url: str) -> None:
        if url == "":
            raise ValueError("The url cannot be empty.")
        else:
            if ("exhentai.org" not in url) and ("e-hentai.org" not in url):
                raise ValueError("The url is not the gallery's url.")
            self.url = url

            if "exhentai.org" in self.url:
                match = re.search(
                    r"https://exhentai\.org/g/(\d+)/([a-zA-Z0-9]+)", self.url
                )
            if "e-hentai.org" in self.url:
                match = re.search(
                    r"https://e-hentai\.org/g/(\d+)/([a-zA-Z0-9]+)", self.url
                )
            if match:
                self.gid = int(match.group(1))
                self.url_key = match.group(2)
            else:
                raise ValueError("The url is not the gallery's url.")
