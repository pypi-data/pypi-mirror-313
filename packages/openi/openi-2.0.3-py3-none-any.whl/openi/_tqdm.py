from __future__ import annotations

from typing import Optional

from tqdm.auto import tqdm


class FileProgressBar(tqdm):
    """
    Customized `Tqdm` class for OpenI uploads and downloads.
    It displays a file progress bar of the operation.


    Args:
        display_name (`str`):
            The name of the file being uploaded or downloaded.
        size (`int`):
            The total size of the file in bytes.
        position (`int`, `optional`, defaults to `0`):
            The display position of the progress bar if multiple bars are created.
        initial (`int`, `optional`, defaults to `0`):
            The initial progress of the progress bar.
        colour (`str`, `optional`, defaults to `None`):
            The colour of the progress bar.
        max_width (`int`, `optional`, defaults to `None`):
            The maximum width of the `display_name` parameter.
            If provided, the `display_name` will be truncated to this length.

    Example:
    ```python
    >>> pbar = FileProgressBar("sample.zip", 1024*1024*64)
    ⏳ sample.zip:   0%|          | 0.00/64.0M [00:00<?, ?B/s]

    >>> pbar.update(1024*1024*32)
    ⏳ sample.zip:   50%|█████     | 32.0M/64.0M [00:00<?, ?B/s]
    ```
    """

    def __init__(
        self,
        display_name: str,
        size: int,
        position: int = 0,
        initial: int = 0,
        colour: Optional[str] = None,
        max_width: Optional[int] = None,
    ):
        if max_width:
            if len(display_name) > max_width:
                display_name = f"…{display_name[-1 * max_width :]}"
            else:
                display_name = f"{display_name.rjust(max_width + 1)}"

        self.display_name = display_name
        desc = f"⏳ {display_name}"

        super().__init__(
            total=size,
            initial=initial,
            desc=desc,
            position=position,
            colour=colour,
            dynamic_ncols=True,
            unit_scale=True,
            unit_divisor=1024,
            unit="B",
        )

    def waiting(self) -> None:
        self.set_description_str(f"⏳ {self.display_name}")

    def uploading(self) -> None:
        self.set_description_str(f"⬆️ {self.display_name}")
        self.refresh()

    def downloading(self) -> None:
        self.set_description_str(f"⬇️ {self.display_name}")
        self.refresh()

    def completed(self) -> None:
        self.set_description_str(f"✅ {self.display_name}")
        self.colour = "green"
        self.refresh()
        self.close()

    def failed(self) -> None:
        self.set_description_str(f"❌ {self.display_name}")
        self.colour = "red"
        self.refresh()
        self.close()

    def skipped(self, msg) -> None:
        self.set_description_str(f"➖ {msg}")
        # self.n = self.total
        # self.colour = "green"
        self.refresh()
        self.close()


def create_pbar(
    display_name: str,
    size: int,
    position: int = 0,
    initial: int = 0,
) -> FileProgressBar:
    return FileProgressBar(
        display_name=display_name,
        size=size,
        position=position,
        initial=initial,
    )


def close_all_pbar(pbar_list: list[FileProgressBar]) -> None:
    for pbar in pbar_list:
        pbar.close()


# def create_pbar_list(
#     list_of_files: Union[LocalFile, ModelFile, DatasetFile]
# ) -> List[FileProgressBar]:
#     list_of_files_pbars: List[FileProgressBar] = list()
#
#     for pos, f in enumerate(list_of_files):
#         if isinstance(f, ModelFile):
#             filename = f.fileName
#         if isinstance(f, DatasetFile):
#             filename = f.name
#         if isinstance(f, LocalFile):
#             filename = f.name
#
#         filesize = f.size
#
#         pbar = create_pbar(
#             display_name=filename,
#             size=filesize,
#             position=pos,
#         )
#         list_of_files_pbars.append(pbar)
#
#     return list_of_files_pbars
