import os
from html.parser import HTMLParser
import unittest


class ImgSrcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_srcs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            attr_dict = dict(attrs)
            src = attr_dict.get("src")
            if src:
                self.img_srcs.append(src)


class AssetTests(unittest.TestCase):
    def test_img_sources_exist(self):
        html_file = os.path.join(os.path.dirname(__file__), os.pardir, "index.html")
        html_file = os.path.normpath(html_file)
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        parser = ImgSrcParser()
        parser.feed(content)
        self.assertGreater(len(parser.img_srcs), 0, "No <img> tags found in HTML")
        project_root = os.path.dirname(html_file)
        for src in parser.img_srcs:
            # Remove leading './' or '/'
            normalized_src = src.lstrip("./")
            self.assertTrue(normalized_src.startswith("assets/"), f"Image src {src} not in assets/")
            asset_path = os.path.join(project_root, normalized_src)
            self.assertTrue(os.path.isfile(asset_path), f"Asset not found: {src}")


if __name__ == "__main__":
    unittest.main()
