import os
import random
import string
import tempfile
import zipfile
from pathlib import Path

from nzshm_common.util import compress_path, compress_string, decompress_string


def test_string_compression_round_trip():
    random_input = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1028))
    round_tripped = decompress_string(compress_string(random_input))
    assert random_input == round_tripped


def test_string_compression_round_trip_unicode():
    unicode = "āĀēĒīĪōŌūŪ Le cœur déçu mais l'âme plutôt naïve. ‘Single’ and “double” quotes, “curly” apostrophes."
    round_tripped = decompress_string(compress_string(unicode))
    assert unicode == round_tripped


def test_compress_path_round_trip():
    random_content_A = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1024))

    # create a temporary directory using the context manager
    tmpdirname = tempfile.mkdtemp()
    assert Path(tmpdirname).exists()

    fileA = None
    try:
        with tempfile.NamedTemporaryFile(prefix='Random_data_', dir=tmpdirname, mode='w', delete=False) as fileA:
            # ref https://stackoverflow.com/a/49868505
            fileA.write(random_content_A)
            fileA.flush()

            print(fileA.name)
            assert Path(fileA.name).exists()

            archive_file_name = compress_path(fileA.name, Path(tmpdirname, 'test_archive_A.zip'))

            print(f'archive_file_name: {archive_file_name}')
            assert Path(archive_file_name).exists()

            with zipfile.ZipFile(archive_file_name, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    print(info)

                tmp2name = tmpdirname
                with zipfile.ZipFile(archive_file_name, 'r') as zip_ref:
                    # assert fileA.name in zip_ref.namelist()
                    zip_ref.extractall(tmp2name)

                extracted_fileA = Path(tmp2name, fileA.name)

                print(extracted_fileA)
                print(list(Path(tmp2name).glob('*')))
                assert extracted_fileA.exists()

                with open(extracted_fileA, 'r') as newFileA:
                    assert newFileA.read() == random_content_A
    finally:
        if fileA is not None:
            os.remove(fileA.name)
