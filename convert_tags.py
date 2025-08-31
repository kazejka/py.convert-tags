from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
from mutagen.asf import ASF
from mutagen.wave import WAVE
from mutagen.apev2 import APEv2
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.wavpack import WavPack
import os
import argparse
import sys
import logging
from datetime import datetime

def setup_logging(log_file=None, verbose=False):
    """Настройка системы логирования"""
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Консольный вывод
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO if verbose else logging.WARNING)
    logger.addHandler(console_handler)
    
    # Файловый вывод (если указан)
    if log_file:
        # Создаем папку для логов если её нет
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    
    return logger

def process_mp3(filepath, id3_version=3):
    """Обработка MP3 файлов с выбором версии ID3"""
    try:
        audio = ID3(filepath)
    except ID3NoHeaderError:
        audio = ID3()
    
    audio.save(filepath, v2_version=id3_version)

def process_flac(filepath):
    """Обработка FLAC файлов"""
    audio = FLAC(filepath)
    audio.save()

def process_mp4(filepath):
    """Обработка MP4/M4A файлов (AAC, ALAC)"""
    audio = MP4(filepath)
    audio.save()

def process_ogg(filepath):
    """Обработка OGG Vorbis файлов"""
    audio = OggVorbis(filepath)
    audio.save()

def process_opus(filepath):
    """Обработка Opus файлов"""
    audio = OggOpus(filepath)
    audio.save()

def process_wma(filepath):
    """Обработка WMA файлов"""
    audio = ASF(filepath)
    audio.save()

def process_wav(filepath):
    """Обработка WAV файлов"""
    audio = WAVE(filepath)
    # WAV обычно не имеет тегов, но если есть - сохраняем
    if audio.tags:
        audio.save()

def process_ape(filepath):
    """Обработка APE файлов"""
    audio = APEv2(filepath)
    audio.save()

def process_wv(filepath):
    """Обработка WavPack файлов"""
    audio = WavPack(filepath)
    audio.save()

def process_audio_files(root_folder, id3_version=3):
    """
    Рекурсивно обрабатывает все аудиофайлы
    id3_version: 3 - ID3v2.3 (по умолчанию), 4 - ID3v2.4
    """
    supported_formats = {
        # Lossy formats
        '.mp3': lambda path: process_mp3(path, id3_version),
        '.aac': process_mp4,  # Обычно в MP4 контейнере
        '.ogg': process_ogg,
        '.opus': process_opus,
        '.wma': process_wma,
        
        # Lossless formats
        '.flac': process_flac,
        '.alac': process_mp4,  # Обычно в MP4 контейнере
        '.ape': process_ape,
        '.wav': process_wav,
        '.wave': process_wav,  # Альтернативное расширение
        '.wv': process_wv,     # WavPack
        
        # Контейнеры
        '.m4a': process_mp4,
        '.mp4': process_mp4,
    }
    
    processed_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext in supported_formats:
                filepath = os.path.join(root, filename)
                try:
                    supported_formats[file_ext](filepath)
                    processed_count += 1
                    version_str = f" v2.{id3_version}" if file_ext in ['.mp3'] else ""
                    logging.info(f"Обработан{version_str}: {filename}")
                except Exception as e:
                    error_count += 1
                    logging.error(f"Ошибка с {filename}: {e}")
    
    return processed_count, error_count

def setup_argparse():
    """Настройка парсера аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Исправление кодировки тегов в аудиофайлах",
        epilog="Примеры использования:\n"
               "  python convert_tags.py D:\\music --id3_v24\n"
               "  python convert_tags.py /home/user/music --log music_convert.log\n"
               "  python convert_tags.py . --verbose --test",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'path',
        help='Путь к папке с аудиофайлами'
    )
    
    parser.add_argument(
        '--id3_v24', 
        action='store_true',
        help='Использовать ID3v2.4 вместо ID3v2.3 (по умолчанию)'
    )
    
    parser.add_argument(
        '--id3_v23', 
        action='store_true',
        help='Явно указать использование ID3v2.3 (используется по умолчанию)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Подробный вывод в консоль'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Тестовый режим (только покажет что будет обработано)'
    )
    
    parser.add_argument(
        '--log', '-l',
        metavar='FILE',
        help='Сохранять лог в указанный файл'
    )
    
    parser.add_argument(
        '--log-dir',
        metavar='DIR',
        default='logs',
        help='Папка для сохранения лог-файлов (по умолчанию: logs)'
    )
    
    return parser.parse_args()

def get_supported_formats():
    """Возвращает список поддерживаемых форматов"""
    return {
        'Lossy': ['.mp3', '.aac', '.ogg', '.opus', '.wma'],
        'Lossless': ['.flac', '.alac', '.ape', '.wav', '.wv'],
        'Containers': ['.m4a', '.mp4']
    }

def main():
    args = setup_argparse()
    
    folder_path = args.path
    
    # Настройка логирования
    log_file = args.log
    if not log_file and not args.test:
        # Автоматическое имя файла лога
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(args.log_dir, f'audio_tags_convert_{timestamp}.log')
    
    logger = setup_logging(log_file, args.verbose)
    
    # Определяем версию ID3
    if args.id3_v24:
        id3_version = 4
        version_name = "ID3v2.4"
    else:
        id3_version = 3
        version_name = "ID3v2.3"
    
    # Проверяем существование пути
    if not os.path.exists(folder_path):
        logging.error(f"Путь не существует: {folder_path}")
        sys.exit(1)
    
    if not os.path.isdir(folder_path):
        logging.error(f"Это не папка: {folder_path}")
        sys.exit(1)
    
    logging.info(f"Обработка папки: {folder_path}")
    logging.info(f"Версия тегов: {version_name}")
    
    if log_file:
        logging.info(f"Лог-файл: {log_file}")
    
    # Показываем поддерживаемые форматы
    formats = get_supported_formats()
    logging.info("Поддерживаемые форматы:")
    for category, exts in formats.items():
        logging.info(f"  {category}: {', '.join(exts)}")
    
    logging.info("=" * 60)
    
    if args.test:
        # Тестовый режим - только показываем файлы
        logging.info("ТЕСТОВЫЙ РЕЖИМ. Файлы не будут изменены.")
        logging.info("Будут обработаны следующие файлы:")
        logging.info("=" * 60)
        
        supported_extensions = set()
        for exts in formats.values():
            supported_extensions.update(exts)
        
        file_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in supported_extensions:
                    filepath = os.path.join(root, filename)
                    file_count += 1
                    total_size += os.path.getsize(filepath)
                    if args.verbose:
                        rel_path = os.path.relpath(filepath, folder_path)
                        logging.info(f"  {rel_path}")
        
        logging.info("=" * 60)
        logging.info(f"Найдено файлов для обработки: {file_count}")
        logging.info(f"Общий размер: {total_size / (1024*1024*1024):.2f} GB")
        return
    
    # Режим реальной обработки
    start_time = datetime.now()
    processed, errors = process_audio_files(folder_path, id3_version)
    end_time = datetime.now()
    duration = end_time - start_time
    
    logging.info("=" * 60)
    logging.info("ОБРАБОТКА ЗАВЕРШЕНА")
    logging.info(f"Успешно обработано: {processed} файлов")
    logging.info(f"Ошибок: {errors}")
    logging.info(f"Время выполнения: {duration}")
    
    if errors == 0:
        logging.info("Все файлы обработаны успешно!")
    else:
        logging.warning(f"Было {errors} ошибок при обработке")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        sys.exit(1)
