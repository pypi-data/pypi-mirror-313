import datetime
import os
import random
import shutil
import string
import unittest

from src.galleryinfo_parser.galleryinfo_parser import parse_galleryinfo


def random_string(length: int) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits) for x in range(length)
    )


class TestGalleryInfoParser(unittest.TestCase):
    def _generate_galleryinfo(
        self, tags: str, withcomments: bool = False
    ) -> tuple[dict[str, str], str]:
        if tags == "":
            raise ValueError("tags cannot be empty")

        elements = dict[str, str]()
        elements["Title"] = random_string(10)
        elements["Upload Time"] = "2007-04-13 03:43"
        elements["Uploaded By"] = random_string(10)
        elements["Downloaded"] = "2007-08-13 03:43"
        elements["Tags"] = tags
        if withcomments:
            elements["Uploader's Comments"] = "\n" + random_string(10) + "\n"
        end = "Downloaded from E-Hentai Galleries by the Hentai@Home Downloader <3\n"

        return elements, "\n".join(
            ["\n".join([f"{key}: {value}" for key, value in elements.items()]), end]
        )

    def _assert_galleryinfo(
        self,
        gidpair: tuple[str, int],
        tagspair: tuple[str, list[tuple[str, str]]],
        withcomments: bool,
    ):
        """
        gidpair: (gallery_folder, gid)
        tagspair: (tags, tags_answer)
        """

        gallery_folder = gidpair[0]
        gid = gidpair[1]

        tags = tagspair[0]
        tags_answer = tagspair[1]

        dir_path = os.path.join(os.path.dirname(__file__), gallery_folder)
        if os.path.exists("dir_path"):
            raise FileExistsError(f"{dir_path} already exists")
        os.mkdir(dir_path)

        answer_element, txt = self._generate_galleryinfo(
            tags=tags, withcomments=withcomments
        )
        galleryinfo_path = os.path.join(dir_path, "galleryinfo.txt")
        with open(galleryinfo_path, "w") as file:
            file.write(txt)

        gallery = parse_galleryinfo(dir_path)
        shutil.rmtree(dir_path)

        self.assertEqual(gallery.gallery_name, gallery_folder)
        self.assertEqual(gallery.gid, gid)
        self.assertEqual(gallery.files_path, ["galleryinfo.txt"])
        self.assertEqual(
            gallery.modified_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(gallery.title, answer_element["Title"])
        self.assertEqual(gallery.upload_time, answer_element["Upload Time"])
        self.assertEqual(gallery.upload_account, answer_element["Uploaded By"])
        self.assertEqual(gallery.download_time, answer_element["Downloaded"])
        if withcomments:
            self.assertEqual(
                gallery.galleries_comments, answer_element["Uploader's Comments"][1:-1]
            )
        else:
            self.assertEqual(gallery.galleries_comments, "")
        self.assertEqual(gallery.tags, tags_answer)

    def test_gid(self):
        tagspair = ("tag1:value1", [("tag1", "value1")])
        self._assert_galleryinfo(("1", 1), tagspair, False)
        self._assert_galleryinfo(("[1] [3]", 3), tagspair, False)
        self._assert_galleryinfo(("1 [3]", 3), tagspair, False)
        self._assert_galleryinfo(("[1 [3]", 3), tagspair, False)
        self._assert_galleryinfo(("1] [3]", 3), tagspair, False)

    def test_tags(self):
        gidpair = ("1", 1)
        self._assert_galleryinfo(gidpair, ("tag1:value1", [("tag1", "value1")]), False)
        self._assert_galleryinfo(
            gidpair,
            ("tag1:value1, tag1:value2", [("tag1", "value1"), ("tag1", "value2")]),
            False,
        )
        self._assert_galleryinfo(gidpair, ("value1", [("untagged", "value1")]), False)
        self._assert_galleryinfo(
            gidpair,
            ("tag1:value1, tag2:value2", [("tag1", "value1"), ("tag2", "value2")]),
            False,
        )
        self._assert_galleryinfo(
            gidpair,
            ("tag1:value1, value2", [("tag1", "value1"), ("untagged", "value2")]),
            False,
        )

    def test_comments(self):
        gidpair = ("1", 1)
        tagspair = ("tag1:value1", [("tag1", "value1")])
        self._assert_galleryinfo(gidpair, tagspair, False)
        self._assert_galleryinfo(gidpair, tagspair, True)
