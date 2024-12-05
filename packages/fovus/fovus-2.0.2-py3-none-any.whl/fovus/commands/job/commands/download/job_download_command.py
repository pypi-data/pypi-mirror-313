import click
from typing_extensions import Tuple, Union

from fovus.adapter.fovus_api_adapter import FovusApiAdapter
from fovus.adapter.fovus_s3_adapter import FovusS3Adapter
from fovus.util.file_util import FileUtil


@click.command("download")
@click.argument("job_directory", type=str)
@click.option(
    "--job-id",
    type=str,
    help=(
        "The ID of the job to download files from. This is only required if JOB_DIRECTORY has not been initialized by"
        " the Fovus CLI."
    ),
)
@click.option(
    "--include-paths",
    "include_paths_tuple",
    metavar="include_paths",
    type=str,
    multiple=True,
    help=r"""
        The relative paths to files or folders inside the JOB_DIRECTORY that will be downloaded. Paths are provided with support for Unix shell-style wildcards.

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
        The relative paths to files or folders inside the JOB_DIRECTORY that will not be downloaded. Paths are provided with support for Unix shell-style wildcards.

        You can only provide either --include-paths or --exclude-paths,  not both.

        Supported wildcards:
        \* - matches any number of characters
        ? - matches any single character

        E.g. taskName/out?/\*.txt matches any .txt file in folders taskName/out1, taskName/out2, etc.

        E.g. taskName???/folder/file.txt matches taskName001/folder/file.txt, taskName123/folder/file.txt, etc.

        Multiple paths may be provided.
        """,
)
def job_download_command(
    job_id: Union[str, None],
    job_directory: str,
    include_paths_tuple: Tuple[str, ...],
    exclude_paths_tuple: Tuple[str, ...],
):
    """
    Download job files from Fovus Storage.

    Only new or updated files will be downloaded. If the job is running,
    the files will be synced to Fovus Storage before being downloaded.

    JOB_DIRECTORY is the directory where the files will be downloaded.
    """
    job_id = FileUtil.get_job_id(job_id, job_directory)

    include_paths = list(include_paths_tuple) if len(include_paths_tuple) > 0 else None
    exclude_paths = list(exclude_paths_tuple) if len(exclude_paths_tuple) > 0 else None

    print("Authenticating...")
    fovus_api_adapter = FovusApiAdapter()
    fovus_s3_adapter = FovusS3Adapter(
        fovus_api_adapter,
        root_directory_path=job_directory,
        job_id=job_id,
        include_paths=include_paths,
        exclude_paths=exclude_paths,
    )
    fovus_api_adapter.sync_job_files(job_id, include_paths, exclude_paths)
    fovus_s3_adapter.download_files()
