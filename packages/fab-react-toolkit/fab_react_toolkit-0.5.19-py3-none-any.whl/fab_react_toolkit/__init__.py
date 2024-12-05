from flask import render_template_string, send_file
from .views import OpenAPIView, IndexView 
from .apis import AuthApi, InfoApi, PermissionViewApi, PermissionsApi, RolesApi, UsersApi, ViewsMenusApi, OpenApi
from .api import ModelRestApi
from .interface import SQLAInterface

import io
class FABReactToolkit(object):

    def __init__(self, appbuilder):
        self.appbuilder = appbuilder
        self.appbuilder.react_toolkit = self
        self.appbuilder.app.config.setdefault("FAB_REACT_AUTH", True)
        self.appbuilder.app.config.setdefault("FAB_REACT_INFO", True)
        self.appbuilder.app.config.setdefault("FAB_REACT_SEC", True)
        self.appbuilder.app.config.setdefault("FAB_REACT_OPENAPI", True)
        self.appbuilder.app.config.setdefault("FAB_REACT_CONFIG", {})
        
        if self.appbuilder.app.config.get("FAB_REACT_AUTH"):
            self.appbuilder.add_api(AuthApi)
        if self.appbuilder.app.config.get("FAB_REACT_INFO"):
            self.appbuilder.add_api(InfoApi)
        if self.appbuilder.app.config.get("FAB_REACT_SEC"):
            self.appbuilder.add_api(AuthApi)
            self.appbuilder.add_api(PermissionViewApi)
            self.appbuilder.add_api(PermissionsApi)
            self.appbuilder.add_api(RolesApi)
            self.appbuilder.add_api(UsersApi)
            self.appbuilder.add_api(ViewsMenusApi)

        if self.appbuilder.app.config.get("FAB_REACT_OPENAPI"):
            self.appbuilder.add_api(OpenApi)
            self.appbuilder.add_view_no_menu(OpenAPIView)

        @self.appbuilder.app.route('/server-config.js', methods=['GET'])
        def js_manifest():
            content = render_template_string('window.fab_react_config = {{ react_vars |tojson }}',
                                    react_vars=self.appbuilder.app.config["FAB_REACT_CONFIG"]).encode('utf-8')
            scriptfile = io.BytesIO(content)
            return send_file(scriptfile, mimetype='application/javascript', download_name="server-config.js")            
