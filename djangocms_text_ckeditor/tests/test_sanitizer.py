# -*- coding: utf-8 -*-
import html5lib

from django.test import TestCase
from html5lib import treebuilders

from .. import html
from .. import sanitizer
from .. import settings


class SanitizerTestCase(TestCase):

    def setUp(self):
        self.allow_token_parsers = sanitizer.TextSanitizer.allow_token_parsers

    def tearDown(self):
        sanitizer.TextSanitizer.allow_token_parsers = self.allow_token_parsers

    def test_sanitizer(self):
        allowed_attrs = html5lib.sanitizer.HTMLSanitizer.allowed_attributes[:]
        sanitizer.TextSanitizer.allow_token_parsers = (html.DataAttributeParser,)
        parser = html5lib.HTMLParser(
            tree=treebuilders.getTreeBuilder("dom"),
            tokenizer=sanitizer.TextSanitizer
        )
        body = '<span data-one="1" data-two="2">some text</span>'
        body = html.clean_html(body, full=False, parser=parser)
        self.assertEqual('<span data-one="1" data-two="2">some text</span>', body)
        self.assertEqual(allowed_attrs, html5lib.sanitizer.HTMLSanitizer.allowed_attributes)

    def test_sanitizer_with_custom_token_parser(self):

        class DonutAttributeParser(sanitizer.AllowTokenParser):

            def parse(self, attribute, val):
                return attribute == 'donut'

        sanitizer.TextSanitizer.allow_token_parsers = (DonutAttributeParser,)
        parser = html5lib.HTMLParser(
            tree=treebuilders.getTreeBuilder("dom"),
            tokenizer=sanitizer.TextSanitizer
        )
        body = '<span donut="yummy">some text</span>'
        body = html.clean_html(body, full=False, parser=parser)
        self.assertEqual('<span donut="yummy">some text</span>', body)

    def test_sanitizer_without_token_parsers(self):
        sanitizer.TextSanitizer.allow_token_parsers = ()
        parser = html5lib.HTMLParser(
            tree=treebuilders.getTreeBuilder("dom"),
            tokenizer=sanitizer.TextSanitizer
        )
        body = '<span data-one="1" data-two="2">some text</span>'
        body = html.clean_html(body, full=False, parser=parser)
        self.assertEqual('<span>some text</span>', body)