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
