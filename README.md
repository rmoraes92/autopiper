# AutoPiper

AutoPiper is a thin command-line interface (CLI) wrapper around the
[piper](https://github.com/rhasspy/piper?tab=readme-ov-file) project.

The goal here is to help you:
- downloading piper
- downloading void models for piper

## Features

- **Initialize Projects**: Quickly set up a project with default settings.
- **List Models**: Display a list of available ONNX-mapped voice models.
- **Download Assets**: Download specific assets from GitHub releases, including voice models and configurations.

## Installation

To install AutoPiper, clone the repository and install the dependencies using [Poetry](https://python-poetry.org/):

```bash
# Clone the repository
git clone https://github.com/your-username/autopiper.git
cd autopiper

# Install dependencies
poetry install
```

## Usage

AutoPiper provides a CLI with the following commands:

### Initialize a Project

```bash
autopiper init \
    --tag-name <tag_name> \
    --lang-code <language_code> \
    --voice-model-name <model_name> \
    --quality <quality>
```

- `--tag-name`: Tag name of the release to download (default: latest).
- `--lang-code`: Language code to use (default: `en_US`).
- `--voice-model-name`: Voice model name to use (default: `amy`).
- `--quality`: Quality of the voice model (default: `low`).

### List Available Models

```bash
autopiper list-models
```

This command lists all available ONNX-mapped voice models.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## Acknowledgments

AutoPiper leverages the [Piper](https://github.com/rhasspy/piper) project for voice synthesis capabilities.