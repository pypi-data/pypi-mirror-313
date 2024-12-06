# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `change-encode`: 將文件從GB2312編碼轉換為UTF-8編碼。
* `change-lang`: 將文件的語言轉換為指定的語言。

## `change-encode`

將文件從GB2312編碼轉換為UTF-8編碼。

Args:
  path (str): 文件路徑。
  output (str, optional): 轉換後的文件存放位置（默認值為“dist”）。

**Usage**:

```console
$ change-encode [OPTIONS] PATH
```

**Arguments**:

* `PATH`: [required]

**Options**:

* `--output TEXT`: [default: ./dist]
* `--help`: Show this message and exit.

## `change-lang`

將文件的語言轉換為指定的語言。

Args:
  path (str): 文件路徑。
  lang (str): 目標語言。(s2t t2s)
  output (str, optional): 轉換後的文件存放位置（默認值為“dist”）。

**Usage**:

```console
$ change-lang [OPTIONS] PATH LANG
```

**Arguments**:

* `PATH`: [required]
* `LANG`: [required]

**Options**:

* `--output TEXT`: [default: ./dist]
* `--help`: Show this message and exit.
