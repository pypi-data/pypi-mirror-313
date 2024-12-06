from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import jsbeautifier
import typer
from pymongo import MongoClient

import module_qc_database_tools
from module_qc_database_tools.chip_config_api import ChipConfigAPI
from module_qc_database_tools.cli.globals import CONTEXT_SETTINGS, OPTIONS
from module_qc_database_tools.cli.utils import get_itkdb_client
from module_qc_database_tools.core import DPPort, LocalModule, Module
from module_qc_database_tools.utils import (
    chip_uid_to_serial_number,
    get_layer_from_serial_number,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    serial_number: str = OPTIONS["serial_number"],
    chip_template_path: Path = typer.Option(
        (module_qc_database_tools.data / "YARR" / "chip_template.json").resolve(),
        "-ch",
        "--chipTemplate",
        help="Default chip template from which the chip configs are generated.",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output_dir: Optional[Path] = typer.Option(  # noqa: UP007
        None,
        "-o",
        "--outdir",
        help="Path to output directory. If not specified, will store configs in mongodb.",
        exists=False,
        writable=True,
    ),
    modes: List[str] = typer.Option(  # noqa: UP006
        ["warm", "cold", "LP"],
        "-m",
        "--mode",
        help="Modes to generate configs for.",
    ),
    dp_port: DPPort = typer.Option(
        DPPort.A,
        "-p",
        "--port",
        "--dp",
        help="Select DisplayPort on PCIe card that connectivity file will be written for.",
    ),
    version: str = typer.Option(
        "latest",  ## TODO: ["latest", "TESTONWAFER", "MODULE/INITIAL_WARM", ...], ## use stage/test names?
        "-v",
        "--version",
        help="Generate chip configs, default is 'latest'. Possible choices: 'TESTONWAFER', 'latest'",
    ),
    use_current_stage: bool = typer.Option(
        False,
        "--use-current-stage/--use-initial-warm",
        help="From localDB, get the current module stage, generate, and upload the config to the current stage (enabled) or INITIAL_WARM (default).",
    ),
    speed: int = typer.Option(
        1280,
        "-s",
        "--speed",
        help="Readout speed in MHz. Possible choices: [1280, 640, 320, 160] MHz.",
    ),
    layer: str = typer.Option(
        "Unknown",
        "-l",
        "--layer",
        help="Layer of module, used for applying correct QC criteria settings. Options: R0, R0.5, L0, L1, L2 (default is automatically determined from the module SN)",
    ),
    mongo_uri: str = OPTIONS["mongo_uri"],
    itkdb_access_code1: Optional[str] = OPTIONS["itkdb_access_code1"],  # noqa: UP007
    itkdb_access_code2: Optional[str] = OPTIONS["itkdb_access_code2"],  # noqa: UP007
    from_local: bool = typer.Option(
        False, "--local", help="Pull latest config from LocalDB"
    ),
    fast: bool = typer.Option(
        False, "-f", "--fast", help="Fast generation of YARR config, no formatting."
    ),
    no_eos_token: bool = typer.Option(False, "--noeos", help="Do not use eos token"),
    reverse: bool = typer.Option(
        False,
        "--reverse",
        help="Use reversed order of chip ID, e.g. for old L0 linear triplets.",
    ),
    ssl: bool = OPTIONS["ssl"],
):
    """
    Main executable for generating yarr config.
    """
    if not from_local:
        client = get_itkdb_client(
            access_code1=itkdb_access_code1, access_code2=itkdb_access_code2
        )
        module = Module(client, serial_number, no_eos_token)
    else:
        client = MongoClient(mongo_uri, ssl=ssl)
        module = LocalModule(client, serial_number)

    if layer == "Unknown":
        typer.echo("INFO: Getting layer-dependent config from module SN...")
        layer_config = get_layer_from_serial_number(serial_number)
    else:
        typer.echo(
            f"INFO: Overwriting default layer config ({get_layer_from_serial_number(serial_number)}) with manual input ({layer})!"
        )
        layer_config = layer

    chip_template = (
        json.loads(chip_template_path.read_text()) if not from_local else None
    )

    for suffix in modes:
        connectivity_path = Path(output_dir or "", module.name).joinpath(
            f"{module.name}_{layer_config}{'_'+suffix if suffix else ''}.json"
        )

        generated_configs = module.generate_config(
            chip_template,
            layer_config,
            dp_port.value,
            suffix=suffix,
            version=version,
            speed=speed,
            reverse=reverse,
        )

        if output_dir:
            save_configs_local(generated_configs, connectivity_path, fast)

        elif not from_local:
            mongo_client = MongoClient(mongo_uri, ssl=ssl)
            chip_config_client = ChipConfigAPI(mongo_client)
            current_stage = (
                module.get_current_stage()
                if use_current_stage
                else "MODULE/INITIAL_WARM"
            )
            save_configs_mongo(
                generated_configs, chip_config_client, suffix, current_stage
            )


def save_configs_local(configs, connectivity_path, fast):
    """
    Save the configs generated to disk.
    """
    connectivity_path.parent.mkdir(parents=True, exist_ok=True)

    connectivity_path.write_text(json.dumps(configs["module"], indent=4))
    typer.echo(f"module connectivity file saved to {connectivity_path}")

    for chip_config, chip_spec in zip(configs["module"]["chips"], configs["chips"]):
        output_path = connectivity_path.parent.joinpath(chip_config["config"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if fast:
            output_path.write_text(
                json.dumps(chip_spec)
            )  ## file size is 1.8M, no linebreak
        else:
            ## needed to avoid having chip config file at 14MB (but slow)
            beautified = jsbeautifier.beautify(
                json.dumps(chip_spec), jsbeautifier.default_options()
            )
            output_path.write_text(beautified)  ## file size 1.9MB
        # output_path.write_text(json.dumps(chip_spec, indent=4)) ## file size 14MB due to linebreaks

        typer.echo(f"chip config file saved to {output_path}")


def save_configs_mongo(configs, chip_config_client, mode, stage):
    """
    Save the configs generated to mongo.
    """
    chip_type = configs["module"]["chipType"]
    for chip_spec in configs["chips"]:
        chip_serial_number = chip_uid_to_serial_number(
            chip_spec[chip_type]["Parameter"]["Name"]
        )
        base_commit_id = chip_config_client.create_config(
            chip_serial_number, stage, branch=mode
        )
        new_commit_id = chip_config_client.commit(
            base_commit_id,
            chip_spec,
            "initial generation from module-qc-database-tools",
        )
        typer.echo(
            f"chip config file saved to mongodb from {base_commit_id} ➜ {new_commit_id}"
        )


if __name__ == "__main__":
    typer.run(main)
