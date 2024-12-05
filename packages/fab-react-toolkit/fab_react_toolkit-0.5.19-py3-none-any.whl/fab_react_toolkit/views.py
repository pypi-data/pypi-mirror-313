import json
import os

from flask import url_for
from flask_appbuilder import BaseView, expose, IndexView as FABIndexView
from .apis import OpenApi

class OpenAPIView(BaseView):
    route_base = "/openapi"
    default_view = "show"

    @expose("/<version>")
    def show(self, version):
        return self.render_template(
            self.appbuilder.app.config.get(
                "FAB_API_SWAGGER_TEMPLATE", "appbuilder/swagger/swagger.html"
            ),
            openapi_uri=url_for(OpenApi.__name__ + '.' +
                                OpenApi.get.__name__, version=version),
        )


class IndexView(FABIndexView):
    index_template = 'index.html'
    route_base = "/"

    def __init__(self, **kwargs):
        self.base_path = os.getenv("SCRIPT_NAME", "")  + "/"
        super().__init__(**kwargs)
    

    def _do_render(self):
        return self.render_template(self.index_template, appbuilder=self.appbuilder, base_path=self.base_path)

    @expose("/<string:path>")
    @expose("/<path:path>")
    def index_all(self, path):
        return self._do_render()

    @expose("/")
    def index(self):
        return self._do_render()