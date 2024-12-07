
import argparse
import logging
import os
import platform
import shlex
import subprocess
import sys
import time
import tomllib
from contextlib import suppress
from filelock import FileLock, Timeout as LockTimeout
from pathlib import Path
from typing import Dict

########

LOCK_FILE_SUFFIX = '.lock'

CTRL_ARGS = 'ctrl-args'
SYNC_ARGS = 'sync-args'
SYNC_ARGS_VPN = 'sync-args-vpn'
CONFIGS = 'configs'
SERVERS = 'servers'
FOLDERS = 'folders'

########

class LevelFormatter(logging.Formatter):
    logging.Formatter.default_msec_format = logging.Formatter.default_msec_format.replace(',', '.') if logging.Formatter.default_msec_format else None

    def __init__(self, fmts: Dict[int, str], fmt: str, **kwargs):
        super().__init__()
        self.formatters = dict({level: logging.Formatter(fmt, **kwargs) for level, fmt in fmts.items()})
        self.default_formatter = logging.Formatter(fmt, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        return self.formatters.get(record.levelno, self.default_formatter).format(record)

class Logger(logging.Logger):
    def __init__(self, name, level = logging.NOTSET):
        super().__init__(name, level)
        self.exitcode = 0

    def prepare(self, timestamp: bool, silent: bool):
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            LevelFormatter(
                {
                    logging.WARNING: '%(asctime)s %(message)s',
                    logging.INFO: '%(asctime)s %(message)s',
                    logging.DEBUG: '%(asctime)s %(levelname)s %(message)s',
                },
                '%(asctime)s %(name)s: %(levelname)s: %(message)s')
            if timestamp else
            LevelFormatter(
                {
                    logging.WARNING: '%(message)s',
                    logging.INFO: '%(message)s',
                    logging.DEBUG: '%(levelname)s %(message)s',
                },
                '%(name)s: %(levelname)s: %(message)s')
        )
        self.addHandler(handler)
        if self.level == logging.NOTSET:
            self.setLevel(logging.WARNING if silent else logging.INFO)

    def exception_or_error(self, e: Exception, args):
        if not args or args.debug:
            logger.exception(e)
        else:
            if hasattr(e, '__notes__'):
                logger.error("%s: %s", LazyStr(repr, e), LazyStr(", ".join, e.__notes__))
            else:
                logger.error(LazyStr(repr, e))

    def error(self, msg, *args, **kwargs):
        self.exitcode = 1
        super().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.exitcode = 1
        super().critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if level >= logging.ERROR:
            self.exitcode = 1
        super().log(level, msg, *args, **kwargs)

class LazyStr:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
    def __str__(self):
        if self.result is None:
            self.result = str(self.func(*self.args, **self.kwargs))
        return self.result

logger = Logger(Path(sys.argv[0]).name)

########

# based on https://stackoverflow.com/a/55656177/2755656
def sync_ping(host, packets: int = 1, timeout: float = 1):
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(int(timeout*1000)), host]
        # don't use text=True, the async version will raise ValueError("text must be False"), who knows why
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-W', str(int(timeout)), host]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0

def test_networking(timeout: float = 60):
    cnt = int(timeout / 5)
    while True:
        last_test_at = time.time()
        if sync_ping('1.1.1.1', 1, 5):
            return True
        if 0 < (time_to_sleep := last_test_at + 5 - time.time()):
            time.sleep(time_to_sleep)
        if not (cnt := cnt -1):
            return False

def shlex_split(args):
    return shlex.split(args, platform.system().lower() != 'windows')

def append_if_not_in(args, option, option_args = None):
    if option not in args:
        args.append(option)
        if option_args:
            args.extend(option_args)

def append_logging_options(args, parsed_args):
    if parsed_args.timestamp:
        append_if_not_in(args, '-t')
    if parsed_args.silent:
        append_if_not_in(args, '-s')
    if parsed_args.debug:
        append_if_not_in(args, '--debug')

def append_sync_options(args, parsed_args):
    if parsed_args.dry:
        append_if_not_in(args, '-d')

