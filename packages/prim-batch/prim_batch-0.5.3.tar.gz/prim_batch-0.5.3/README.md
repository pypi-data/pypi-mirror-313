
# Primitive Batch

Multiplatform Python script for batch execution of prim-ctrl and prim-sync commands.

With the help of this script you can sync multiple phones (Primitive FTPd SFTP servers) and multiple folders on them in a preconfigured way.

It basically concatenates command lines for prim-ctrl and prim-sync based on the config. So depending on your system, Windows or Unix, use the appropriate single or double quotation marks and proper escaping in the config file.

See my other project, https://github.com/lmagyar/prim-sync, for bidirectional and unidirectional sync over SFTP (multiplatform Python script optimized for the Primitive FTPd SFTP server).

See my other project, https://github.com/lmagyar/prim-ctrl, for remote control of your phone's Primitive FTPd SFTP server and optionally Tailscale VPN.

**Note:** These are my first ever Python projects, any comments on how to make them better are appreciated.

## Features

- Optionally select only 1 server and/or folder to sync from the configuration, this is useful for a manually started sync
- Optionally select a scheduled run, that tests networking, syncs without pause and with less log messages, but with some extra log lines that are practical when the output is appended to a log file
- Optionally select a test run and only print out the commands that are configured to run

## Installation

You need to install:

