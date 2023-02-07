import os


def open_image(data, image_name="map_image.png"):
    with open(image_name, "wb") as file:
        file.write(data.content)


def close_image(image_name="mao_image.png"):
    os.remove(image_name)


if __name__ == "__main__":
    ...