def execute(command, args, parsed_args):
    cmd = args.copy()
    cmd.insert(0, command)
    logger.debug("executing: %s", LazyStr(shlex.join, cmd))
    if parsed_args.test:
        return (0, '<<<TEST RUN>>>')
    # text=True doesn't work with the async version, will raise ValueError("text must be False"), who knows why
    # creationflags=subprocess.CREATE_NO_WINDOW causes to NOT write stderr at all
    result = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=sys.stderr, text=True)
    return (result.returncode, result.stdout)

########

class HasPredefinedConfigs():
    def __init__(self, configs):
        self.configs = configs

    def get_sync_args_from_configs(self, name):
        config = self.configs.get(name)
        if config:
            return shlex_split(config[SYNC_ARGS])
        else:
            return []

class General(HasPredefinedConfigs):
    def __init__(self, args, config):
        super().__init__(config[CONFIGS])
        self.ctrl_args = shlex_split(config[CTRL_ARGS])
        self.sync_args = shlex_split(config[SYNC_ARGS])
        self.server_configs = config[SERVERS]

class Server(HasPredefinedConfigs):
    def __init__(self, args, general: General, server_name: str):
        server = general.server_configs[server_name]
        super().__init__(server[CONFIGS])
        self.args = args
        self.general = general
        self.ctrl_args = shlex_split(server[CTRL_ARGS])
        self.sync_args = shlex_split(server[SYNC_ARGS])
        self.sync_args_vpn = shlex_split(server[SYNC_ARGS_VPN])
        self.folder_configs = server[FOLDERS]
        self._ctrl_cmd_args = None

    @property
    def ctrl_cmd_args(self):
        if self._ctrl_cmd_args is None:
            self._ctrl_cmd_args = list()
            self._ctrl_cmd_args.extend(self.ctrl_args)
            self._ctrl_cmd_args.extend(self.general.ctrl_args)
            append_logging_options(self._ctrl_cmd_args, self.args)
            if self.args.scheduled:
                append_if_not_in(self._ctrl_cmd_args, '-s')
        return self._ctrl_cmd_args

    def get_sync_args_from_configs(self, name):
        sync_args = list()
        sync_args.extend(self.general.get_sync_args_from_configs(name))
        sync_args.extend(super().get_sync_args_from_configs(name))
        return sync_args

    def test(self):
        test_ctrl_args = self.ctrl_cmd_args.copy()
        if self.args.ctrl_args:
            test_ctrl_args.extend(arg for arg in shlex_split(self.args.ctrl_args) if arg not in ['-ac', '--accept-cellular'])
        exitcode, _stdout = execute('prim-ctrl', test_ctrl_args, self.args)
        return exitcode == 0

    def start(self, no_state: bool = False):
        start_ctrl_args = self.ctrl_cmd_args.copy()
        if self.args.ctrl_args:
            start_ctrl_args.extend(shlex_split(self.args.ctrl_args))
        start_ctrl_args.extend(['-i', 'start'])
        if not no_state:
            start_ctrl_args.extend(['-b'])
        exitcode, self.previous_state = execute('prim-ctrl', start_ctrl_args, self.args)
        if exitcode == 0:
            if not no_state:
                logger.debug("  previous state: %s", self.previous_state)
            else:
                logger.info(self.previous_state.rstrip())
        return exitcode == 0

    @property
    def connected_over_vpn(self):
        return 'connected=remote' in self.previous_state

    def stop(self, no_state: bool = False):
        stop_ctrl_args = self.ctrl_cmd_args.copy()
        if self.args.ctrl_args:
            stop_ctrl_args.extend(arg for arg in shlex_split(self.args.ctrl_args) if arg not in ['-ac', '--accept-cellular'])
        stop_ctrl_args.extend(['-i', 'stop'])
        if not no_state:
            stop_ctrl_args.extend(['-r', self.previous_state])
        exitcode, _stdout = execute('prim-ctrl', stop_ctrl_args, self.args)
        return exitcode == 0

