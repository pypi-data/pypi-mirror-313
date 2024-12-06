from __future__ import annotations

import contextlib
import logging
from collections.abc import Iterator

import itkdb
from itkdb.models.component import Component as ITkDBComponent

from module_qc_database_tools.typing_compat import ProdDBComponent

log = logging.getLogger(__name__)


def get_component(client, identifier) -> (ProdDBComponent, str):
    """
    Get component information using identifier (serial number or id).

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for component information
        identifier (:obj:`str`): identifier of component to get information for (serial number or id)

    Returns:
        component (:obj:`dict`): information about the component from prodDB
        stage (:obj:`str`): current stage of component
    """
    try:
        component = client.get("getComponent", json={"component": identifier})
    except itkdb.exceptions.BadRequest as exc:
        msg = "An unknown error occurred. Please see the log."
        with contextlib.suppress(Exception):
            message = exc.response.json()
            if "ucl-itkpd-main/getComponent/componentDoesNotExist" in message.get(
                "uuAppErrorMap", {}
            ):
                msg = f"component with {identifier} not in ITk Production DB."

        raise ValueError(msg) from exc

    current_stage = get_stage(client, component)
    serial_number = component["serialNumber"]
    if not current_stage:
        msg = f"component with {serial_number} does not have a current stage. Something is wrong with this component in ITk Production Database."
        raise ValueError(msg)

    return (component, current_stage)


def get_serial_number(component: ProdDBComponent) -> str:
    """
    Get the serial number from the component.

    Args:
        component (:obj:`dict`): prodDB component to get serial number from

    Returns:
        serial_number (:obj:`str`): serial number of component
    """
    return component["serialNumber"]


def get_stage(client, component: ProdDBComponent) -> str | None:  # noqa: ARG001  # pylint: disable=unused-argument
    """
    Get the stage from the component.

    Args:
        component (:obj:`dict`): prodDB component to get stage from

    Returns:
        stage (:obj:`str`): stage of component
    """
    return (component.get("currentStage") or {}).get("code")


def get_children(
    client, component: ProdDBComponent, *, component_type=None, ignore_types=None
) -> Iterator[ProdDBComponent]:
    """
    Get children for component by ID matching the component type from Local DB.

    !!! note

        This returns a generator.

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for parent-child relationship
        component (:obj:`dict`): the top-level component to recursively get the children of
        component_type (:obj:`str` or :obj:`None`): the component type code to filter children by (None for any)
        ignore_types (:obj:`list` or :obj:`None`): component types to ignore

    Returns:
        children (:obj:`iterator`): generator of localDB components matching the component type
    """

    def _recursive(
        component: ITkDBComponent, *, component_type, ignored_types
    ) -> Iterator[ProdDBComponent]:
        current_component_type = (component._data.get("componentType") or {}).get(  # pylint: disable=protected-access
            "code"
        )
        if (
            current_component_type == component_type or component_type is None
        ) and current_component_type not in ignored_types:
            yield component._data  # pylint: disable=protected-access

        for child in component.children:
            yield from _recursive(
                child, component_type=component_type, ignored_types=ignored_types
            )

    # walk through structure
    component_model = ITkDBComponent(client, component)
    component_model.walk()

    yield from _recursive(
        component_model, component_type=component_type, ignored_types=ignore_types or []
    )


def set_component_stage(client, serial_number: str, stage: str, *, userdb=None) -> None:  # noqa: ARG001  # pylint: disable=unused-argument
    """
    Set component (by serial number) to the current stage.

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for parent-child relationship
        serial_number (:obj:`str`): serial number of component
        stage (:obj:`str`): code of stage to set component to

    Returns:
        None
    """
    component = client.get("getComponent", json={"component": serial_number})
    pdb_component_type = component["componentType"]["code"]

    if stage not in [
        ct_stage["code"] for ct_stage in component["componentType"]["stages"]
    ]:
        msg = (
            f"{stage} is not a valid stage on this component type: {pdb_component_type}"
        )
        raise ValueError(msg)

    try:
        client.post(
            "setComponentStage",
            json={
                "component": serial_number,
                "stage": stage,
            },
        )
    except itkdb.exceptions.BadRequest:
        msg = f"Unable to set {serial_number} to {stage}"
        log.exception(msg)
        return False
    return True
