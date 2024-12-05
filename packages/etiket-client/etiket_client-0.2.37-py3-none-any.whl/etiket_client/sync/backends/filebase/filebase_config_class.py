import pathlib, dataclasses

@dataclasses.dataclass
class FileBaseConfigData:
    root_directory: pathlib.Path
    server_folder : bool