def copy_arg(
    source: dict, dest: dict, source_name: str, dest_name: str | None = None
):
    if source_name in source:
        if dest_name is None:
            dest[source_name] = source[source_name]
        else:
            dest[dest_name] = source[source_name]
