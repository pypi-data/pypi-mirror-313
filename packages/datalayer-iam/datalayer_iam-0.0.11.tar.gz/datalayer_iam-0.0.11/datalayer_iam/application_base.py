# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from datalayer_iam import __version__

from traitlets import Bool, Unicode

from datalayer_core.application import DatalayerApp, base_aliases, base_flags


datalayer_iam_aliases = dict(base_aliases)
datalayer_iam_aliases["cloud"] = "DatalayerIAMBaseApp.cloud"
datalayer_iam_aliases["server-base-url"] = "DatalayerIAMBaseApp.server_base_url"
datalayer_iam_aliases["server-base-ws-url"] = "DatalayerIAMBaseApp.server_base_ws_url"
datalayer_iam_aliases["server-token"] = "DatalayerIAMBaseApp.server_token"

datalayer_iam_flags = dict(base_flags)
datalayer_iam_flags["no-minimize"] = (
    {"DatalayerIAMBaseApp": {"minimize": False}},
    "Do not minimize a production build.",
)


class DatalayerIAMBaseApp(DatalayerApp):
    name = "datalayer_iam"

    version = __version__

    aliases = datalayer_iam_aliases

    flags = datalayer_iam_flags

    cloud = Unicode("ovh", config=True, help="")

    minimize = Bool(True, config=True, help="")

    server_base_url = Unicode("http://localhost:8888", config=True, help="")

    server_base_ws_url = Unicode("ws://localhost:8888", config=True, help="")

    server_token = Unicode("60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6", config=True, help="")

    router_url = Unicode("http://jupyter-router-api-svc:2001/api/routes", config=True, help="")

    router_token = Unicode("test", config=True, help="")

    lang = Unicode("python", config=True, help="")

    kernel_id = Unicode(None, allow_none=True, config=True, help="")
