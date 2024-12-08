from .plugin import Plugin


class RouterPlugin(Plugin):
    default_options = {
        "app_engine": None,
        "auto_options": None,
        "decompress_gzip": 0,
        "disable_access_log": False,
        "disable_gzip": False,
        "disable_handle_method_not_allowed": None,
        "disable_redirect_fixed_path": True,
        "error_body": {},
        "forwarded_by_client_ip": False,
        "health_path": "/__health",
        "hide_version_header": False,
        "logger_skip_paths": [],
        "max_multipart_memory": None,
        "max_payload": 0,
        "remote_ip_headers": [],
        "remove_extra_slash": False,
        "return_error_msg": False,
        "trusted_proxies": [],
    }
