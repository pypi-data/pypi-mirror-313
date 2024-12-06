# CY3761 | fb764bc@outlook.com | 2024-11-25 11:17:32 | open.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
def storage(src: str | Path, data=None, **kwargs):
    src = Path(src)
    is_read = data is None

    # print(src.exists())

    if is_read and not src.exists():
        return

    if isinstance(data, list):
        data = a_010.join([str(v) for v in data])

    if isinstance(data, dict):
        data = format_dumps(data)

    with src.open(
            switch(is_read, a_119, a_114) + a_116,
            encoding=kwargs.get(encoding_k, encoding)
    ) as io:
        return switch(
            is_read,
            lambda: io.write(data),
            lambda: io.read(),
        )()


# ----------------------------------------------------------------------------------------------------
def main_00():
    print(storage('./text.txt', [1234567, '肥婆跳舞拿第一']))
    print(storage('./text.txt', dict(a=1, b=2)))
    print(storage('./text.txt'))


# ----------------------------------------------------------------------------------------------------
def main():
    pass
    main_00()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
