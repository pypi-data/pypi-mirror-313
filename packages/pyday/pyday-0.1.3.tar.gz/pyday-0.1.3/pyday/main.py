import typer

from .change_encode import change_file_encode
from .change_lang import change_file_lang

app = typer.Typer(no_args_is_help=True)


@app.command()
def change_encode(path: str, output: str = "./dist") -> None:
    """
    將文件從GB2312編碼轉換為UTF-8編碼。

    Args:
      path (str): 文件路徑。
      output (str, optional): 轉換後的文件存放位置（默認值為“dist”）。
    """
    try:
        change_file_encode(path, output)
    except Exception as e:
        print(str(e))


@app.command()
def change_lang(path: str, lang: str, output: str = "./dist") -> None:
    """
    將文件的語言轉換為指定的語言。

    Args:
      path (str): 文件路徑。
      lang (str): 目標語言。(s2t t2s)
      output (str, optional): 轉換後的文件存放位置（默認值為“dist”）。
    """
    try:
        change_file_lang(path, lang, output)
    except Exception as e:
        print(str(e))
