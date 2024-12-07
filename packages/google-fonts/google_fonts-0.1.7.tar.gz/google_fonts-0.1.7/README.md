## google-fonts

A pip tool to help to download google fonts into your computer.

## Installation

```shell
pip install google-fonts
```

## Usage

### Help

```shell
google-fonts --help # For help
```

### GitHub Token Configuration

The `.env` file will be stored in `~/.config/google_fonts/.env` (MacOS)

```shell
google-fonts config --token your_github_token # Setting github token
```

### List fonts

```shell
google-fonts list

# If you don't want set your token for long time
# Using the following configuration
google-fonts list --token your_github_token # Use github token specifically for once
```

### Install fonts

```shell
google-fonts install font1 font2 ...
# If you don't want set your token for long time
# Using the following configuration
google-fonts install font1 font2 ... --token your_github_token
```

## Advanced

There are some font name that can not find in `api.github.com`.

For example: `notosanssc`

You can use `--force` with specific font name to download.

The font name can be found in [`github/google/fonts`](https://github.com/google/fonts/tree/main/ofl)

```shell
google-fonts install notosanssc notosanstc --force
```

## Deploy

```shell
poetry config pypi-token.pypi
```