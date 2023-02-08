import requests
from Samplas.open_json import open_json


SERVER_STATIC = "http://static-maps.yandex.ru/1.x/"
SERVER_GEOCODE = "http://geocode-maps.yandex.ru/1.x/"
SERVER_SEARCH = "https://search-maps.yandex.ru/v1/"


def geocode(geocode: str, sco="latlong", kind="house", format="json"):  # запрос
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
    # open_json(response)
    features = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return features


def get_coordinates(address):
    toponym = geocode(address, sco="latlong")
    if not toponym:
        return None, None

    toponym_coordinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = map(float, toponym_coordinates.split(" "))

    # Собираем координаты в параметр ll
    ll = (toponym_longitude, toponym_lattitude)

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = (dx, dy)

    return ll, span


def get_photo(point: str, spn="0.05,0.05", type_photo="map", mark=""):  # получить фото
    request = f"{SERVER_STATIC}?ll={point}&spn={spn}&l={type_photo}&pt={mark}"
    # print(request)
    response = requests.get(request)
    return response


def change_spn(spn: tuple, value: int) -> tuple:  # изменить spn
    coef = 1.1
    if value < 0:
        coef = 0.5
    spn = (spn[0] + value * spn[0] * coef, spn[1] + value * spn[1] * coef)
    spn = (spn[0] if spn[0] > 0.001 else 0.001, spn[1] if spn[1] > 0.001 else 0.001)
    return spn


def change_ll(ll: tuple, spn: tuple, value: tuple):  # изменить координаты
    ll = ll[0] + spn[0] * value[0] * 2, ll[1] + spn[1] * value[1] * 2
    return ll


if __name__ == "__main__":
    ...
