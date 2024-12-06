import typing as t

from .pyproject_config import PyProjectConfig


def load_vite_apps(pyproject_config: PyProjectConfig) -> t.List[t.Dict[str, t.Any]]:
    vite_apps = []
    for vite_app in pyproject_config.vite_apps:
        vite_apps.append(
            {
                "vite_app": vite_app,
                "serve_app": pyproject_config.vt_config.get("serve_app"),
            }
        )
    return vite_apps
