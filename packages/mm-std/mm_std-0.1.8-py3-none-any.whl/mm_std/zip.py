from zipfile import ZipFile


def read_text_from_zip_archive(zip_archive_path: str, filename: str | None = None, password: str | None = None) -> str:
    with ZipFile(zip_archive_path) as zipfile:
        if filename is None:
            filename = zipfile.filelist[0].filename
        return zipfile.read(filename, pwd=password.encode() if password else None).decode()
