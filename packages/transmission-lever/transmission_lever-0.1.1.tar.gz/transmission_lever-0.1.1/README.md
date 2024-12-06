# Transmission Lever

Small program that simplifies common chores on torrents by wrapping the RPC.
This program is not meant to be a manager by itself, only a *lever*
for others to write their own automatized tools.

## Installation

```bash
pip install transmission-lever
```

### Configuration file

Running `tlever` on the same machine as the torrent program will match the default credentials,
if that is not the case please copy the example file from the repository under one of the following paths:

```bash
1. ~/.config/transmission-lever/config.json
2. /etc/xdg/transmission-lever/config.json
3. ~/.transmission-lever/config.json
4. /etc/transmission-lever/config.json
```

They will be checked in that order.

## CLI Usage

### Categories

To organize torrents in folders the same way as clients like qBittorrent,
a label-based system marks the torrents and moves them to the location.

All paths are relative to the `Downloads` directory, this is read from
the transmission configuration file.

For example, to move `<torrent-hash>` into the *movies* category.
```bash
tlever category add movies <torrent-hash>
```

This will add the label `@movies` to the torrent and move its data to:
```
Downloads/
└── movies
    └── torrent-name
```

To undo the action:
```bash
tlever category remove movies <torrent-hash>
```

This will remove the label `@movies` to the torrent and move its data to:
```
Downloads/
└── torrent-name
```

> This command does not clean up empty directories,
> this is because the program is using the RPC to move torrent data
> and it does not have permissions over the filesystem in all use cases.
> 
> Hooking the command `find /path/to/Downloads -type d -empty -delete` to a script
> triggered by added|done|done_seeding of a torrent does the trick.

If labels get desync from the torrent directory, you can enforce the category label directory:
```bash
tlever enforce category
```

### Tags

To separate common labels from category labels,
a tag with a prefix is used.

For example, to tag `<torrent-hash>` with *best-of-the-year*:
```bash
tlever tag add best-of-the-year <torrent-hash>
```

This will add the label `#best-of-the-year` to the torrent.

To undo the action:
```bash
tlever tag remove best-of-the-year <torrent-hash>
```

This will remove the label `#best-of-the-year` to the torrent.

> This command *is not* equivalent to `tier label ...`
> as it is *always* prefixed.

### Tiers

To set upload speed throttling based on ratio,
this is based on [qbitseedmgr](https://github.com/Tomodoro/qbitseedmgr).

To start managing torrents:
```bash
tlever tier set
```

To stop managing torrents:
```bash
tlever tier unset
```

To resume paused torrents:
```bash
tlever tier activate
```

To keep the tiers updated and active:
```bash
tlever enforce tier
```

> The port of `not-popular` is a WIP.

### Clogs

When torrents surpass the last tier they are left unmanaged and if not configured correctly
they  can start hogging the bandwidth for themselves.

This commands fixes their upload limit to 50KiBps regardless their ratio or longevity.

> This is an experimental feature and many values are currently hardcoded.

To set the clog:
```bash
tlever clog set
```

To unset the clog:
```bash
tlever clog unset
```

### TUI

Basic terminal interface to show live a torrent stats.

> This is an experimental feature that needs further testing.

For example, given the torrent `<torrent-hash>`:
```bash
tlever tui show <torrent-hash>
```

### Labels

To manage labels without prefixes, useful to fix torrents that have
 invalid categories or tags because of a change in their prefix.

For example, given the prefixes `@` and `#` for categories and tags respectively,
it's desired to remove the invalid tag `%monthly-release`
from `<torrent-hash>`:
```bash
tlever label remove %monthly-release <torrent-hash>
```

To add an arbitrary label:
```bash
tlever label add custom-label <torrent-hash>
```

## Module Usage

### Overview

The functions are split into three namespaces:

1. `core`: direct calls to RPC
2. `extra`: extended functionality (i.e. categories)
3. `community`: extended functionality added from user's PR

The goal is to have a friendly wrapper with proper docstrings
that is modular and extendable.

If a PR use case is generic enough it will be added to `extra`.

### How to use?

The main file `tlever.py` that handles the CLI
it's only a series of if/else statements around functions.

To build a custom program you only need to call this functions
inside your program, making the respective module imports.