import re
from typing import *
import numpy as np

def createNamedDictionary(personList):
    personList.sort(key=len, reverse=True)
    name_dictionary = {}
    hasKey = False

    for potential_name_key in personList:
        title = re.findall(r'^(?:Mr\.|Mrs\.|Miss|Doctor)', potential_name_key)
        name_split_no_title = re.findall(r'(?!Mr\.|Mrs\.|Miss|Doctor)[A-Z][a-z]+', potential_name_key)
        original_length_no_title = len(name_split_no_title)

        if len(name_split_no_title) > 1:
            surname = name_split_no_title[1]
            name_split_no_title = [name_split_no_title[0]]

        print(len(name_split_no_title))
        print(name_split_no_title)
        for name in personList:
            if name in name_dictionary.keys() or (len(name_dictionary.values()) > 0 and
                                                  name in np.concatenate(
                        list(name_dictionary.values()))):
                print("Continuing on ", name)
                continue

            if re.match(fr".*({'|'.join(name_split_no_title)}).*", name):
                #                 print('\t ',re.match(fr".*({'|'.join(name_split_no_title)}).*", name))

                if original_length_no_title == 1:
                    continue

                if len(name) > len(potential_name_key):
                    raise ("This shouldn't happen with the way the sorting works")
                else:
                    if potential_name_key not in name_dictionary.keys() and name not in name_dictionary.keys():
                        print('\t Key:', potential_name_key, "\t\t Value: ", potential_name_key, )
                        name_dictionary[potential_name_key] = [potential_name_key]
                    elif potential_name_key in name_dictionary.keys():
                        print('\t Key:', potential_name_key, "\t\t Value: ", name)
                        print('\tt name_split_no_title: ', name_split_no_title)
                        if re.match(fr'.*(?!{surname}).*$', name) and len(name_split_no_title) == len(
                                re.findall(r'(?!Mr\.|Mrs\.|Miss|Doctor)[A-Z][a-z]+', name)):
                            print('\t\t >>>>>>>>>>>. SURNAME DOES NOT MATCH!!!')
                            print('\t\t >>>>>>>>>>>.potential_name_key, name')

                        name_dictionary[potential_name_key] = [
                            *name_dictionary[potential_name_key],
                            name
                        ]

                    #                     print('key: ', potential_name_key, '\tvalue', potential_name_key)
                #                     name_dictionary[potential_name_key] = [ potential_name_key ]
                continue

    return name_dictionary


def extract_surnames(unique_person_list):
    surname_list = []
    names_to_ignore = ['Anne']
    # first pass: go through, get break of first / lasts
    for name in unique_person_list:
        name_split_no_title = re.findall(r'(?!Mr\.|Mrs\.|Miss|Doctor)[A-Z][a-z]+', name)
        surname = '' if len(name_split_no_title) == 1 else name_split_no_title[1]

        if surname != '' and surname not in names_to_ignore:
            surname_list.append(surname)

    return set(surname_list)


def get_unambiguous_name_list(unique_person_list, surname_list):
    unambiguous_name_list = []
    for name in unique_person_list:
        name_split_no_title = re.findall(r'(?!Mr\.|Mrs\.|Miss|Doctor)[A-Z][a-z]+', name)
        first_name = name_split_no_title[0]

        if first_name not in surname_list:
            unambiguous_name_list.append(name)
        else:
            print(f"Name {name} is ambiguous. Not processing")
    return unambiguous_name_list


def create_named_dictionary(unique_person_list):
    title_regex = r'^(?:Mr\.|Mrs\.|Miss|Doctor)'
    no_title_regex = r'(?!Mr\.|Mrs\.|Miss|Doctor)[A-Z][a-z]+'
    unique_person_list.sort(key=len, reverse=True)
    unique_person_key = {}
    name_dictionary = {}

    surname_list = extract_surnames(unique_person_list)
    unambiguous_person_list = get_unambiguous_name_list(unique_person_list, surname_list)

    alias_dictionary = createNamedDictionary(unambiguous_person_list)

    return alias_dictionary

def get_earliest_chapter_sentence_from_name_lists(book, name_lists, n=0, first=True):
    '''
    Takes in a list of lists, where
    each list in this list of lists is a
    list of aliases for a single character.
    
    Returns a dictionary with character names
    as keys and a list with chapter number as
    the first element and sentence number as the
    second element.
    '''
    first_mentioned = {}
    for idx, aliases in enumerate(other_suspects):
        alias_matcher = '|'.join(aliases)
        found_match = False
        for chapter_num, chapter in enumerate(book.clean):
            for sent_num, sentence in enumerate(chapter[2:]):
                match = re.search(alias_matcher, sentence)
                if match:
                    if not found_match:
                        first_mentioned[aliases[0]] = [chapter_num + 1, sent_num + 1, []]
                    found_match = True
                    if n > 0:
                        words = get_n_words(book, alias_matcher, chapter_num, sent_num, n)
                        first_mentioned[aliases[0]][-1].append(words)
                    if first:
                        break
            if first and found_match:
                break
    return first_mentioned

def get_n_words(book, alias_matcher, chapter_num, sent_num, n):
    sents = ' '.join(book.clean[chapter_num][sent_num + 1: sent_num + 4])
    words = re.search('((?:\S+ ){0,' + str(n) + '}\S?(?:' + alias_matcher + ')\S?(?: \S+){0,' + str(n) + '})', sents).group(0)
    return words

def get_co_occurences(book, name_lists, n_sents=2):
    assert len(name_lists) == 2
    mentions_a, mentions_b = {}, {}
    dets, perp = name_lists[0], name_lists[1]
    dets_matcher = '|'.join(dets)
    perp_matcher = '|'.join(perp)
    for chapter_num, chapter in enumerate(book.clean):
        mentions_a[chapter_num] = []
        mentions_b[chapter_num] = []
        for sent_num, sentence in enumerate(chapter[2:]):
            match_a = re.search(dets_matcher, sentence)
            match_b = re.search(perp_matcher, sentence)
            if match_a:
                mentions_a[chapter_num].append(sent_num)
            if match_b:
                mentions_b[chapter_num].append(sent_num)
    co_occurences = []
    for chapter_a, sent_nums_a in mentions_a.items():
        for chapter_b, sent_nums_b in mentions_b.items():
            if chapter_a == chapter_b:
                for sent_num_a in sent_nums_a:
                    for sent_num_b in sent_nums_b:
                        if sent_num_a > sent_num_b and sent_num_a - sent_num_b <= n_sents:
                            sents = book.clean[chapter_a][2:][sent_num_b:sent_num_a+1]
                            co_occurences.append([chapter_a, sent_num_b, sent_num_a, sents])
                        if sent_num_b > sent_num_a and sent_num_b - sent_num_a <= n_sents:
                            sents = book.clean[chapter_a][2:][sent_num_a:sent_num_b+1]
                            co_occurences.append([chapter_a, sent_num_a, sent_num_b, sents])
    return co_occurences
