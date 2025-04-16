# AutoPiper

AutoPiper is a thin command-line interface (CLI) wrapper around the
[piper](https://github.com/rhasspy/piper?tab=readme-ov-file) project.

The goal here is to help you:

- downloading piper
- downloading void models for piper

## Features

- [x] **Initialize Projects**: Quickly set up a project with default settings.
- [x] **List Voice Models**: Display a list of available ONNX-mapped voice
      models.
- [ ] **Download Voice Models**: Download specific assets from GitHub releases,
      including voice models and configurations.

## Installation

`pip install --user autopiper`

To install AutoPiper from source clone the repository and install the
dependencies using [Poetry](https://python-poetry.org/):

```bash
# Clone the repository
git clone https://github.com/your-username/autopiper.git
cd autopiper

# Install dependencies
poetry install
```

## Supported Platform

- [x] Linux - x86_64
- [ ] Linux - aarch64
- [ ] Linux - armv7l
- [ ] Macos - aarch64
- [ ] Macos - x64
- [ ] Windows - amd64

## 1 - Usage

AutoPiper provides a CLI with the following commands:

### 1.1 - Initialize a Project with Piper v2023.11.14-2 and US Voice

```bash
autopiper init
```

#### 1.2 - Initialize a Project with Piper v2023.11.14-2 and Danish Voice

```bash
autopiper init \
    --tag-name 2023.11.14-2 \
    --lang-code da_DK \
    --voice-model-name talesyntese \
    --quality medium
```

- `--tag-name`: Tag name of the release to download (default: latest).
- `--lang-code`: Language code to use (default: `en_US`).
- `--voice-model-name`: Voice model name to use (default: `amy`).
- `--quality`: Quality of the voice model (default: `low`).

### 1.3 - List Available Models

```bash
autopiper list-models
```

### 1.4 - List Installed Models

```bash
autopiper list-models --installed
```

### 1.5 - Generate Audio File

```bash
echo "hello world" > hello.txt
autopiper text-to-speech hello.txt hello.wav --voide-model-id en_US-amy-low
```

This command lists all available ONNX-mapped voice models.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to
improve the project.

## Acknowledgments

AutoPiper leverages the [Piper](https://github.com/rhasspy/piper) project for
voice synthesis capabilities.
