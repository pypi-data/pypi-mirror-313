import base64


def get_file_contents(path: str) -> bytes:
    with open(path, "rb") as file:
        read_file = file.read()

        return base64.b64encode(read_file)


def get_filename_from_path(path: str) -> str:
    return path.split("/")[-1]
