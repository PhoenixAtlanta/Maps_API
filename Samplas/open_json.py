import json


def open_json(data: json, name_file="geo_data.json"):
    name_file = name_file
    try:
        with open(name_file, "w", encoding="utf8") as file:
            json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        print(e, "\n", e.__class__.__name__)


if __name__ == "__main__":
    ...
