import typing as t
from pathlib import Path
from tomllib import loads  # type: ignore


class PyProjectConfig:
    cwd: Path
    pyproject: Path
    vt_config: t.Dict[str, t.Any]

    npm_exec: str
    npx_exec: str
    serve_app: str
    vite_apps: t.List[t.Dict[str, t.Any]]

    def __init__(self) -> None:
        self.cwd = Path.cwd()
        self.pyproject = self.cwd / "pyproject.toml"
        self.load_pyproject()

    def load_pyproject(self) -> None:
        if not self.pyproject.exists():
            raise FileNotFoundError("pyproject.toml not found.")

        pyproject_raw = loads(str(self.pyproject.read_text()))
        self.vt_config = pyproject_raw.get("tool", {}).get("vite_transporter", {})
        self.npm_exec = self.vt_config.get("npm_exec", "npm")
        self.npx_exec = self.vt_config.get("npx_exec", "npx")
        self.serve_app = self.vt_config.get("serve_app", "app")
        self.vite_apps = self.vt_config.get("vite_apps", [])

    def __enter__(self) -> "PyProjectConfig":
        return self

    def __exit__(self, exc_type: t.Any, exc_val: t.Any, exc_tb: t.Any) -> None:
        return None
