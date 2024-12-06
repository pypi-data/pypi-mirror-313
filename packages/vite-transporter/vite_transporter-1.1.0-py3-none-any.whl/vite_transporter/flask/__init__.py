import sys
import typing as t
from pathlib import Path

from vite_transporter.elements import BodyContent, ScriptTag, LinkTag
from vite_transporter.globals import HTTP_HEADERS
from vite_transporter.utilities import Sprinkles

if "flask" in sys.modules:
    from flask import Flask, url_for, Response, Blueprint
    from markupsafe import Markup
else:
    raise ImportError("Flask is not installed.")


class ViteTransporter:
    app: t.Optional[Flask]
    vt_root_path: Path

    cors_allowed_hosts: t.Optional[t.List[str]]

    def __init__(
        self,
        app: t.Optional[Flask] = None,
        cors_allowed_hosts: t.Optional[t.List[str]] = None,
    ) -> None:
        if app is not None:
            self.init_app(app, cors_allowed_hosts)

    def init_app(
        self, app: Flask, cors_allowed_hosts: t.Optional[t.List[str]] = None
    ) -> None:
        if app is None:
            raise ImportError("No app was passed in.")
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")

        self.app = app
        self.cors_allowed_hosts = cors_allowed_hosts

        if "vite_transporter" in self.app.extensions:
            raise ImportError(
                "The app has already been initialized with vite-to-flask."
            )

        self.app.extensions["vite_transporter"] = self
        self.app.config["VTF_APPS"] = {}
        self.vt_root_path = Path(app.root_path) / "vite"

        if not self.vt_root_path.exists():
            print(
                f"{Sprinkles.WARNING}{Sprinkles.BOLD}vt folder not found, a new one was created.{Sprinkles.END}{Sprinkles.END}\n\r"
                f"{Sprinkles.OKCYAN}{self.vt_root_path}{Sprinkles.END}\n\r"
            )
            self.vt_root_path.mkdir()

        for folder in self.vt_root_path.iterdir():
            if folder.is_dir():
                self.app.config["VTF_APPS"].update({folder.name: folder})

        self._load_blueprint(app)
        self._load_context_processor(app)
        self._load_cors_headers(app, self.cors_allowed_hosts)

    def _load_blueprint(self, app: Flask) -> None:
        app.register_blueprint(
            Blueprint(
                "__vite__",
                __name__,
                url_prefix="/--vite--",
                static_folder=f"{app.root_path}/vite",
                static_url_path="/",
            )
        )

    @staticmethod
    def _load_context_processor(app: Flask) -> None:
        @app.context_processor
        def vt_head_processor() -> t.Dict[str, t.Callable[..., t.Any]]:
            def vt_head(vite_app: str) -> t.Any:
                vite_assets = Path(app.root_path) / "vite" / vite_app
                find_vite_js = vite_assets.glob("*.js")
                find_vite_css = vite_assets.glob("*.css")

                tags: t.List[t.Union[ScriptTag, LinkTag]] = []

                for file in find_vite_js:
                    tags.append(
                        ScriptTag(
                            src=url_for(
                                "__vite__.static", filename=f"{vite_app}/{file.name}"
                            ),
                            type_="module",
                        )
                    )

                for file in find_vite_css:
                    tags.append(
                        LinkTag(
                            rel="stylesheet",
                            href=url_for(
                                "__vite__.static", filename=f"{vite_app}/{file.name}"
                            ),
                        )
                    )

                return Markup("".join([tag.raw() for tag in tags]))

            return dict(vt_head=vt_head)

        @app.context_processor
        def vt_body_processor() -> t.Dict[str, t.Callable[..., t.Any]]:
            def vt_body(
                root_id: str = "root",
                noscript_message: str = "You need to enable JavaScript to run this app.",
            ) -> t.Any:
                return BodyContent(root_id, noscript_message)()

            return dict(vt_body=vt_body)

    @staticmethod
    def _load_cors_headers(
        app: Flask, cors_allowed_hosts: t.Optional[t.List[str]] = None
    ) -> None:
        if cors_allowed_hosts:
            print(
                f"\n\r{Sprinkles.WARNING}{Sprinkles.BOLD}vite-transporter is disabling CORS restrictions for:"
                f"{Sprinkles.END}{Sprinkles.END}\n\r"
                f"{Sprinkles.OKCYAN}{', '.join(cors_allowed_hosts)}{Sprinkles.END}\n\r"
            )

            @app.after_request
            def after_request(response: Response) -> Response:
                response.headers["Access-Control-Allow-Origin"] = ", ".join(
                    cors_allowed_hosts
                )
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    HTTP_HEADERS
                )
                response.headers["Access-Control-Allow-Methods"] = "*"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
