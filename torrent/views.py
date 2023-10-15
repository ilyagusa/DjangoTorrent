from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.files import File
from django.core.files.images import ImageFile

from .models import Torrent, TorrentFile

from .parser_torrent_site.parse_torrent_site import parse_film_page_by_url

import requests
import os

from bs4 import BeautifulSoup as BS

SITE_URL = "https://top-lafa.ru"


def main(request):
    """Main page"""
    torrents = Torrent.objects.all()

    return render(
        request,
        'torrent/main.html',
        {
            'title': 'Главная страница сайта',
            'torrents': torrents
        }
    )


def download(request, torrent_id: int):
    """Download torrent file"""
    torrent_obj = Torrent.objects.get(id=torrent_id)

    if not torrent_obj:
        raise Http404("Торрент не найден")

    # get the download path
    download_path = torrent_obj.file.path

    if os.path.exists(download_path):
        with open(download_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/torrent")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download_path)
            return response

    raise Http404("Торрент не найден")


def torrent(request, torrent_id):
    torrent_obj = Torrent.objects.get(id=torrent_id)

    return render(
        request,
        'torrent/torrent.html',
        {
            'title': 'Страница определенного торрента',
            'torrent': torrent_obj
        }
    )


def about(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера
    path = request.path  # получаем запрошенный путь

    return render(request, 'torrent/about.html')


def parse_site(request):
    html_page = BS(requests.get(f"{SITE_URL}/film/Komediya/").content, 'html.parser')

    for film in html_page.select(".in_cinema"):
        film_url = film.findAll("a", href=True)[0]['href']

        try:
            film_info_dict = parse_film_page_by_url(film_url)
        except Exception as ex:
            print(f"Ошибка\n{ex}")
            continue

        if not film_info_dict["Описание"]:
            continue

        new_torrent = Torrent(
            name=film_info_dict["Название"],
            type="Фильм",
            score=film_info_dict["Score"],
            genres=film_info_dict["Категория"] or "",
            description=film_info_dict["Описание"],
            info={
                "year_release": film_info_dict.get("Год выпуска"),
                "premiere": film_info_dict.get("Премьера"),
                "producer": film_info_dict.get("Режиссер"),
                "actors": film_info_dict.get("В ролях")
            },
        )

        new_torrent.image = ImageFile(open(film_info_dict["PosterPath"], "rb"))

        new_torrent.save()

        # Цикл по всем торрент-файлам и добавление их в БД по foreign_key
        torrent_files = film_info_dict.get("TorrentFiles", [])
        if len(torrent_files) > 3:
            torrent_files = torrent_files[:3]
        for torrent_file in torrent_files:
            torrent_file_size, torrent_file_path = torrent_file.get("SizeStr", ""), torrent_file.get("Path")
            torrent_file_format = torrent_file.get("Format", "")
            print(f"path_file = {torrent_file_path}, file_size = {torrent_file_size}")

            if not all((torrent_file_format, torrent_file_size, torrent_file_path,)):
                continue

            if torrent_file_path:
                new_torrent_file = TorrentFile(
                    file=File(open(torrent_file_path, "rb")),
                    size=torrent_file_size,
                    torrent=new_torrent,
                    file_format=torrent_file_format
                )

                new_torrent_file.save()
