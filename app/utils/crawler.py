import requests
import html
from bs4 import BeautifulSoup

BUGS_ARTIST_SONG_LIST_URL = lambda artist_id, idx: f"https://music.bugs.co.kr/artist/{artist_id}/tracks?page={idx}"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

artists = {
    "IU": "80049126",
    "RedVelvet": "80199440",
    "AKMU": "80141499"
}


def refine(target: str):
    return '"' + target.lower().replace(" ", "_").replace("'", "").replace('"', "").replace("(", "").replace(')', "").replace("-","_").replace("to_","") + '",'


def artist_music(artist_id):
    res = requests.get(BUGS_ARTIST_SONG_LIST_URL(artist_id, 1), headers=header)
    t = res.text
    num_page = t.count("javascript:void(retrieveTrackPage(")
    result = []
    for i in range(1, num_page + 1):
        res = requests.get(BUGS_ARTIST_SONG_LIST_URL(artist_id, i), headers=header)
        t = html.unescape(res.text)
        l = t.split('<th scope="row">')[1:-1]
        for song in l:
            k = song.split('title="')[1].split('"')[0]
            result.append(k)

    return result


def list_to_csv(filename, list):
    with open(filename, "a") as f:
        for i in list:
            f.write(f"{i}\n")


def animal_furniture():
    TARGET_URL = "https://gamewith.net/animal-crossing-new-horizons/article/show/17525"
    res = requests.get(TARGET_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('tr > td')[4::3]

    return [refine(i.text.strip()) for i in items]


def animal_character():
    TARGET_URL = "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)"

    res = requests.get(TARGET_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('b > a')[1:]
    return [refine(i.text.strip()) for i in items]


def adjective():
    TARGET_URL = "https://www.talkenglish.com/vocabulary/top-500-adjectives.aspx"
    res = requests.get(TARGET_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('td > a')[2:]
    return [refine(i.text.strip()) for i in items]

