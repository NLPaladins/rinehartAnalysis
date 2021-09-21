import urllib.request
import re
from typing import *


class ProcessedBook:
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
               (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    title: str
    url: str
    detectives: List[str]
    suspects: List[str]
    crime_type: str

    def __init__(self, title: str, metadata: Dict, make_lower: bool = True):
        """
        raw holds the books as a single string.
        clean holds the books as a list of lowercase lines starting
        from the first chapter and ending with the last sentence.
        """
        self.title = title
        self.url = metadata['url']
        self.detectives = metadata['detectives']
        self.suspects = metadata['suspects']
        self.crime_type = metadata['crime_type']
        self.raw = self.read_book_from_proj_gut(self.url)
        if make_lower:
            lines = self.raw.lower()
        else:
            lines = self.raw
        lines = lines.replace('\r\n', '\n').split('\n')
        self.lines = self.clean_lines(lines=lines)
        self.clean = self.get_clean_book(make_lower=make_lower)

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
        lines = lines.replace('\r\n', '\n').split('\n')
        lines = self.clean_lines(lines)
        chapters = self.lines_to_chapters(lines)
        return chapters

    def clean_lines(self, lines: List[str]) -> List[str]:
        clean_lines = []
        start = False
        for line in lines:
            if re.match(r'^chapter i\.', line):
                clean_lines.append(line)
                start = True
                continue
            if not start:
                continue
            if re.match(r'^\*\*\* end of the project gutenberg ebook', line):
                break
            if self.pass_clean_filter(line):
                clean_lines.append(line)
        return clean_lines

    @staticmethod
    def lines_to_chapters(lines: List[str]) -> List[str]:
        chapters = []
        sentences = []
        current_sent = ''
        for i, line in enumerate(lines):
            # add chapter as 1st sentence
            if re.match(r'^chapter [ivxlcdm]+\.$', line):
                if sentences:
                    chapters.append(sentences)
                sentences = [line]
                add_chapter_title = True
                continue
            # add chapter title as 2nd sentence
            elif add_chapter_title:
                sentences.append(line)
                add_chapter_title = False
                continue
            sents = re.findall(r' *((?:mr\.|mrs.|[^\.\?!])*)(?<!mr)(?<!mrs)[\.\?!]', line)
            # if no sentence end is detected
            if not sents:
                if current_sent == '':
                    current_sent = line
                else:
                    current_sent += ' ' + line
            # if at least one sentence end is detected
            else:
                for group in sents:
                    if current_sent != '':
                        current_sent += ' ' + group
                        sentences.append(current_sent)
                    else:
                        sentences.append(group)
                    current_sent = ''
                # set the next sentence to its start if there is one
                sent_end = re.search(r'(?<!mr)(?<!mrs)[\.\?!] ((?:mr\.|mrs\.|[^\.\?!])*)$', line)
                if sent_end is not None:
                    current_sent = sent_end.groups()[0]
        return chapters

    @staticmethod
    def pass_clean_filter(line: str) -> bool:
        # removing the illustration lines and empty lines
        # can add other filters here as needed
        if line == '' or re.match(r'illustration:|\[illustration\]', line):
            return False
        else:
            return True

    def get_chapter(self, chapter: int) -> str:
        return self.clean[chapter - 1]
