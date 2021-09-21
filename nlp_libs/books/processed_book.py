import urllib.request
import re
from typing import *


class ProcessedBook:
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
               (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    url: str
    detectives: List[str]
    suspects: List[str]
    crime_type: str

    def __init__(self, title, metadata: Dict, make_lower: bool = True):
        """
        raw holds the books as a single string.
        clean holds the books as a list of lowercase lines starting
        from the first chapter and ending with the last sentence.
        """
        self.url = metadata['url']
        self.detectives = metadata['detectives']
        self.suspects = metadata['suspects']
        self.crime_type = metadata['crime_type']
        self.raw = self.read_book_from_proj_gut(self.url)
        self.clean = self.get_clean_book(make_lower)

    @staticmethod
    def read_book_from_proj_gut(book_url: str) -> str:
        req = urllib.request.Request(book_url)
        client = urllib.request.urlopen(req)
        page = client.read()
        return page.decode('utf-8')

    def get_clean_book(self, make_lower: bool = True) -> List[str]:
        if make_lower:
            lines = self.raw.lower()
        else:
            lines = self.raw
        lines = lines.replace('\r\n', '\n')
        lines = lines.split('\n')
        clean = []
        start = False
        for line in lines:
            if re.match(r'^chapter i\.', line):
                clean.append(line)
                start = True
                continue
            if not start:
                continue
            if re.match(r'^\*\*\* end of the project gutenberg ebook', line):
                break
            if self.pass_clean_filter(line):
                clean.append(line)
        return clean

    @staticmethod
    def pass_clean_filter(line: str) -> bool:
        # removing the illustration lines and empty lines
        # can add other filters here as needed
        if line == '' or re.match(r'illustration:|\[illustration\]', line):
            return False
        else:
            return True

    @classmethod
    def num_to_roman(cls, num: int) -> str:
        roman = ''
        while num > 0:
            for i, r in cls.num_map:
                while num >= i:
                    roman += r
                    num -= i
        return roman

    def get_chapter(self, chapter: int) -> List[str]:
        # takes an integer chapter and returns the
        # corresponding chapter contents as a list of lines
        roman = self.num_to_roman(chapter).lower()
        start_line = '^chapter ' + roman + '.$'
        chapter = []

        start = False
        for line in self.clean:
            if re.match(start_line, line):
                chapter.append(line)
                start = True
                continue
            elif start:
                if re.match(r'^chapter [ivxlcdm]+\.$', line):
                    break
                else:
                    chapter.append(line)

        return chapter

    def get_full_names(self, chapter: int = None) -> List[str]:
        if chapter is None:
            doc = self.clean
        else:
            doc = self.get_chapter(chapter)

        full_names = []
        name_regex = r'[A-Z][a-z]+\s[A-Z][a-z]'
        for line in doc:
            print(line)
            if re.match(name_regex, line):
                full_names.append(line)

        return full_names

