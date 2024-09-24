import pytest
from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3
from pydub import AudioSegment

from src.core.converter import SingleFileConverter
from src.utils.enums import AudioFormat


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def test_flac_file(temp_dir):
    flac_path = temp_dir / "test.flac"

    # Создаем тестовый аудиофайл
    audio = AudioSegment.silent(duration=1000)  # 1 секунда тишины
    audio.export(flac_path, format="flac")

    # Добавляем метаданные
    flac = FLAC(flac_path)
    flac["title"] = "Test Title"
    flac["artist"] = "Test Artist"
    flac["album"] = "Test Album"

    # Добавляем тестовую обложку
    picture = Picture()
    picture.type = 3  # 3 означает обложку
    picture.mime = "image/jpeg"
    picture.desc = "Cover"
    with open("tests/resources/test_cover.jpg", "rb") as img:
        picture.data = img.read()
    flac.add_picture(picture)

    flac.save()
    return flac_path


def test_convert_with_cover(temp_dir, test_flac_file):
    converter = SingleFileConverter(AudioFormat.MP3, include_cover=True)
    output_path = temp_dir / "output.mp3"

    converted_file = converter.convert(test_flac_file, output_path)

    assert converted_file.exists()
    assert converted_file.suffix == ".mp3"

    # Проверяем метаданные
    mp3 = MP3(converted_file)
    assert mp3.tags["TIT2"].text[0] == "Test Title"
    assert mp3.tags["TPE1"].text[0] == "Test Artist"
    assert mp3.tags["TALB"].text[0] == "Test Album"

    # Проверяем наличие обложки
    assert SingleFileConverter.has_cover(converted_file)


def test_convert_without_cover(temp_dir, test_flac_file):
    converter = SingleFileConverter(AudioFormat.MP3, include_cover=False)
    output_path = temp_dir / "output_no_cover.mp3"

    converted_file = converter.convert(test_flac_file, output_path)

    assert converted_file.exists()
    assert converted_file.suffix == ".mp3"

    # Проверяем метаданные
    mp3 = MP3(converted_file)
    assert mp3.tags["TIT2"].text[0] == "Test Title"
    assert mp3.tags["TPE1"].text[0] == "Test Artist"
    assert mp3.tags["TALB"].text[0] == "Test Album"

    # Проверяем отсутствие обложки
    assert not SingleFileConverter.has_cover(converted_file)


def test_invalid_input_file(temp_dir):
    converter = SingleFileConverter(AudioFormat.MP3, include_cover=True)
    invalid_input = temp_dir / "non_existent.flac"
    output_path = temp_dir / "output.mp3"

    with pytest.raises(Exception):  # Ожидаем, что будет выброшено исключение
        converter.convert(invalid_input, output_path)
