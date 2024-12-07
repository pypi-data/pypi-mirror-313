from datetime import datetime
from typing import Optional

import click
from rich import print, table

import coiled
from coiled.cli.curl import sync_request

from ..cluster.utils import find_cluster
from ..utils import CONTEXT_SETTINGS

TODAY = datetime.today().date()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option("--format", default="table", type=click.Choice(["json", "table"]))
@click.option("--limit", default=10, type=int)
def batch_status(
    cluster: str,
    workspace: Optional[str],
    format: str,
    limit: int,
):
    if cluster:
        show_cluster_job_status(cluster=cluster, workspace=workspace, format=format)
    else:
        show_job_list(workspace=workspace, format=format, limit=limit)


def format_dt(dt):
    if not dt:
        return ""
    dt = datetime.fromisoformat(dt)

    if dt.date() == TODAY:
        return dt.time().strftime("%H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def show_job_list(workspace, format, limit):
    with coiled.Cloud(workspace=workspace) as cloud:
        url = f"{cloud.server}/api/v2/jobs/?workspace={workspace or ''}&limit={limit or ''}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )
        if format == "json":
            print(response)
        elif format == "table":
            if not response or not response.get("items"):
                print("No batch jobs found")
                return

            jobs = response["items"]
            show_workspace = len({job["workspace_name"] for job in jobs}) > 1

            t = table.Table()
            t.add_column(
                "ID",
            )
            if show_workspace:
                t.add_column("Workspace")
            t.add_column("State", justify="center")
            t.add_column("Tasks Done", justify="right")
            t.add_column("Submitted", justify="right")
            # t.add_column("Started", justify="right")
            t.add_column("Finished", justify="right")
            t.add_column("Approx Cloud Cost", justify="right")
            t.add_column("Command")

            for job in jobs:
                if job["n_tasks_failed"]:
                    if job["n_tasks_succeeded"]:
                        tasks_done = f"{job['n_tasks_succeeded']} + [red]{job['n_tasks_failed']}[/red]"
                        tasks_done = f"{tasks_done:4}"
                    else:
                        tasks_done = f"[red]{job['n_tasks_failed']:4}[/red]"
                else:
                    tasks_done = f"{job['n_tasks_succeeded']:4}"

                tasks_done = f"{tasks_done} /{job['n_tasks']:4}"
                if job["n_tasks_succeeded"] == job["n_tasks"]:
                    tasks_done = f"[green]{tasks_done}[/green]"

                row_data = [str(job["cluster_id"] or "")]

                if show_workspace:
                    row_data.append(str(job["workspace_name"] or ""))

                row_data.extend([
                    str(job["state"] or ""),
                    tasks_done,
                    format_dt(job["created"]),
                    format_dt(job["completed"]),
                    f"${job['approximate_cloud_total_cost']:.2f}" if job["approximate_cloud_total_cost"] else "",
                    job["user_command"],
                ])

                t.add_row(*row_data)
            print(t)


def show_cluster_job_status(cluster: str, workspace: Optional[str], format: str):
    with coiled.Cloud(workspace=workspace) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]

        url = f"{cloud.server}/api/v2/jobs/cluster/{cluster_id}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )

        if format == "json":
            print(response)
        elif format == "table":
            if not response:
                print(f"No batch jobs for cluster {cluster_id}")
                return

            cluster_state = response[0]["cluster_state"]
            user_command = response[0]["user_command"]

            t = table.Table(
                title=(
                    f"Batch Jobs for Cluster {cluster_id} ([bold]{cluster_state}[/bold])\n"
                    f"[bold]Command:[/bold] [green]{user_command}[/green]"
                )
            )
            t.add_column("Array ID")
            t.add_column("Assigned To")
            t.add_column("State")
            t.add_column("Start Time")
            t.add_column("Stop Time")
            t.add_column("Duration")
            t.add_column("Exit Code")

            for job in response:
                for task in job["tasks"]:
                    if task["start"] and task["stop"]:
                        start = datetime.fromisoformat(task["start"])
                        stop = datetime.fromisoformat(task["stop"])
                        duration = f"{int((stop - start).total_seconds())}s"
                    else:
                        duration = ""

                    t.add_row(
                        str(task["array_task_id"]),
                        task["assigned_to"]["private_ip_address"] if task["assigned_to"] else "",
                        task["state"],
                        format_dt(task["start"]),
                        format_dt(task["stop"]),
                        duration,
                        str(task["exit_code"]),
                    )
            print(t)