class Folder():
    def __init__(self, args, server: Server, folder_name: str):
        self.args = args
        self.server = server
        folder = server.folder_configs[folder_name]
        self.configs = folder[CONFIGS]
        self.sync_args = shlex_split(folder[SYNC_ARGS])
        self._sync_cmd_args = None

    @property
    def sync_cmd_args(self):
        if self._sync_cmd_args is None:
            self._sync_cmd_args = list()
            self._sync_cmd_args.extend(self.server.sync_args)
            if self.args.use_vpn or not self.args.sync_only and self.server.connected_over_vpn:
                self._sync_cmd_args.extend(self.server.sync_args_vpn)
            self._sync_cmd_args.extend(self.server.general.sync_args)
            for config_name in self.configs:
                self._sync_cmd_args.extend(self.server.get_sync_args_from_configs(config_name))
            self._sync_cmd_args.extend(self.sync_args)
            append_logging_options(self._sync_cmd_args, self.args)
            append_sync_options(self._sync_cmd_args, self.args)
            if self.args.scheduled:
                append_if_not_in(self._sync_cmd_args, '-ss')
            if self.args.sync_args:
                self._sync_cmd_args.extend(shlex_split(self.args.sync_args))
        return self._sync_cmd_args

    def sync(self):
        exitcode, _stdout = execute('prim-sync', self.sync_cmd_args, self.args)
        return exitcode == 0

########

class WideHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog: str, indent_increment: int = 2, max_help_position: int = 35, width: int | None = None) -> None:
        super().__init__(prog, indent_increment, max_help_position, width)

