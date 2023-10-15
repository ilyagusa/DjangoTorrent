import requests
import uuid

from bs4 import BeautifulSoup as BS

SITE_URL = "https://top-lafa.ru"


def _upd_info_from_details_tbl(film_html: BS, film_info_dict: dict):
    """
    Update film_info_dict by value from detail_table

    :param film_html: HTML page with film
    :param film_info_dict: dict with info about the film
    """
    film_details_tbl_node = film_html.select(".detail_tbl")[0]

    keys_node, values_node = film_details_tbl_node.select(".leftrow"), film_details_tbl_node.select(".rightrow")

    for key, value in zip(keys_node, values_node):

        if key.string == "Название:":
            res_value = value.findAll("span")[0].string
        elif key.string == "Категория:":
            res_value = []

            for a in value.findAll("a"):
                res_value.append(a.string)
        elif key.string == "Режиссер:":
            res_value = value.findAll("a")[0].string
        elif key.string == "В ролях:":
            res_value = []

            for span in value.findAll("span"):
                res_value.append(span.string)
        else:
            res_value = value.string

        film_info_dict[key.string.replace(":", "")] = res_value

        if film_info_dict.get("Категория"):
            film_info_dict["Категория"].sort()

def _upd_info_by_film_descr(film_html: BS, film_info_dict: dict):
    """
    Update film_info_dict by value from description

    :param film_html: HTML page with film
    :param film_info_dict: dict with info about the film
    :return:
    """
    film_description_node = film_html.select(".span_descr")[0]

    if film_description_node.string:
        film_info_dict["Описание"] = film_description_node.string.strip()
    else:
        film_info_dict["Описание"] = ""


def _upd_info_by_poster_img(film_html: BS, film_info_dict: dict):
    """
    Update film_info_dict by value from poster image

    :param film_html: HTML page with film
    :param film_info_dict: dict with info about the film
    :return:
    """
    film_poster_node = film_html.select(".c_pic_col")[0]
    film_poster_url = film_poster_node.findAll("img")[0]["src"]

    film_poster_html = requests.get(SITE_URL + film_poster_url)
    file_poster_path = "E:\labs\DjangoTorrent\django_torrent\media\\" + film_poster_url.split("/")[-1]
    print(f"URL_FILMS = {film_poster_url.split('/')[-1]}")

    with open(file_poster_path, "wb") as poster_file:
        print(file_poster_path)
        poster_file.write(film_poster_html.content)

    film_info_dict["PosterPath"] = file_poster_path


def _upd_info_by_torrent_files(film_html: BS, film_info_dict: dict):
    """
    Update film_info_dict from torrent_files table

    :param film_html: HTML page with film
    :param film_info_dict: dict with info about the film
    :return:
    """
    film_info_dict["TorrentFiles"] = []

    torrent_table = film_html.select(".ts_film")[0]

    for value_tag in torrent_table.findAll('tr'):
        torrent_file_info = {}

        for torrent_file_detail_tag in value_tag.findAll("td"):
            torrent_file_detail_str = torrent_file_detail_tag.string

            if torrent_file_detail_str:
                if "MB" in torrent_file_detail_str or "GB" in torrent_file_detail_str:
                    torrent_file_info["SizeStr"] = torrent_file_detail_str
                if torrent_file_detail_str.upper() in ('MKV', 'AVI', 'BDMV', 'MKV', 'MP4'):
                    torrent_file_info["Format"] = torrent_file_detail_str.upper()

        torrent_file_url_tag = value_tag.select('.dlink_t', href=True)

        if not torrent_file_info.get("Format"):
            continue

        if torrent_file_url_tag:
            torrent_file_html = requests.get(SITE_URL + torrent_file_url_tag[0]["href"])

            torrent_file_path = "E:\labs\DjangoTorrent\django_torrent\media\\torrent\\" + film_info_dict["URL"].split("/")[-1][:-4] + "_" + str(uuid.uuid4())[0:5] + ".torrent"

            with open(torrent_file_path, "wb") as poster_file:
                poster_file.write(torrent_file_html.content)
                torrent_file_info["Path"] = torrent_file_path

            film_info_dict["TorrentFiles"].append(torrent_file_info)


def _upd_info_by_score(film_html: BS, film_info_dict: dict):
    """
    Update film_info_dict from score rating

    :param film_html: HTML page with film
    :param film_info_dict: dict with info about the film
    :return:
    """
    score_kinopoisk = film_html.findAll("meta", {"itemprop": "ratingValue"})
    film_info_dict["Score"] = score_kinopoisk[0]["content"]


def parse_film_page_by_url(film_url: str) -> dict:
    """
    Parse film page by url

    :param film_url
    :return: film_info_dict
    """
    print(SITE_URL + film_ur)

    film_html = BS(requests.get(SITE_URL + film_url).content, 'html.parser')

    film_info_dict = {"URL": film_url}

    _upd_info_from_details_tbl(film_html, film_info_dict)
    _upd_info_by_film_descr(film_html, film_info_dict)
    _upd_info_by_poster_img(film_html, film_info_dict)
    _upd_info_by_torrent_files(film_html, film_info_dict)
    _upd_info_by_score(film_html, film_info_dict)

    print(film_info_dict)
    return film_info_dict

print(1)

parse_film_page_by_url("/film/Uzhasi/perl1.htm")