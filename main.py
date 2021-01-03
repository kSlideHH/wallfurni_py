import sys

from g_python.gextension import Extension


from wallfurni import WallFurni

ext = None

extension_info = {
    "title": "WallFurniPy",
    "description": "Move wall furni",
    "version": "1.0",
    "author": "kSlide"
}


if __name__ == '__main__':
    extension = Extension(extension_info, sys.argv)
    extension.start()
    WallFurni(extension)
