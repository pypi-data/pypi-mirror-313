import asyncio
import logging
import platform
import typing
from logging import getLogger
from typing import Dict, List, Optional, Set, Tuple, cast

from rich.progress import Progress
from typing_extensions import Literal

from coiled.context import track_context
from coiled.scan import scan_prefix
from coiled.software_utils import (
    check_pip_happy,
    create_wheels_for_local_python,
    create_wheels_for_packages,
    partition_ignored_packages,
    partition_local_packages,
    partition_local_python_code_packages,
)
from coiled.types import (
    ArchitectureTypesEnum,
    PackageInfo,
    PackageLevelEnum,
    ResolvedPackageInfo,
    parse_conda_channel,
)
from coiled.v2.core import CloudV2
from coiled.v2.widgets.util import simple_progress

PYTHON_VERSION = platform.python_version_tuple()
ANY_AVAILABLE = "ANY-AVAILABLE"


logger = getLogger("coiled.package_sync")


async def default_python() -> PackageInfo:
    python_version = platform.python_version()
    return {
        "name": "python",
        "path": None,
        "source": "conda",
        "channel_url": ANY_AVAILABLE,
        "channel": ANY_AVAILABLE,
        "subdir": "linux-64",
        "conda_name": "python",
        "version": python_version,
        "wheel_target": None,
    }


