import sys

if sys.version_info >= (3, 8):
    # Python 3.8 及以上版本，使用系统的 Literal
    from typing import Literal as SystemLiteral

    Literal = SystemLiteral
else:
    # Python 3.8 以下版本，使用自定义的 Literal
    class _Literal:
        def __getitem__(self, item):
            return None


    Literal = _Literal()

Encoding = Literal["gbk", "utf8"]
