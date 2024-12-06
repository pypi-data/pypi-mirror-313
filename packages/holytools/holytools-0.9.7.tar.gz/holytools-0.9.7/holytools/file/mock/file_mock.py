import os
import shutil
import tempfile
from holytools.file.types import PlaintextFile, ImageFile, BinaryFile

# ---------------------------------------------------------

def create_temp_copy(filename: str) -> str:
    module_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(module_dir, filename)

    temp_fd, temp_filepath = tempfile.mkstemp(suffix=os.path.splitext(filename)[1], dir='/tmp')
    os.close(temp_fd)
    shutil.copy2(original_file_path, temp_filepath)

    return temp_filepath


class FileMock:
    @staticmethod
    def lend_png() -> ImageFile:
        fpath = create_temp_copy('mock.png')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_jpg() -> ImageFile:
        fpath = create_temp_copy('mock.jpg')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_pdf() -> PlaintextFile:
        fpath = create_temp_copy('mock.pdf')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_txt() -> PlaintextFile:
        fpath = create_temp_copy('mock.txt')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_csv() -> PlaintextFile:
        fpath = create_temp_copy('mock.csv')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_bin() -> BinaryFile:
        fpath = create_temp_copy('mock.bin')
        return BinaryFile(fpath=fpath)

    @staticmethod
    def lend_wav() -> BinaryFile:
        fpath = create_temp_copy('mock.wav')
        return BinaryFile(fpath=fpath)

if __name__ == "__main__":
    print(os.path.abspath(__file__))