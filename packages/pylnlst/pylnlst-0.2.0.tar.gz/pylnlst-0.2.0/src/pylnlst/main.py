"""pylnlst: tool to create linux symbolic links seamlessly."""

from collections.abc import Iterator
from pathlib import Path
from typing import Annotated

import typer
from rich import print  # noqa: A004

__version__ = "0.2.0"

FILE_LIST_DOC = """
Path to the file containing the list of files to process. Note that you can
prefix a line with '#' to comment out that line.
"""

DST_DIR_DOC = """
Path to the destination directory where the symbolic links will be created.
"""

BASE_SRC_DIR_DOC = """
Assumed base source directory for all the files in the filelist.
"""

MAX_CLASHING_FILE_INDEX = 1000


class LinkNameExhaustedError(Exception):
    """Error raised when couldn't find a unique name for the link."""


def version_callback(*, value: bool) -> None:
    """Print the version."""
    if value:
        print(f"pylnlst {__version__}")
        raise typer.Exit


def fail_if_not_exists(path_to_file: Path) -> None:
    """Raise error if the given path does not point to an existing file."""
    if not path_to_file.exists():
        msg = f"File '{path_to_file}' does not exist"
        raise FileNotFoundError(msg)


def files_from_filelist(
    filelist: Path | str,
    base_dir: Path | str | None,
) -> Iterator[Path]:
    """Return the next file in the filelist."""
    if isinstance(filelist, str):
        filelist = Path(filelist)
    fail_if_not_exists(filelist)

    with Path.open(filelist) as filelist_obj:
        for line in filelist_obj:
            stripped_line = line.strip()
            if stripped_line.startswith("#") or len(stripped_line) == 0:
                continue
            path_to_file = (
                base_dir / Path(stripped_line)
                if base_dir is not None
                else Path(stripped_line)
            )
            try:
                fail_if_not_exists(path_to_file)
            except FileNotFoundError as e:
                print(
                    f"[red][bold]ERROR in filelist files: ({e}) "
                    "Are you missing --base-src-dir?[/bold][/red] :x:",
                )
                raise typer.Exit(code=1) from e
            yield path_to_file


def get_symbolic_link_name(dst_dir: Path, file: Path) -> Path:
    """Calculate a symbolic link name as a Path object."""
    link_name = dst_dir / file.name
    if link_name.exists():
        for i in range(MAX_CLASHING_FILE_INDEX):
            ext = link_name.suffix
            filename_wo_ext = link_name.stem
            parent = link_name.parent
            candidate_link_name = parent / f"{filename_wo_ext}_{i:03}{ext}"
            if not candidate_link_name.exists():
                link_name = candidate_link_name
                break
        if link_name.exists():
            err_msg = (
                f"Exhausted all possible names for {dst_dir / file.name}: "
                f"{link_name} exists"
            )
            raise LinkNameExhaustedError(err_msg)
    return link_name


def pylnlst(
    list_file: Annotated[
        Path,
        typer.Option(
            exists=True,
            dir_okay=False,
            file_okay=True,
            readable=True,
            resolve_path=True,
            show_default=False,
            help=FILE_LIST_DOC,
        ),
    ],
    dst_dir: Annotated[
        Path,
        typer.Option(
            exists=True,
            dir_okay=True,
            file_okay=False,
            readable=True,
            writable=True,
            resolve_path=True,
            show_default=False,
            help=DST_DIR_DOC,
        ),
    ],
    base_src_dir: Annotated[
        Path | None,
        typer.Option(
            exists=False,
            dir_okay=True,
            file_okay=False,
            readable=True,
            resolve_path=True,
            show_default=False,
            help=BASE_SRC_DIR_DOC,
        ),
    ] = None,
    _: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Automate the creation of symbolic links in a destination directory.

    pylnlst automate the creation of symbolic links by using a list of file
    paths from a specified file and creates symbolic links for each entry in a
    designated target directory.
    The source files can be optionally prefixed by a base directory.
    This tool can process files having spaces, brackets, or special characters
    in their names.
    """
    for file in files_from_filelist(list_file, base_src_dir):
        try:
            print(f"'{file}': ", end="")
            link_name = get_symbolic_link_name(dst_dir, file)
            link_name.symlink_to(file.resolve())
        except LinkNameExhaustedError:
            print(
                "[red][bold]ERROR (could not find valid name)[/bold][/red] :x:",
            )
        except OSError:
            print("[red][bold]ERROR (OS related error)[/bold][/red] :x:")
        else:
            if link_name.name != file.name:
                print(
                    "[yellow][bold]Copied (destination link was renamed)"
                    "[/bold][/yellow] :white_check_mark:",
                )
            else:
                print("[green][bold]OK[/bold][/green] :white_check_mark:")


def main() -> None:
    """Entry point for the CLI app."""
    typer.run(pylnlst)


if __name__ == "__main__":
    main()
