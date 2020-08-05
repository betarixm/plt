import requests
import html

BUGS_ARTIST_SONG_LIST_URL = lambda artist_id, idx: f"https://music.bugs.co.kr/artist/{artist_id}/tracks?page={idx}"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

artists = {
    "IU": "80049126",
    "RedVelvet": "80199440",
    "AKMU": "80141499"
}

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


result = []
for key, value in artists.items():
    beka = artist_music(value)
    result += beka
    print(beka)

list_to_csv("dummy.csv", result)
