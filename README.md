# Audio Tag Converter
A Python script that fixes and standardizes tag encoding in various audio file formats using the mutagen library.

## Supported Formats
    Lossy: MP3, AAC, OGG, Opus, WMA
    Lossless: FLAC, ALAC, APE, WAV, WavPack
    Containers: M4A, MP4

## Usage
```bash
python convert_tags.py /path/to/music/folder
```

## Command Line Arguments
| Argument | Description | Example |
| :--- | :--- | :--- |
| `--id3_v24` | Use ID3v2.4 instead of ID3v2.3 (default)|`--id3_v24` |
| `--id3_v23` | Explicitly use ID3v2.3 | `--id3_v23` |
| `--verbose`, `-v` | Verbose console output | `-v` |
| `--test`, `-t` | Test mode (show files without modifying) | `--test` |
| `--log`, `-l` | Save log to specified file | `--log convert.log` |
| `--log-dir` | Directory for log files |`--log-dir ./logs` |

### Examples
**Example 1:** Basic usage
```bash
python convert_tags.py "D:\Music"
```

**Example 2:** Test mode with verbose output:
```bash
python convert_tags.py "/home/user/music" --test --verbose
```

**Example 3:** Use ID3v2.4 with custom log:
```bash
python convert_tags.py ".\My Music" --id3_v24 --log "conversion.log"
```

## Requirements
    Python 3.6+
    mutagen>=1.47.0
