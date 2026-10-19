"""Create/update a storage-mode Lovelace dashboard from a YAML source file.

Runs ON the Home Assistant host (SSH add-on), talking to Core's websocket
through the Supervisor proxy with $SUPERVISOR_TOKEN - no long-lived token needed.
Needs PyYAML (present in the SSH add-on) and `websockets` on PYTHONPATH.

Source file layout (see dashboards/tablet2.yaml):
  dashboard: {url_path, title, icon, require_admin, show_in_sidebar}
  config:    the Lovelace config (views, ...)
`!file name.md` anywhere in the YAML is replaced by that file's text, read
relative to the YAML file, so markdown card bodies can be shared between dashboards.
`!template {file: name.yaml, vars: {k: v}}` is replaced by that YAML file parsed after
substituting each ${k}, so one view/card layout can be reused with different entities.

Usage: python3 deploy_dashboard.py path/to/dashboard.yaml
"""
import asyncio
import json
import os
import string
import sys

import websockets
import yaml

WS_URL = "ws://supervisor/core/websocket"


def load_source(path):
    """Parse the dashboard YAML, resolving !file tags relative to its folder."""
    base = os.path.dirname(os.path.abspath(path))

    def file_tag(loader, node):
        with open(os.path.join(base, loader.construct_scalar(node)), encoding="utf-8") as f:
            return f.read().rstrip("\n")

    def template_tag(loader, node):
        spec = loader.construct_mapping(node, deep=True)
        with open(os.path.join(base, spec["file"]), encoding="utf-8") as f:
            text = string.Template(f.read()).substitute(spec.get("vars", {}))
        return yaml.safe_load(text)

    yaml.SafeLoader.add_constructor("!file", file_tag)
    yaml.SafeLoader.add_constructor("!template", template_tag)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


async def call(ws, msg_id, payload):
    """Send one websocket command and return its result, raising on failure."""
    await ws.send(json.dumps({"id": msg_id, **payload}))
    while True:
        reply = json.loads(await ws.recv())
        if reply.get("id") == msg_id:
            if not reply.get("success"):
                raise RuntimeError(f"{payload['type']} failed: {reply.get('error')}")
            return reply.get("result")


async def deploy(src):
    """Create the dashboard if it does not exist, then save its config."""
    meta, config = src["dashboard"], src["config"]
    async with websockets.connect(WS_URL, max_size=None) as ws:
        await ws.recv()  # auth_required
        await ws.send(json.dumps({"type": "auth", "access_token": os.environ["SUPERVISOR_TOKEN"]}))
        if json.loads(await ws.recv()).get("type") != "auth_ok":
            raise RuntimeError("websocket auth failed")

        dashboards = await call(ws, 1, {"type": "lovelace/dashboards/list"})
        if not any(d["url_path"] == meta["url_path"] for d in dashboards):
            await call(ws, 2, {"type": "lovelace/dashboards/create", "mode": "storage", **meta})
            print(f"created dashboard /{meta['url_path']}")

        await call(ws, 3, {"type": "lovelace/config/save", "url_path": meta["url_path"], "config": config})
        print(f"saved config to /{meta['url_path']} ({len(config['views'])} view(s))")


if __name__ == "__main__":
    asyncio.run(deploy(load_source(sys.argv[1])))
