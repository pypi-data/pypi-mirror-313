# douglog

A simple command line program that quickly creates and opens single log files with a date in a semi-organized way. Use tools like [`fzf`](https://github.com/junegunn/fzf) or [`ripgrep`](https://github.com/BurntSushi/ripgrep) to search through the generated logs.

## Dependencies

`git`: to use the `git` subcommand.

## Example Config

Default location is `~/.config/dlog.toml`.

```
editor = "nvim"
home = "~/dlogs"
logbooks = ["homelab", "work"]
```

- `editor` sets your editor.
- `home` is where you want to store your logs.
- `logbooks` is a list of your logs (to organize separate logging).

## Usage

```
$ dlog log <log-name>
$ dlog list
$ dlog search <regex>
$ dlog git <git commands>
```

## For Development

To install locally for testing:

```
source pyenv/bin/activate
pip install -e .
```