@track_context
async def approximate_packages(
    cloud: CloudV2,
    packages: List[PackageInfo],
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    progress: Optional[Progress] = None,
    strict: bool = False,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    pip_check_errors: Optional[Dict[str, List[str]]] = None,
    gpu_enabled: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    user_conda_installed_python = next((p for p in packages if p["name"] == "python"), None)
    user_conda_installed_pip = next(
        (i for i, p in enumerate(packages) if p["name"] == "pip" and p["source"] == "conda"),
        None,
    )
    if not user_conda_installed_pip:
        # This means pip was installed by pip, or the system
        # package manager
        # Insert a conda version of pip to be installed first, it will
        # then be used to install the users version of pip
        pip = next(
            (p for p in packages if p["name"] == "pip" and p["source"] == "pip"),
            None,
        )
        if not pip:
            # insert a modern version and hope it does not introduce conflicts
            packages.append({
                "name": "pip",
                "path": None,
                "source": "conda",
                "channel_url": "https://conda.anaconda.org/conda-forge/",
                "channel": "conda-forge",
                "subdir": "noarch",
                "conda_name": "pip",
                "version": "22.3.1",
                "wheel_target": None,
            })
        else:
            # insert the users pip version and hope it exists on conda-forge
            packages.append({
                "name": "pip",
                "path": None,
                "source": "conda",
                "channel_url": "https://conda.anaconda.org/conda-forge/",
                "channel": "conda-forge",
                "subdir": "noarch",
                "conda_name": "pip",
                "version": pip["version"],
                "wheel_target": None,
            })
    coiled_selected_python = None
    if not user_conda_installed_python:
        # insert a special python package
        # that the backend will pick a channel for
        coiled_selected_python = await default_python()
        packages.append(coiled_selected_python)
    packages, _ = partition_ignored_packages(packages, priorities=priorities)
    packages, local_python_code = partition_local_python_code_packages(packages)
    packages, local_python_wheel_packages = partition_local_packages(packages)
    with simple_progress("Validating environment", progress=progress):
        results = await cloud._approximate_packages(
            packages=[
                {
                    "name": pkg["name"],
                    "priority_override": (
                        PackageLevelEnum.CRITICAL
                        if (
                            pkg["version"]
                            and (
                                strict
                                or (
                                    pkg["wheel_target"]
                                    # Ignore should override wheel_target (see #2640)
                                    and not priorities.get((pkg["name"], pkg["source"])) == PackageLevelEnum.IGNORE
                                )
                            )
                        )
                        else priorities.get((
                            (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                            pkg["source"],
                        ))
                    ),
                    "python_major_version": PYTHON_VERSION[0],
                    "python_minor_version": PYTHON_VERSION[1],
                    "python_patch_version": PYTHON_VERSION[2],
                    "source": pkg["source"],
                    "channel_url": pkg["channel_url"],
                    "channel": pkg["channel"],
                    "subdir": pkg["subdir"],
                    "conda_name": pkg["conda_name"],
                    "version": pkg["version"],
                    "wheel_target": pkg["wheel_target"],
                }
                # Send all packages to backend to help with debugging
                for pkg in packages + local_python_code + local_python_wheel_packages
            ],
            architecture=architecture,
            pip_check_errors=pip_check_errors,
            gpu_enabled=gpu_enabled,
        )
    finalized_packages: typing.List[ResolvedPackageInfo] = []
    finalized_packages.extend(await create_wheels_for_local_python(local_python_code, progress=progress))
    finalized_packages.extend(await create_wheels_for_packages(local_python_wheel_packages, progress=progress))
    for package_result in results:
        # Ensure channel from package_result is a channel and not a URL for conda packages
        if package_result["conda_name"] and package_result["channel_url"]:
            subdir = f"linux-{architecture.conda_suffix}"
            channel = parse_conda_channel(package_result["name"], package_result["channel_url"], subdir)[0]
        else:
            channel = package_result["channel_url"]
        # Remove channel_url note that endpoint returns for backward compatibility
        if (
            channel
            and package_result["note"]
            and (channel == package_result["note"] or package_result["note"].endswith(f",{channel}"))
        ):
            package_result["note"] = None

        finalized_packages.append({
            "name": package_result["name"],
            "source": "conda" if package_result["conda_name"] else "pip",
            "channel": channel,
            "conda_name": package_result["conda_name"],
            "client_version": package_result["client_version"],
            "specifier": package_result["specifier"] or "",
            "include": package_result["include"],
            "note": package_result["note"],
            "error": package_result["error"],
            "sdist": None,
            "md5": None,
        })

    return finalized_packages


@track_context
async def create_environment_approximation(
    cloud: CloudV2,
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    only: Optional[Set[str]] = None,
    conda_extras: Optional[List[str]] = None,
    strict: bool = False,
    progress: Optional[Progress] = None,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    gpu_enabled: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    packages = await scan_prefix(progress=progress)
    pip_check_errors = await check_pip_happy(progress)
    if only:
        packages = [pkg for pkg in packages if pkg["name"] in only]
    extra_packages: List[PackageInfo] = [
        {
            "name": conda_extra,
            "path": None,
            "source": "conda",
            "channel_url": ANY_AVAILABLE,
            "channel": ANY_AVAILABLE,
            "subdir": f"linux-{architecture.conda_suffix}",
            "conda_name": conda_extra,
            "version": "",
            "wheel_target": None,
        }
        for conda_extra in (conda_extras or [])
    ]
    result = await approximate_packages(
        cloud=cloud,
        packages=[pkg for pkg in packages] + extra_packages,
        priorities=priorities,
        strict=strict,
        progress=progress,
        architecture=architecture,
        pip_check_errors=pip_check_errors,
        gpu_enabled=gpu_enabled,
    )
    return result


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)

    from rich.console import Console
    from rich.table import Table

    async def run():
        async with CloudV2(asynchronous=True) as cloud:
            return await create_environment_approximation(
                cloud=cloud,
                priorities={
                    ("dask", "conda"): PackageLevelEnum.CRITICAL,
                    ("twisted", "conda"): PackageLevelEnum.IGNORE,
                    ("graphviz", "conda"): PackageLevelEnum.LOOSE,
                    ("icu", "conda"): PackageLevelEnum.LOOSE,
                },
            )

    result = asyncio.run(run())

    table = Table(title="Packages")
    keys = ("name", "source", "include", "client_version", "specifier", "error", "note")

    for key in keys:
        table.add_column(key)

    for pkg in result:
        row_values = [str(pkg.get(key, "")) for key in keys]
        table.add_row(*row_values)
    console = Console()
    console.print(table)
    console.print(table)
