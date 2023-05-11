from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import Torrent

import os


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
