from mx_stream_core.config.delta import delta_path


def get_delta_path(table_name=None) -> str:
    if table_name is not None:
        return f"{delta_path}/{table_name}"
    print("path: ", delta_path)
    return delta_path
