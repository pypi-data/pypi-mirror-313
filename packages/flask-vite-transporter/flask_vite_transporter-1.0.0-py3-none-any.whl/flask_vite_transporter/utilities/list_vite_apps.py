import sys
import typing as t

from .sprinkles import Sprinkles


def list_vite_apps(vite_apps_found: t.List[t.Dict[str, t.Any]]) -> None:
    print("")
    if not vite_apps_found:
        print(
            f" {Sprinkles.WARNING}No vite apps found in pyproject.toml{Sprinkles.END}"
        )
    else:
        for app in vite_apps_found:
            print(
                f"{Sprinkles.OKGREEN}{app.get('vite_app')}/dist/assets{Sprinkles.END} "
                f"{Sprinkles.BOLD}=>{Sprinkles.END} "
                f"{Sprinkles.OKGREEN}{app.get('serve_app')}/vt/{app.get('vite_app')}/{Sprinkles.END}"
            )
    print("")
    sys.exit(0)
