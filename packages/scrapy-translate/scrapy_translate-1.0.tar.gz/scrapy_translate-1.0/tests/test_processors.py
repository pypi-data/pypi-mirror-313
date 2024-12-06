import unittest

from scrapy_translate.processors import (
    extract_text_from_html,
    inject_text_into_html,
)


class TestProcessors(unittest.TestCase):
    def test_html_processor(self):
        html = '<p>Hello, <strong>World!</strong><br><img src="img.png"></p>'
        result = inject_text_into_html(html, extract_text_from_html(html))
        self.assertEqual(html, result)
