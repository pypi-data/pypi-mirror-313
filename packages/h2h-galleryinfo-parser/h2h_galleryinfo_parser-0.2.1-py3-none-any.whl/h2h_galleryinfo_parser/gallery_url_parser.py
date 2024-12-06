__all__ = ["GalleryURLParser"]


import re


class GalleryURLParser:
    """
    A parser class for extracting gallery information from URLs.
    Attributes:
        gid (int): The gallery ID.
        url (str): The gallery URL.
        url_key (str): The key associated with the gallery URL.
    Methods:
        __init__(): Initializes the GalleryURLParser with default values.
        gid: Property to get or set the gallery ID.
        url: Property to get or set the gallery URL. The URL must be from exhentai.org or e-hentai.org.
    Examples:
        >>> parser = GalleryURLParser()
        >>> parser.url = "https://exhentai.org/g/1234567/abcdefg"
        >>> parser.gid
        1234567
        >>> parser.url_key
        "abcdefg"
    """

    __slots__ = ["gid", "url", "url_key"]

    def __init__(self) -> None:
        self.gid = 0
        self.url = ""
        self.url_key = ""

    @property
    def gid(self) -> int:
        if self.gid == 0:
            raise ValueError("GID is not set.")
        return self.gid

    @gid.setter
    def gid(self, gid: int) -> None:
        self.gid = gid

    @property
    def url(self) -> str:
        return self.url

    @url.setter
    def url(self, url: str) -> None:
        if url != "":
            if ("exhentai.org" not in self.url) and ("e-hentai.org" not in self.url):
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
        else:
            raise ValueError("The url cannot be empty.")
