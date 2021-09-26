import urllib.request
from nlp_libs import Configuration, ColorizedLogger
from copy import deepcopy
import numpy as np
import urllib.request
import re
from typing import *

logger = ColorizedLogger(logger_name='Process Book', color='cyan')


class ProcessedBook:
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
               (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    title: str
    url: str

    # detectives: List[str]
    # suspects: List[str]
    # crime_type: str

    def __init__(self, title: str, metadata: Dict):
        """
        raw holds the books as a single string.
        clean holds the books as a list of lowercase lines starting
        # from the first chapter and ending with the last sentence.
        """
        self.title = title
        self.url = metadata['url']
        # self.detectives = metadata['detectives']
        # self.suspects = metadata['suspects']
        # self.crime_type = metadata['crime_type']
        self.raw = self.read_book_from_proj_gut(self.url)

        self.raw_lower = self.raw.lower()
        self.raw_no_new_lines = re.sub(r'\r\n', r'\n', self.raw)
        self.raw_no_new_lines_lower = re.sub(r'\r\n', r'\n', self.raw_lower)

        self.lines = self.clean_lines(raw=self.raw_no_new_lines)
        self.lines_lower = self.clean_lines(raw=self.raw_no_new_lines_lower)
        self.clean_lower, self.clean = self.get_clean_books()

    @staticmethod
    def read_book_from_proj_gut(book_url: str) -> str:
        req = urllib.request.Request(book_url)
        client = urllib.request.urlopen(req)
        page = client.read()
        return page.decode('utf-8')

    def get_clean_books(self) -> Tuple[List[str], List[str]]:
        # return self.lines_to_chapters(self.lines_lower), self.lines_to_chapters(self.lines)
        clean_chapters_capitalized = self.lines_to_chapters(self.lines)
        clean_chapters_copy_for_lower = deepcopy(clean_chapters_capitalized)

        for chapter_idx in range(len(clean_chapters_copy_for_lower)): 
            for line_idx in range(len(clean_chapters_copy_for_lower[chapter_idx])): 
                clean_chapters_copy_for_lower[chapter_idx][line_idx] = clean_chapters_copy_for_lower[chapter_idx][line_idx].lower()

        return clean_chapters_copy_for_lower, clean_chapters_capitalized

    def clean_lines(self, raw: str) -> List[str]:
        lines = re.findall(r'.*(?=\n)', raw)
        clean_lines = []
        start = False
        for line in lines:
            if re.match(r'^chapter i\.?', line, re.IGNORECASE):
                clean_lines.append(line)
                start = True
                continue
            if not start:
                continue
            if re.match(r'^\*\*\* end of the project gutenberg ebook', line, re.IGNORECASE):
                break
            if self.pass_clean_filter(line):
                clean_lines.append(line)
        return clean_lines

    def print_info(self):
        logger.info(f'The raw length of this book as a string is {len(self.raw)}')
        logger.info(f'This book has {len(self.clean)} chapters\n')
        for i, chapter in enumerate(self.clean):
            if i == 5: break
            logger.info(f'{chapter[0]} - {chapter[1]}')
            logger.info(f'There are {len(chapter)} sentences in this chapter.')
            num_words = []
            for sent in chapter:
                num_words.append(len(sent.split(' ')))
            avg_words = np.mean(num_words)
            logger.info(f'The average sentence length in this chapter is {avg_words} words\n')

    def __str__(self):
        self.print_info()

    @staticmethod
    def lines_to_chapters(lines: List[str]) -> List[str]:
        chapters = []
        sentences = []
        current_sent = ''
        add_chapter_state = 0
        for i, line in enumerate(lines):
            # add chapter as 1st sentence
            if re.match(r'^chapter [ivxlcdm]+\.?$', line, re.IGNORECASE):
                if sentences:
                    chapters.append(sentences)
                sentences = [line]
                add_chapter_state = 1
                continue
            # add chapter title as 2nd sentence
            elif add_chapter_state == 1:
                sentences.append(line)
                add_chapter_state = 2
                continue
            # If it is the first normal line add a ". " before the line so the third regex can
            # match it. Otherwise it's unmatchable.
            if add_chapter_state == 2:
                line = '. ' + line
                add_chapter_state = 3

            sents = re.findall(r'\s*(?:(?=[“”])(?:(.*?”(?:mr\.|mrs.|[^\.\?!])*(?<!mr)(?<!mrs))[\.\?!])|(?![“”])(?:((?:mr\.|mrs.|[^\.\?!])*(?<!mr)(?<!mrs))[\.\?!]))',
                               line,
                               re.IGNORECASE)
            # if no sentence end is detected
            if not sents:
                if current_sent == '':
                    current_sent = line
                else:
                    current_sent += ' ' + line
            # if at least one sentence end is detected
            else:
                for group in sents:
                    if group[0] is None or group[0] == '':
                        group = group[1]
                    else:
                        group = group[0]
                    if current_sent != '':
                        current_sent += ' ' + group
                        sentences.append(current_sent)
                    elif group != '':
                        sentences.append(group)
                    current_sent = ''

                # set the next sentence to its start if there is one
                sent_end = re.search(r'(?<!mr)(?<!mrs)(?:(?:[\.\?!] )(?:(?:(?![“”])((?:mr\.|mrs\.|[^\.\?!]|[\.\?!]”)*))|(?:(?=[“”])([^”]*?”*(?:mr\.|mrs\.|[^\.\?!])*))))$',
                                     line,
                                     re.IGNORECASE)
                if sent_end is not None:
                    sent_end_groups = sent_end.groups()
                    if sent_end_groups[0] is None:
                        current_sent = sent_end.groups()[1]
                    else:
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

    @staticmethod
    def get_characters_per_chapter(chapter):
        found_character_list = []
        singular_or_multiple_names = '[A-Z][a-z][A-Z]?[a-z][A-Z]?[a-z]+(?:(?:\s|,|.|\.\s)[A-Z][a-z][A-Z]?[a-z][A-Z]?[a-z]+)?(?:\s[A-Z][a-z][A-Z]?[a-z][A-Z]?[a-z]+)?(?:\s[A-Z][a-z][A-Z]?[a-z][A-Z]?[a-z]+)?'
        # TODO: Executive decision occurred on the search string to ignore the
        #       first word of each sentence as regex cannot differentiate between
        #       a singular word and a name.  However, this does introduce a curious
        #       thing with McKnight in the man in the lower ten, such that we get him
        #.      as "Knight".
        search_string = re.compile(fr'(?<!“)(?<!‘)(?<!^)({singular_or_multiple_names})')
        #get characters per sentence in chapter
        for sentence in chapter:
            res = re.findall(search_string, sentence)
            found_character_list.append(res)

        unique_characters = list(np.concatenate(found_character_list))
        return found_character_list, unique_characters


    def get_all_characters_per_novel(self):
        preceding_words_to_ditch = [
            'After', 'Although', 'And', 'As', 'At',
            'Before', 'Both', 'But', 'Did', 'For',
            'Good', 'Had', 'Has', 'Home', 'If', 'Is',
            'Leaving', 'Like', 'No', 'Nice', 'Old', 'On', 'Or',
            'Poor', 'Send', 'So', 'That', 'Tell', 'The', 'Thank',
            'To', 'Was', 'Whatever', 'When', 'Where', 'While',
            'With', 'Your', 'View',
            #Specific Places
            'African', 'Brewing', 'Hospital', 'Zion', 'New', 'Country',
            'Greenwood', 'Western', 'American', 'Bar', 'Chestnut', 'Queen',
            'Summitville', 'Union', 'City', "Japan", "Europe", "Company",
            "Street", "Station", "Bank", "Weekly", "ville", "Providence",
            "Creek", "Brewing", 'California', 'Italian', 'London', 'French',
            'Scotland'
        ]

        book_by_chapter =self.clean

        totalUniqueList = []
        characterProgressionList = []
        for chapter in book_by_chapter:

            characterProgression, uniqueCharacters = self.get_characters_per_chapter(chapter)

            characterProgressionList.append(characterProgression)
            totalUniqueList = [*totalUniqueList, *uniqueCharacters]

        totalUnique = set(totalUniqueList)

        joined_preceding_words_to_lose = '|'.join(preceding_words_to_ditch)
        #not even preceding - just ditch them if they're within the "name"
        preceding_word_to_lose_regex = fr'^(?!.*({joined_preceding_words_to_lose})).*'
        regex = re.compile(preceding_word_to_lose_regex)

        filtered_people = list(filter(regex.match, totalUnique))

        return filtered_people, characterProgressionList


    def get_chapter(self, chapter: int, lower=True) -> str:
        if lower:
            return self.clean_lower[chapter - 1]
        else:
            return self.clean[chapter - 1]

    def extract_character_names(self, lower=True):
        if lower is True:
            lines_by_chapter = self.lines_to_chapters(self.lines_lower)
        else:
            lines_by_chapter = self.lines_to_chapters(self.lines)
        for chapter in lines_by_chapter:
            print(chapter)
