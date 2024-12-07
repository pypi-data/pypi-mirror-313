import datetime
import os
import re
import shlex

import click
from dask.utils import format_time
from rich import print

from coiled.cli.curl import sync_request
from coiled.cli.run import dict_from_key_val_list
from coiled.cli.utils import CONTEXT_SETTINGS, fix_path_for_upload
from coiled.credentials.aws import get_aws_local_session_token

# Be fairly flexible in how we parse options in header, i.e., we allow:
# "#COILED"
# "# COILED"
# then ":" and/or " "
# then you can specify key as "key" or "--key"
# key/val pair as "key val" or "key=val"
# or just "key" if it's a flag
HEADER_REGEX = re.compile(r"^\s*(# ?COILED)[\s:-]+([\w_-]+)([ =](.+))?")


def parse_array_string(array):
    try:
        return [int(array)]
    except ValueError:
        ...

    if "," in array:
        result = []
        for a in array.split(","):
            result.extend(parse_array_string(a))
        return result

    array_range = array.split("-")
    if len(array_range) == 2:
        start, end = array_range
        skip = 1
        try:
            if len(end.split(":")) == 2:
                end, skip = end.split(":")
                skip = int(skip)
            start = int(start)
            end = int(end)
        except ValueError:
            ...
        else:
            # no value error so far
            if start > end:
                # can't have this inside the try or else it would be caught
                raise ValueError(
                    f"Unable to parse '{array}' as a valid array range, start {start} is greater than end {end}."
                )
            return list(range(start, end + 1, skip))

    raise ValueError(f"Unable to parse '{array}' as a valid array range. Valid formats are `n`, `n-m`, or `n-m:s`.")


def handle_possible_implicit_file(implicit_file):
    if os.path.exists(implicit_file) and os.path.isfile(implicit_file):
        with open(implicit_file) as f:
            file_content = f.read()

        remote_rel_dir, remote_base = fix_path_for_upload(local_path=implicit_file)

        return {
            "local_path": implicit_file,
            "path": f"{remote_rel_dir}{remote_base}",
            "remote_path": f"/scratch/{remote_rel_dir}{remote_base}",
            "content": file_content,
        }


def search_content_for_implicit_files(f: dict):
    content = f["content"]
    implicit_files = []
    for line in content.split("\n"):
        if "python" in line or ".sh" in line:
            line_parts = shlex.split(line.strip())
            for part in line_parts:
                implicit_file = handle_possible_implicit_file(part)
                if implicit_file:
                    # TODO handle path translation?
                    implicit_files.append(implicit_file)
    return implicit_files


def get_kwargs_from_header(f: dict, click_params: list):
    click_lookup = {}
    for param in click_params:
        for opt in param.opts:
            lookup_key = opt.lstrip("-")
            click_lookup[lookup_key] = param
            if "-" in lookup_key:
                # support both (e.g.) `n-tasks` and `n_tasks`
                click_lookup[lookup_key.replace("-", "_")] = param

    kwargs = {}
    content = f["content"]
    for line in content.split("\n"):
        match = re.fullmatch(HEADER_REGEX, line)
        if match:
            kwarg = match.group(2).lower()
            val = match.group(4)
            val = val.strip().strip('"') if val else val

            if kwarg not in click_lookup:
                raise ValueError(f"Error parsing header in {f['path']}:\n{line}\n  {kwarg} is not valid argument")

            param = click_lookup[kwarg]
            val = True if param.is_flag else param.type.convert(val, param=param, ctx=None)
            key = param.name

            if param.multiple:
                if key not in kwargs:
                    kwargs[key] = []
                kwargs[key].append(val)
            else:
                kwargs[key] = val
    return kwargs


