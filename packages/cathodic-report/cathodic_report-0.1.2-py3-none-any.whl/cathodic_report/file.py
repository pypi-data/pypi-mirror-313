def write_to_md(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
