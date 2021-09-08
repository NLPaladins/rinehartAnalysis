import urllib

rinehartURLs = {
    "The_Circular_Staircase": "https://www.gutenberg.org/files/434/434-0.txt",
    "The_Man_in_Lower_Ten": "https://www.gutenberg.org/files/1869/1869-0.txt", 
    "The_Breaking_Point": "https://www.gutenberg.org/files/1601/1601-0.txt", 
    "Oh,_Well,_You_Know_How_Women_Are!": "https://www.gutenberg.org/cache/epub/24259/pg24259.txt",
    "The_Window_at_the_White_Cat": "https://www.gutenberg.org/cache/epub/34020/pg34020.txt",
    "The_Amazing_Interlude": "https://www.gutenberg.org/cache/epub/1590/pg1590.txt",
    "Dangerous_Days": "https://www.gutenberg.org/files/1693/1693-0.txt", 
    "The_Case_of_Jennie_Brice": "https://www.gutenberg.org/cache/epub/11127/pg11127.txt", 
    "The_After_House":"https://www.gutenberg.org/files/2358/2358-0.txt", 
    "The_Street_of_Seven_Stars": "https://www.gutenberg.org/files/1214/1214-0.txt", 
    "When_a_Man_Marries":"https://www.gutenberg.org/files/1671/1671-0.txt", 
    "Locked_Doors": "https://www.gutenberg.org/files/54273/54273-0.txt", 
    "The_Bat":"https://www.gutenberg.org/cache/epub/2019/pg2019.txt", 
    "The_Confession": "https://www.gutenberg.org/cache/epub/1963/pg1963.txt",
    "Bab:_A_Sub-Deb": "https://www.gutenberg.org/cache/epub/366/pg366.txt", 
    "Tenting_To-night":"https://www.gutenberg.org/cache/epub/19475/pg19475.txt",
    "Long_Live_the_King": "https://www.gutenberg.org/files/2714/2714-0.txt", 
    "Affinities and Other Stories": "https://www.gutenberg.org/cache/epub/41408/pg41408.txt", 
    "Sight_Unseen":"https://www.gutenberg.org/files/1960/1960-0.txt",
    "Tish,_The_Chronicle_of_Her_Escapades_and_Excursions": "https://www.gutenberg.org/cache/epub/3464/pg3464.txt", 
    "A_Poor_Wise_Man": "https://www.gutenberg.org/files/1970/1970-0.txt", 
    "The_Truce_of_God": "https://www.gutenberg.org/cache/epub/14573/pg14573.txt", 
    "More_Tish": "https://www.gutenberg.org/cache/epub/19851/pg19851.txt", 
    "Where_There's_A_Will": "https://www.gutenberg.org/cache/epub/330/pg330.txt", 
    "K": "https://www.gutenberg.org/files/9931/9931-0.txt"
}

def readBookFromProjGut(bookKey:str='The_Circular_Staircase'):
    req = urllib.request.Request(rinehartURLs[bookKey])
    client = urllib.request.urlopen(req)
    page = client.read()
    return page.decode('utf-8')