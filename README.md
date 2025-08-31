# py.convert-tags
Converting tags to v23 or v24

# Базовое использование с автоматическим логом
python convert_tags.py D:\music --id3_v24

# Указание конкретного лог-файла
python convert_tags.py D:\music --log conversion.log

# В другой папке для логов
python convert_tags.py D:\music --log-dir D:\logs

# Подробный вывод + лог
python convert_tags.py D:\music --verbose --log detailed.log

# Только тестовый режим
python convert_tags.py D:\music --test --verbose

# Короткие опции
python convert_tags.py D:\music -v -l music_fix.log
