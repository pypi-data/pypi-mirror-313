# merge two word files

import functools


def check_file_exist(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")


def check():
    def wrapper(func):
        @functools.wraps(func)
        def inner(original_docx_name, append_docx_name, output_path, *args, **kwargs):
            for file in [original_docx_name, append_docx_name]:
                check_file_exist(file)
            return func(
                original_docx_name, append_docx_name, output_path, *args, **kwargs
            )

        return inner

    return wrapper
