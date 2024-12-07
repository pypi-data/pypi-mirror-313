def infer_filetype(path: str) -> str:
    """
    Infers the file type of a given file using both libmagic and file extension
    methods. It first tries to identify the file type using libmagic. If
    libmagic is not available or cannot determine the file type, it falls back
    to identifying based on the file extension.

    :param path: The path to the file whose file type needs to be inferred.
    :return: The inferred file type as a string ('txt', 'csv', 'json', 'parquet'),
             or an empty string if the file type cannot be determined.
    """
    return infer_by_magic(path) or infer_by_extension(path)


def infer_by_extension(path: str) -> str:
    """
    Infers the file type based on the file extension. This function maps common
    file extensions to their respective file types.

    :param path: The path to the file including its extension.
    :return: The inferred file type as a string ('txt', 'csv', 'json', 'parquet'),
             or an empty string if the extension does not match known types.
    """
    extension = path.split(".")[-1].lower()

    filetype_map = {"txt": "txt", "csv": "csv", "json": "json", "parquet": "parquet"}

    return filetype_map.get(extension, "")


def infer_by_magic(path: str) -> str:
    """
    Infers the file type using the libmagic library, which analyzes the content
    of the file. This method is more reliable than inferring based on the file
    extension but requires the libmagic library to be installed. If libmagic is
    not installed, this function returns an empty string.

    Note: The identification of some file types like 'parquet' might be
    unreliable as it often returns generic MIME types such as
    'application/octet-stream'.

    :param path: The path to the file for which the file type is to be inferred.
    :return: The inferred file type as a string ('txt', 'csv', 'json'),
             or an empty string if the file type cannot be determined or libmagic
             is not available.
    """
    # try to use libmagic if available
    try:
        import magic
    except ModuleNotFoundError:
        return ""

    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(path)

    # note that parquet mimetype often looks like `application/octet-stream`
    # and so should be considered unreliable for identification
    filetype_map = {
        "text/plain": "txt",
        "text/csv": "csv",
        "application/json": "json",
        "application/x-ndjson": "json",
    }

    return filetype_map.get(mime_type, "")