def main():
    args = None
    print_stopped = False
    pause = False
    try:
        parser = argparse.ArgumentParser(
            description="Multiplatform Python script for batch execution of prim-ctrl and prim-sync commands, for more details see https://github.com/lmagyar/prim-batch",
            formatter_class=WideHelpFormatter)

        parser.add_argument('config_file', metavar='config-file', help="TOML config file")
        parser.add_argument('--scheduled', help="tests networking, syncs without pause and with less log messages, but with some extra log lines that are practical when the output is appended to a log file", default=False, action='store_true')
        parser.add_argument('--no-pause', help="syncs without pause", default=False, action='store_true')
        parser.add_argument('--servers', nargs='+', metavar="SERVER", help="syncs only the specified SERVERs (all, or only the specified --folders FOLDERs on them)")
        parser.add_argument('--folders', nargs='+', metavar="FOLDER", help="syncs only the specified FOLDERs (on all, or only on the specified --servers SERVERs)")
        parser.add_argument('--ctrl-only', nargs='?', choices=["test", "start", "stop"], help="use only prim-ctrl, you can sync the server manually (this is the equivalent of prim-ctrl's -i option), default: test", default=None, const='test', action='store')
        parser.add_argument('--sync-only', help="use only prim-sync, you have to start/stop the server manually", default=False, action='store_true')
        parser.add_argument('--use-vpn', help="use vpn config (not zeroconf) to access the server (can be used only when --sync-only is used)", default=False, action='store_true')
        parser.add_argument('--test', help="do not execute any prim-ctrl or prim-sync commands, just log them (\"dry\" option for prim-batch), enables the --no-pause and --debug options", default=False, action='store_true')
        logging_group = parser.add_argument_group('logging',
            description="Note: prim-sync and prim-ctrl commands will receive these options also")
        logging_group.add_argument('-t', '--timestamp', help="prefix each message with a timestamp", default=False, action='store_true')
        logging_group.add_argument('-s', '--silent', help="only errors printed", default=False, action='store_true')
        logging_group.add_argument('--debug', help="use debug level logging and add stack trace for exceptions, disables the --silent and enables the --timestamp options", default=False, action='store_true')
        ctrl_group = parser.add_argument_group('prim-ctrl')
        ctrl_group.add_argument('--ctrl-args', metavar="ARGS", help="any prim-ctrl arguments to pass on - between quotation marks, using equal sign, like --ctrl-args='--accept-cellular'")
        sync_group = parser.add_argument_group('prim-sync')
        sync_group.add_argument('-d', '--dry', help="no files changed in the synchronized folder(s), only internal state gets updated and temporary files get cleaned up", default=False, action='store_true')
        sync_group.add_argument('--sync-args', metavar="ARGS", help="any prim-sync arguments to pass on - between quotation marks, using equal sign, like --sync-args='--ignore-locks'")

        args = parser.parse_args()

        if args.debug or args.test:
            logger.setLevel(logging.DEBUG)
        logger.prepare(args.timestamp or args.debug or args.test, args.silent)

        if args.use_vpn and not args.sync_only:
            raise ValueError("--use-vpn option can be used only when --sync-only is used")

        pause = not args.scheduled and not args.no_pause and not args.test

        argv0 = LazyStr(os.path.basename, sys.argv[0])
        argvx = LazyStr(shlex.join, sys.argv[1:])
        if args.scheduled:
            print_stopped = True
            logger.info("= STARTED = %s %s", argv0, argvx)

        # this testing is useful when as a scheduled task is executed after an awake and networking is not ready yet
        if args.scheduled and not test_networking(600):
            logger.error("Networking is down")
        else:
            try:
                # keep a lock on the config file while running to prevent parallel runs
                with (
                    FileLock(args.config_file + LOCK_FILE_SUFFIX, blocking=False),
                    open(args.config_file, "rb") as config_file
                ):
                    config = tomllib.load(config_file)
                    general = General(args, config)

                    def _sync_server(server_name):
                        server = Server(args, general, server_name)
                        if args.ctrl_only is not None:
                            if args.scheduled:
                                logger.info("----------- %s", server_name)
                            match args.ctrl_only:
                                case "start":
                                    if not args.scheduled:
                                        logger.info("Starting %s", server_name)
                                    server.start(no_state=True)
                                case "stop":
                                    if not args.scheduled:
                                        logger.info("Stopping %s", server_name)
                                    server.stop(no_state=True)
                                case _:
                                    if not args.scheduled:
                                        logger.info("Testing %s", server_name)
                                    server.test()
                            return True
                        elif args.folders is None or any(folder_name in server.folder_configs for folder_name in args.folders):
                            if args.scheduled:
                                logger.info("=========== %s", server_name)
                            else:
                                logger.info("Syncing %s", server_name)
                            if args.sync_only or server.start():
                                try:
                                    if args.folders is None:
                                        for folder_name in server.folder_configs:
                                            if not Folder(args, server, folder_name).sync():
                                                break
                                    else:
                                        for folder_name in args.folders:
                                            if folder_name in server.folder_configs:
                                                if not Folder(args, server, folder_name).sync():
                                                    break;
                                finally:
                                    if not args.sync_only:
                                        server.stop()
                            return True
                        return False

                    if args.servers is None:
                        # iterate all, then test, don't stop at first
                        if not any([_sync_server(server_name) for server_name in general.server_configs]):
                            logger.error("None of the specified folders (%s) are on any configured server", LazyStr(', '.join, args.folders))
                    elif any(server_name in general.server_configs for server_name in args.servers):
                        # iterate all, then test, don't stop at first
                        if not any([_sync_server(server_name) for server_name in args.servers if server_name in general.server_configs]):
                            logger.error("None of the specified folders (%s) are on any specified servers (%s)", LazyStr(', '.join, args.folders), LazyStr(', '.join, args.servers))
                    else:
                        logger.error("None of the specified servers (%s) are in the config", LazyStr(', '.join, args.servers))

            except LockTimeout as e:
                logger.error("Can't acquire lock on %s, probably already running", e.lock_file)

    except Exception as e:
        logger.exception_or_error(e, args)

    if print_stopped:
        logger.info("= STOPPED = %s %s", argv0, argvx)

    if pause:
        with suppress(EOFError):
            input("Press Enter to continue...")

    return logger.exitcode

def run():
    with suppress(KeyboardInterrupt):
        exit(main())
