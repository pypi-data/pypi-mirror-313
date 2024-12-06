from pathlib import Path

from .utils.fileIO import output_file


def change_file_encode(in_path: str, output: str = "./dist") -> None:
    path = Path(in_path)
    if path.is_file():
        file = path.open(encoding="gb2312")
        data: str = file.read()
        output_file(path.name, data, output)
    elif path.is_dir():
        for p in path.iterdir():
            _path = Path(p)
            change_file_encode(_path, f"{output}/{_path.parent}")
    else:
        print("No File or Folder")
