from pathlib import Path

from opencc import OpenCC

from .utils.fileIO import output_file


def change_file_lang(in_path: str, lang: str, output: str = "./dist") -> None:
    path = Path(in_path)
    if path.is_file():
        try:
            file = path.open()
            data: str = file.read()
            # print("change file langauge:", path)
            data_opencc: str = OpenCC(lang).convert(data)
            output_file(path.name, data_opencc, output)
        except UnicodeDecodeError as e:
            print(f"error: {path} | can't change byte")
        except Exception as e:
            print(f"error: {path} | {e}")

    elif path.is_dir():
        for p in path.iterdir():
            _path = Path(p)
            change_file_lang(_path, lang, f"{output}/{_path.parent}")
    else:
        print("No File or Folder")


def change_json_value(data: dict, lang: str = "s2t") -> dict:
    cc = OpenCC(lang)
    for key in data:
        data[key] = cc.convert(data[key])
    return data

    """
    opencc
    hk2s: Traditional Chinese (Hong Kong standard) to Simplified Chinese
    s2hk: Simplified Chinese to Traditional Chinese (Hong Kong standard)
    s2t: Simplified Chinese to Traditional Chinese
    s2tw: Simplified Chinese to Traditional Chinese (Taiwan standard)
    s2twp: Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)
    t2hk: Traditional Chinese to Traditional Chinese (Hong Kong standard)
    t2s: Traditional Chinese to Simplified Chinese
    t2tw: Traditional Chinese to Traditional Chinese (Taiwan standard)
    tw2s: Traditional Chinese (Taiwan standard) to Simplified Chinese
    tw2sp: Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)
    """
