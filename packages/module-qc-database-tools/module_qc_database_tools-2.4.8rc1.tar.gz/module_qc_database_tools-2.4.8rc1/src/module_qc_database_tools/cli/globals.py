from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from typing import Optional

import typer

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class LogLevel(str, Enum):
    """
    Enum for log levels.
    """

    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


class Protocol(str, Enum):
    """
    Enum for upload protocols.
    """

    HTTP = "http"
    HTTPS = "https"


OPTIONS = {}


def verbosity_callback(ctx: typer.Context, value: LogLevel):
    """
    Callback to set log level at the package-level.
    """
    if ctx.resilient_parsing:
        return None

    logging.getLogger("module_qc_database_tools").setLevel(value.value)
    return value


OPTIONS["verbosity"]: LogLevel = typer.Option(
    LogLevel.info,
    "-v",
    "--verbosity",
    help="Log level [options: DEBUG, INFO (default) WARNING, ERROR]",
    callback=verbosity_callback,
)
OPTIONS["measurement_path"]: Path = typer.Option(
    "Measurement/",
    "-p",
    "--path",
    help="Path to directory with output measurement files",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["protocol"]: Protocol = typer.Option(
    Protocol.HTTP, "--protocol", help="Protocol to connect to localDB (http or https)"
)
OPTIONS["verify_ssl"]: bool = typer.Option(
    True,
    "--verify/--skip-verify",
    help="if https protocol, verify or not the SSL certificate",
)
OPTIONS["host"]: str = typer.Option("localhost", "--host", help="localDB server")
OPTIONS["port"]: int = typer.Option(
    5000,
    "--port",
    help="localDB port",
)
OPTIONS["dry_run"]: bool = typer.Option(
    False,
    "-n",
    "--dry-run",
    help="Dry-run, do not submit to localDB or update controller config.",
)
OPTIONS["output_path"]: Path = typer.Option(
    "tmp.json",
    "--out",
    "--output-path",
    help="Analysis output result json file path to save in the local host",
    exists=False,
    writable=True,
)
OPTIONS["output_file"]: Optional[Path] = typer.Option(  # noqa: UP007
    None,
    "-o",
    "--output-file",
    help="Path to file. If not specified, will print to stdout.",
    exists=False,
    writable=True,
    dir_okay=False,
)


OPTIONS["serial_number"]: str = typer.Option(
    ..., "-sn", "--sn", help="ATLAS serial number"
)
OPTIONS["stage"]: str = typer.Option(
    ..., "-stage", "--stage", help="Stage to switch component and it's children to"
)
OPTIONS["mongo_uri"]: str = typer.Option(
    "mongodb://localhost:27017/localdb",
    "-u",
    "--uri",
    help="mongo URI (see documentation for mongo client)",
)
OPTIONS["localdb_name"]: str = typer.Option(
    "localdb",
    "-d",
    "--dbname",
    help="database name used for localDB. This is in your localDB config either as --db (command-line) or as mongoDB.db (yaml).",
)
OPTIONS["userdb_name"]: str = typer.Option(
    "localdbtools",
    "-u",
    "--userdbname",
    help="database name used for localDB tools. This is in your localDB config either as --userdb (command-line) or as userDB.db (yaml).",
)
OPTIONS["ssl"]: bool = typer.Option(
    False, "--ssl/--no-ssl", help="Use ssl for the connection to mongoDB"
)
OPTIONS["itkdb_access_code1"]: Optional[str] = typer.Option(  # noqa: UP007
    None, "--accessCode1", help="Access Code 1 for production DB"
)
OPTIONS["itkdb_access_code2"]: Optional[str] = typer.Option(  # noqa: UP007
    None, "--accessCode2", help="Access Code 2 for production DB"
)
OPTIONS["localdb"]: bool = typer.Option(
    False,
    "--localdb/--proddb",
    help="Whether to pull from localDB (default) or from Production DB.",
)
OPTIONS["mongo_serverSelectionTimeout"]: int = typer.Option(
    5,
    "--serverSelectionTimeout",
    help="server selection timeout in seconds",
)