@click.command(context_settings={**CONTEXT_SETTINGS, "ignore_unknown_options": True})
@click.pass_context
# general cluster options
@click.option("--workspace", default=None, type=str, help="Coiled workspace (uses default workspace if not specified).")
@click.option(
    "--software",
    default=None,
    type=str,
    help=(
        "Existing Coiled software environment "
        "(Coiled will sync local Python software environment if neither software nor container is specified)."
    ),
)
@click.option(
    "--container",
    default=None,
    help=(
        "Docker container in which to run the batch job tasks; "
        "this does not need to have Dask (or even Python), "
        "only what your task needs in order to run."
    ),
)
@click.option(
    "--env",
    "-e",
    default=[],
    multiple=True,
    help=(
        "Environment variables transmitted to run command environment. "
        "Format is ``KEY=val``, multiple vars can be set with separate ``--env`` for each."
    ),
)
@click.option(
    "--secret-env",
    default=[],
    multiple=True,
    help=(
        "Environment variables transmitted to run command environment. "
        "Format is ``KEY=val``, multiple vars can be set with separate ``--secret-env`` for each. "
        "Unlike environment variables specified with ``--env``, these are only stored in our database temporarily."
    ),
)
@click.option(
    "--tag",
    "-t",
    default=[],
    multiple=True,
    help="Tags. Format is ``KEY=val``, multiple vars can be set with separate ``--tag`` for each.",
)
@click.option(
    "--vm-type",
    default=[],
    multiple=True,
    help="VM type to use. Specify multiple times to provide multiple options.",
)
@click.option("--arm", default=False, is_flag=True, help="Use ARM VM type.")
@click.option("--cpu", default=None, type=int, help="Number of cores per VM.")
@click.option("--memory", default=None, type=str, help="Memory per VM.")
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Have a GPU available.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the job.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
# batch specific options
@click.option(
    "--ntasks",
    "--n-tasks",
    default=None,
    type=int,
    help=(
        "Number of tasks to run. "
        "Tasks will have ID from 1 to n, the ``COILED_ARRAY_TASK_ID`` environment variable "
        "for each task is set to the ID of the task."
    ),
)
@click.option("--task-on-scheduler", default=False, is_flag=True, help="Run task with lowest job ID on scheduler node.")
@click.option(
    "--array",
    default=None,
    type=str,
    help=(
        "Specify array of tasks to run with specific IDs (instead of using ``--ntasks`` to get 1-n). "
        "You can specify list of IDs, a range, or a list with IDs and ranges. For example, ``--array 2,4-6,8-10``."
    ),
)
@click.option(
    "--scheduler-task-array",
    default=None,
    type=str,
    help=(
        "Which tasks in array to run on the scheduler node. "
        "In most cases you'll probably want to use ``--task-on-scheduler`` "
        "instead to run task with lowest ID on the scheduler node."
    ),
)
@click.option(
    "--max-workers",
    "-N",
    default=None,
    type=click.IntRange(1),
    help="Maximum number of worker nodes (by default, there will be as many worker nodes as tasks).",
)
@click.option(
    "--wait-for-ready-cluster", default=False, is_flag=True, help="Only assign tasks once full cluster is ready."
)
@click.option(
    "--forward-aws-credentials", default=False, is_flag=True, help="Forward STS token from local AWS credentials."
)
@click.argument("command", nargs=-1)
def batch_run(ctx, **kwargs):
    """
    Submit a batch job to run on Coiled.

    Batch Jobs is currently an experimental feature.
    """

    command = kwargs["command"]

    # Handle command as string case (e.g. `coiled run "python myscript.py"`)
    if len(command) == 1:
        command = shlex.split(command[0])
    # if user tries `coiled run foo.py` they probably want to run `python foo.py` rather than `foo.py`
    if len(command) == 1 and command[0].endswith(".py"):
        command = ["python", command[0]]

    # unescape escaped COILED env vars in command
    command = [part.replace("\\$COILED", "$COILED") for part in command]

    user_files = []
    kwargs_from_header = None

    # identify implicit files referenced in commands like "python foo.py" or "foo.sh"
    for idx, implicit_file in enumerate(command):
        f = handle_possible_implicit_file(implicit_file)
        if f:
            user_files.append(f)
            command[idx] = f["path"]
            # just get kwargs (if any) from the first file that has some in the header
            kwargs_from_header = kwargs_from_header or get_kwargs_from_header(f, ctx.command.params)

    # merge options from file header with options specified on command line
    # command line takes precedence
    if kwargs_from_header:
        for key, val in kwargs_from_header.items():
            # only use the option from header if command line opt was "default" (i.e., not specified by user)
            if ctx.get_parameter_source(key) == click.core.ParameterSource.DEFAULT:
                kwargs[key] = val
            elif isinstance(val, list) and isinstance(kwargs[key], (list, tuple)):
                kwargs[key] = [*kwargs[key], *val]

    # extra parsing/validation of options
    if kwargs["ntasks"] is not None and kwargs["array"] is not None:
        raise ValueError("You cannot specify both `--ntasks` and `--array`")

    # determine how many tasks to run on how many VMs
    if kwargs["ntasks"]:
        job_array_ids = list(range(1, kwargs["ntasks"] + 1))
    elif kwargs["array"]:
        job_array_ids = parse_array_string(kwargs["array"])
    else:
        job_array_ids = [0]

    scheduler_task_ids = parse_array_string(kwargs["scheduler_task_array"]) if kwargs["scheduler_task_array"] else []
    if kwargs["task_on_scheduler"]:
        scheduler_task_ids.append(min(*job_array_ids))

    max_workers = kwargs["max_workers"]
    n_task_workers = len(job_array_ids) if max_workers is None else min(len(job_array_ids), max_workers)

    # if there's just one task, only make a single VM and run it there
    if len(job_array_ids) == 1:
        scheduler_task_ids = job_array_ids
        n_task_workers = 0

    tags = dict_from_key_val_list(kwargs["tag"])

    job_env_vars = dict_from_key_val_list(kwargs["env"])
    job_secret_vars = dict_from_key_val_list(kwargs["secret_env"])

    if kwargs["forward_aws_credentials"]:
        # try to get creds that last 12 hours, but there's a good chance we'll get shorter-lived creds
        aws_creds = get_aws_local_session_token(60 * 60 * 12, log=False)
        if aws_creds["AccessKeyId"]:
            job_secret_vars["AWS_ACCESS_KEY_ID"] = aws_creds["AccessKeyId"]
            if aws_creds["Expiration"]:
                expires_in_s = (
                    aws_creds["Expiration"] - datetime.datetime.now(tz=datetime.timezone.utc)
                ).total_seconds()
                # TODO add doc explaining how to do this and refer to that doc
                print(
                    "[bold]Note[/bold]: "
                    f"Forwarding AWS credentials which will expire in [bold]{format_time(expires_in_s)}[/bold].\n"
                    "For longer tasks that need AWS authentication, "
                    "you should use the AWS Instance Profile to grant permission.\n"
                )
            else:
                print(
                    "[bold]Note[/bold]: "
                    "Forwarding AWS credentials, expiration is not known.\n"
                    "For longer tasks that need AWS authentication, "
                    "you should use the AWS Instance Profile to grant permission.\n"
                )
        if aws_creds["SecretAccessKey"]:
            job_secret_vars["AWS_SECRET_ACCESS_KEY"] = aws_creds["SecretAccessKey"]
        if aws_creds["SessionToken"]:
            job_secret_vars["AWS_SESSION_TOKEN"] = aws_creds["SessionToken"]

    # identify implicit files referenced by other files
    # for example, user runs "coiled batch run foo.sh" and `foo.sh` itself runs `python foo.py`
    user_files_from_content = []
    for f in user_files:
        if "python " in f["content"] or ".sh" in f["content"]:
            more_files = search_content_for_implicit_files(f)
            if more_files:
                user_files_from_content.extend(more_files)
    if user_files_from_content:
        user_files.extend(user_files_from_content)

    if n_task_workers:
        print(f"Running job array of {len(job_array_ids)} tasks on {n_task_workers} worker VMs...")
    else:
        print(f"Running job array of {len(job_array_ids)} tasks on 1 VM...")

    cluster_kwargs = {
        "workspace": kwargs["workspace"],
        "n_workers": n_task_workers,
        "software": kwargs["software"],
        # batch job can either run in normal Coiled software env (which defaults to package sync)
        # or can run in an extra container (which doesn't need to include dask)
        "batch_job_container": kwargs["container"],
        # if batch job is running in extra container, then we just need a pretty minimal dask container
        # so for now switch the default in that case to basic dask container
        # TODO would it be better to use a pre-built senv with our `cloud-env-run` container instead?
        "container": "daskdev/dask:latest" if kwargs["container"] and not kwargs["software"] else None,
        "region": kwargs["region"],
        "scheduler_options": {"idle_timeout": "520 weeks"},  # TODO allow job timeout?
        "worker_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
        "arm": kwargs["arm"],
        "worker_cpu": kwargs["cpu"],
        "worker_memory": kwargs["memory"],
        "worker_disk_size": kwargs["disk_size"],
        "tags": {**tags, **{"coiled-cluster-type": "batch"}},
        # "mount_bucket": mount_bucket,
    }

    # when task will run on scheduler, give it the same VM specs as worker node
    if scheduler_task_ids:
        cluster_kwargs = {
            **cluster_kwargs,
            "scheduler_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
            "scheduler_cpu": kwargs["cpu"],
            "scheduler_memory": kwargs["memory"],
            "scheduler_disk_size": kwargs["disk_size"],
            "scheduler_gpu": kwargs["gpu"],
        }

    import coiled

    with coiled.Cloud(workspace=kwargs["workspace"]) as cloud:
        # Create a job
        job_spec = {
            "user_command": shlex.join(command),
            "user_files": user_files,
            "workspace": cloud.default_workspace,
            "task_array": job_array_ids,
            "scheduler_task_array": scheduler_task_ids,
            "env_vars": job_env_vars,
            "secret_env_vars": job_secret_vars,
            "wait_for_ready_cluster": kwargs["wait_for_ready_cluster"],
        }

        url = f"{cloud.server}/api/v2/jobs/"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="post",
            data=job_spec,
            json=True,
            json_output=True,
        )

        job_id = response["id"]

        # Run the job on a cluster
        cluster = coiled.Cluster(
            cloud=cloud,
            batch_job_ids=[job_id],
            **cluster_kwargs,
        )

    status_command = f"coiled batch status {cluster.cluster_id}"
    if kwargs.get("workspace"):
        status_command = f"{status_command} --workspace {kwargs['workspace']}"

    print()
    print(f"Cluster ID:      {cluster.cluster_id}")
    print(f"Cluster Details: {cluster.details_url}")
    print()
    print("To check job status, you can run:")
    print(f"  {status_command}")