- Python 3.12+, pip and venv on your laptop - see: https://www.python.org/downloads/ or
  <details><summary>Ubuntu</summary>

  ```
  sudo apt update
  sudo apt upgrade
  sudo apt install python3 python3-pip python3-venv
  ```
  </details>
  <details><summary>Windows</summary>

  - Install from Microsoft Store the latest [Python 3](https://apps.microsoft.com/search?query=python+3&department=Apps) (search), [Python 3.12](https://www.microsoft.com/store/productId/9NCVDN91XZQP) (App)
  - Install from Winget: `winget install Python.Python.3.12`
  - Install from Chocolatey: `choco install python3 -y`
  </details>

- pipx - see: https://pipx.pypa.io/stable/installation/#installing-pipx or
  <details><summary>Ubuntu</summary>

  ```
  sudo apt install pipx
  pipx ensurepath
  ```
  </details>
  <details><summary>Windows</summary>

  ```
  py -m pip install --user pipx
  py -m pipx ensurepath
  ```
  </details>

- This repo
  ```
  pipx install prim-batch
  ```

Optionally, if you want to edit or even contribute to the source, you also need to install:
- poetry - see: https://python-poetry.org/
  ```
  pipx install poetry
  ```

## Configuration

It uses TOML file for configuration. Instead of specification, here is an example config:

  <details><summary>Ubuntu</summary>

  ```
  ctrl-args = "--funnel your-laptop 12345 /prim-ctrl 8443"
  sync-args = "-rs '/fs/storage/emulated/0' --ignore-locks 60 -sh"

  [configs]
  in  = { sync-args = "-ui -m --overwrite-destination" }
  out = { sync-args = "-uo -m --overwrite-destination" }

  [servers.your-phone]
  ctrl-args = "Automate youraccount@gmail.com 'SOME MANUFACTURER XXX' automate your-phone-pftpd --tailscale tailxxxx.ts.net your-phone 2222"
  sync-args = "your-phone-pftpd id_ed25519_sftp"
  sync-args-vpn = "-a your-phone.tailxxxx.ts.net 2222"

  [servers.your-phone.configs]
  int = { sync-args = "'~/Mobile' '/fs/storage/emulated/0' '*'" }
  ext = { sync-args = "'~/Mobile' '/fs/storage/XXXX-XXXX'  '/saf'" }

  [servers.your-phone.folders]
  Camera        = { configs = [ "ext" ],        sync-args = "'Camera' 'DCIM/Camera'" }
  Music         = { configs = [ "ext", "out" ], sync-args = "'Music' '*'" }
  Screenshots   = { configs = [ "int" ],        sync-args = "'Screenshots' 'DCIM/Screenshots'" }
  ```

  </details>
  <details><summary>Windows</summary>

  ```
  ctrl-args = '--funnel your-laptop 12345 /prim-ctrl 8443'
  sync-args = '-rs "/fs/storage/emulated/0" --ignore-locks 60 -sh'

  [configs]
  in  = { sync-args = '-ui -m --overwrite-destination' }
  out = { sync-args = '-uo -m --overwrite-destination' }

  [servers.your-phone]
  ctrl-args = 'Automate youraccount@gmail.com "SOME MANUFACTURER XXX" automate your-phone-pftpd --tailscale tailxxxx.ts.net your-phone 2222'
  sync-args = 'your-phone-pftpd id_ed25519_sftp'
  sync-args-vpn = '-a your-phone.tailxxxx.ts.net 2222'

  [servers.your-phone.configs]
  int = { sync-args = '"D:\Mobile" "/fs/storage/emulated/0" "*"' }
  ext = { sync-args = '"D:\Mobile" "/fs/storage/XXXX-XXXX"  "/saf"' }

  [servers.your-phone.folders]
  Camera        = { configs = [ 'ext' ],        sync-args = '"Camera" "DCIM/Camera"' }
  Music         = { configs = [ 'ext', 'out' ], sync-args = '"Music" "*"' }
  Screenshots   = { configs = [ 'int' ],        sync-args = '"Screenshots" "DCIM/Screenshots"' }
  ```
  </details>

## Usage

### Some example

```
prim-batch config.toml -t
prim-batch config.toml -t --servers your-phone --folders Camera
prim-batch config.toml -t --scheduled
```

### Options

```
usage: prim-batch [-h] [--scheduled] [--no-pause] [--servers SERVER [SERVER ...]] [--folders FOLDER [FOLDER ...]] [--ctrl-only [{test,start,stop}]] [--sync-only] [--use-vpn] [--test] [-t] [-s] [--debug]
                  [--ctrl-args ARGS] [-d] [--sync-args ARGS]
                  config-file

Multiplatform Python script for batch execution of prim-ctrl and prim-sync commands, for more details see https://github.com/lmagyar/prim-batch

positional arguments:
  config-file                      TOML config file

options:
  -h, --help                       show this help message and exit
  --scheduled                      tests networking, syncs without pause and with less log messages, but with some extra log lines that are practical when the output is appended to a log file
  --no-pause                       syncs without pause
  --servers SERVER [SERVER ...]    syncs only the specified SERVERs (all, or only the specified --folders FOLDERs on them)
  --folders FOLDER [FOLDER ...]    syncs only the specified FOLDERs (on all, or only on the specified --servers SERVERs)
  --ctrl-only [{test,start,stop}]  use only prim-ctrl, you can sync the server manually (this is the equivalent of prim-ctrl's -i option), default: test
  --sync-only                      use only prim-sync, you have to start/stop the server manually
  --use-vpn                        use vpn config (not zeroconf) to access the server (can be used only when --sync-only is used)
  --test                           do not execute any prim-ctrl or prim-sync commands, just log them ("dry" option for prim-batch), enables the --no-pause and --debug options

logging:
  Note: prim-sync and prim-ctrl commands will receive these options also

  -t, --timestamp                  prefix each message with a timestamp
  -s, --silent                     only errors printed
  --debug                          use debug level logging and add stack trace for exceptions, disables the --silent and enables the --timestamp options

prim-ctrl:
  --ctrl-args ARGS                 any prim-ctrl arguments to pass on - between quotation marks, using equal sign, like --ctrl-args='--accept-cellular'

prim-sync:
  -d, --dry                        no files changed in the synchronized folder(s), only internal state gets updated and temporary files get cleaned up
  --sync-args ARGS                 any prim-sync arguments to pass on - between quotation marks, using equal sign, like --sync-args='--ignore-locks'
```
