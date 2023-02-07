import requests
from Samplas.open_json import open_json


SERVER_STATIC = "http://static-maps.yandex.ru/1.x/"
SERVER_GEOCODE = "http://geocode-maps.yandex.ru/1.x/"
SERVER_SEARCH = "https://search-maps.yandex.ru/v1/"


def geocode(geocode: str, sco="latlong", kind="house", format="json"):
    """
    :param geocode: str
    :param sco: longlat - долгота, широта, latlong - широта, долгота
    :param kind: house, street, metro, district, locality
    :param format: json, xml
    :return: dict
    """

    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"

    geo_params = {
        "geocode": geocode,
        "apikey": apikey,
        "sco": sco,
        "kind": kind,
        "format": format
    }

    response = requests.get(SERVER_GEOCODE, geo_params).json()
    features = response["response"]["GeoObjectCollection"]["featureMember"]
    open_json(features[0]["GeoObject"])
    return response


def get_coordinates(address):
    toponym = geocode(address, sco="latlong")
    if not toponym:
        return None, None

    toponym_coordinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = f"{dx},{dy}"

    return ll, span


def get_photo(point: str, spn="0.05,0.05", type_photo="map", sco="latlong"):
    photo_params = {
        "ll": point,
        "sco": sco,
        "spn": spn,
        "l": type_photo
    }
    response = requests.get(SERVER_STATIC, params=photo_params)
    return response


if __name__ == "__main__":
    ...
