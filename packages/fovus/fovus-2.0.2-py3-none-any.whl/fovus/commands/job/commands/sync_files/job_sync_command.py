import click
from typing_extensions import Tuple, Union

from fovus.adapter.fovus_api_adapter import FovusApiAdapter
from fovus.util.file_util import FileUtil


@click.command("sync")
@click.option("--job-id", type=str, help="The ID of the job to sync files from.")
@click.option(
    "--job-directory",
    type=str,
    help="The directory of the job to sync files from. The job directory must be initialized by the Fovus CLI.",
)
@click.option(
    "--include-paths",
    "include_paths_tuple",
    metavar="include_paths",
    type=str,
    multiple=True,
    help=r"""
        The relative paths to files or folders inside the JOB_DIRECTORY that will be synced. Paths are provided with support for Unix shell-style wildcards.

        You can only provide either --include-paths or --exclude-paths,  not both.

        Supported wildcards:
        \* - matches any number of characters
        ? - matches any single character

        E.g. taskName/out?/\*.txt matches any .txt file in folders taskName/out1, taskName/out2, etc.

        E.g. taskName???/folder/file.txt matches taskName001/folder/file.txt, taskName123/folder/file.txt, etc.

        Multiple paths may be provided.
        """,
)
@click.option(
    "--exclude-paths",
    "exclude_paths_tuple",
    metavar="exclude_paths",
    type=str,
    multiple=True,
    help=r"""
        The relative paths to files or folders inside the JOB_DIRECTORY that will not be synced. Paths are provided with support for Unix shell-style wildcards.

        You can only provide either --include-paths or --exclude-paths,  not both.

        Supported wildcards:
        \* - matches any number of characters
        ? - matches any single character

        E.g. taskName/out?/\*.txt matches any .txt file in folders taskName/out1, taskName/out2, etc.

        E.g. taskName???/folder/file.txt matches taskName001/folder/file.txt, taskName123/folder/file.txt, etc.

        Multiple paths may be provided.
        """,
)
def job_sync_command(
    job_id: Union[str, None],
    job_directory: Union[str, None],
    include_paths_tuple: Tuple[str, ...],
    exclude_paths_tuple: Tuple[str, ...],
):
    """
    Sync job files from a running job to Fovus Storage.

    Only running jobs can be synced.
    """
    job_id = FileUtil.get_job_id(job_id, job_directory)

    include_paths = list(include_paths_tuple) if len(include_paths_tuple) > 0 else None
    exclude_paths = list(exclude_paths_tuple) if len(exclude_paths_tuple) > 0 else None

    print("Authenticating...")
    fovus_api_adapter = FovusApiAdapter()
    fovus_api_adapter.sync_job_files(job_id, include_paths, exclude_paths)
