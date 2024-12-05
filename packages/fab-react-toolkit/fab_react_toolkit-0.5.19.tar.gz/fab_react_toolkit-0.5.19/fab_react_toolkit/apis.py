import jwt
import re
import datetime
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.ext.marshmallow.common import resolve_schema_cls
from flask import Response, request, redirect, g, current_app, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_appbuilder import expose
from flask_appbuilder.api import BaseApi, Model2SchemaConverter, safe
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.utils.base import get_safe_redirect
from flask_appbuilder.security.manager import AUTH_DB, AUTH_LDAP, AUTH_REMOTE_USER
from flask_appbuilder.security.sqla.models import User, Permission, PermissionView, Role, ViewMenu
from werkzeug.security import generate_password_hash
from flask_appbuilder.const import (
    API_SECURITY_PASSWORD_KEY,
    API_SECURITY_USERNAME_KEY,
)

from .api.decorators import login_required
from .api import ModelRestApi


class InfoApi(BaseApi):
    resource_name = "info"
    openapi_spec_tag = "Info"

    security_level_apis = ['PermissionsApi', 'RolesApi', 'UsersApi', 'ViewsMenusApi', 'PermissionViewApi']
    excluded_apis = ['OpenApi', 'MenuApi', 'SecurityApi', 'InfoApi', 'AuthApi']

    @expose("/", methods=["GET"])
    @login_required
    def get_info(self):
        """An endpoint for retreiving the menu.
        ---
        get:
          description: >-
            Get the api structure.
            Returns a forest like structure with details about the ip
          responses:
            200:
              description: Get Info
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      apis:
                        description: Api items in a list
                        type: array
                        items:
                          type: object
                          properties:
                            name:
                              description: >-
                                The internal api name, maps to permission_name
                              type: string
                            type:
                              description: Api type. One of [security, default]
                              type: string
                            level:
                              description: Api permission level
                              type: string
            401:
              $ref: '#/components/responses/401'
        """

        apis = []
        for base_api in self.appbuilder.baseviews:
            if isinstance(base_api, BaseApi) and base_api.class_permission_name not in self.excluded_apis:
                name = base_api.list_title if isinstance(base_api,
                                                         ModelRestApi) else base_api.resource_name.capitalize()
                icon = base_api.icon if hasattr(base_api, 'icon') else ''
                path = base_api.resource_name
                api_type = 'default' if not isinstance(base_api, ModelRestApi) else 'table'
                level = 'default' if base_api.class_permission_name not in self.security_level_apis else 'security'
                permission_name = base_api.class_permission_name

                apis.append(
                    {'name': name, 'icon': icon, 'permission_name': permission_name, 'path': path,
                     'type': api_type, 'level': level})

        return self.response(200, **{"apis": apis})


""" 
These should prob be in the core

Even though API_SECURITY_PROVIDER_DB and API_SECURITY_PROVIDER_LDAP are exposed, the associated Key 
API_SECURITY_PROVIDER_KEY is "provider" which collides with providers of the `oauth` method

"""

API_SECURITY_METHOD_DB = "db"
API_SECURITY_METHOD_LDAP = "ldap"
API_SECURITY_METHOD_OAUTH = "oauth"
API_SECURITY_METHOD_REMOTE = "remote"
API_SECURITY_OAUTH_PROVIDER_KEY = "oauth_provider"
API_SECURITY_FIRSTNAME_KEY = "firstname"
API_SECURITY_LASTNAME_KEY = "lastname"
API_SECURITY_EMAIL_KEY = "email"


class AuthApi(BaseApi):
    """
    This provides the inbuilt authentication features through an API
    For more information see flask_appbuilder.security.modelviews

    flask_appbuilder.security.api.SecurityApi was used as reference but reworked,
    since it simply returns the jwt access and refresh token as json contrary to the functionality of
    flask_appbuilder.security.modelviews where the tokens (with additional information) are stored in
    a signed httpOnly cookie

    Caveats: Doesn't support "Open ID" (since it refers to OpenID 2.0, which is deprecated).
             Doesn't support "REMOTE_USER"

    Fore more details see https://flask-appbuilder.readthedocs.io/en/latest/security.html
    """
    resource_name = "auth"
    # TODO: The datamodel of UserApi should be the same as the user_model in SecurityManger
    datamodel = SQLAInterface(User)
    model2schemaconverter = Model2SchemaConverter
    allow_browser_login = True
    show_exclude_columns = ['password', 'changed', 'created', 'changed_by', 'created_by']

    def __init__(self):
        super().__init__()
        list_cols = self.datamodel.get_user_columns_list()
        self.show_columns = [x for x in list_cols if x not in self.show_exclude_columns]
        self.model2schemaconverter = self.model2schemaconverter(self.datamodel, {})

    def get_client_user_data(self, user):
        """
        Creates user data to be exposed to the client (this should probably be part of user's db data)
        :param user: raw user data from db
        :return: user data where sensitive data is filtered and menu permission data is added
        """

        # use marshmallow to serialize data
        show_model_schema = self.model2schemaconverter.convert(self.show_columns)
        user_data = show_model_schema.dump(user, many=False)

        # get menu permissions - this could be more sophisticated
        sm = self.appbuilder.sm

        roles = [role.name for role in user.roles]
        permissions = [x for x in set([v for k, v in sm.get_user_permissions(user)]) if sm.has_access("can_get", x)]
        user_data['permissions'] = permissions
        user_data['roles'] = roles

        return user_data

    @expose('/login', methods=["POST"])
    @safe
    def login(self):
        """Login endpoint for the API, creates a session cookie
         ---
         post:
           description: >-
             Authenticate and create a session cookie
           requestBody:
             required: true
             content:
               application/json:
                 schema:
                   type: object
                   properties:
                     username:
                       description: The username for authentication
                       example: user1234
                       type: string
                       required: true
                     password:
                       description: The password for authentication
                       example: complex-password
                       type: string
                       required: true
           responses:
             200:
               description: Authentication Successful
             400:
               $ref: '#/components/responses/400'
             401:
               $ref: '#/components/responses/401'
             500:
               $ref: '#/components/responses/500'
         """

        if current_user is not None and current_user.is_authenticated:
            user_data = self.get_client_user_data(current_user)
            return self.response(200, **user_data)

        # Read and validate request body
        if not request.is_json:
            return self.response_400(message="Request payload is not JSON")
        username = request.json.get(API_SECURITY_USERNAME_KEY, None)
        password = request.json.get(API_SECURITY_PASSWORD_KEY, None)

        if not username or not password:
            return self.response_400(message="Missing required parameter")

        # Authenticate based on method
        user = None
        method = self.appbuilder.sm.auth_type
        if method == AUTH_DB:
            user = self.appbuilder.sm.auth_user_db(username, password)
        elif method == AUTH_LDAP:
            user = self.appbuilder.sm.auth_user_ldap(username, password)

        elif method == AUTH_REMOTE_USER:
            username = request.environ.get("REMOTE_USER")
            if username:
                user = self.appbuilder.sm.auth_user_remote_user(username)
        else:
            return self.response_500(
                message="Method {} not supported".format(method)
            )
        if not user:
            return self.response_401()

        # get client user data
        user_data = self.get_client_user_data(user)
        # Set session cookie
        login_user(user, remember=False)
        return self.response(200, **user_data)

    @expose('/login/<provider>', methods=["GET"])
    @safe
    def init_oauth(self, provider):
        """OAuth initiation endpoint for the API
         ---
          get:
            description: >-
              Initiate OAuth login
            parameters:
              - in: path
                name: provider
                schema:
                  type: str
                required: true
                description: Provider to authenticate against

            responses:
              302:
                $ref: '#/components/responses/202'
              500:
                $ref: '#/components/responses/500'
         """
        if provider is None:
            return self.response_400(message="Missing required parameter")

        state = jwt.encode(
            request.args.to_dict(flat=False),
            self.appbuilder.app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        try:
            if provider == "twitter":
                # not works
                return self.appbuilder.sm.oauth_remotes[provider].authorize_redirect(
                    url_for("AuthApi.oauth_authorized", provider=provider, _external=True, state=state)
                )
            else:
                return self.appbuilder.sm.oauth_remotes[provider].authorize_redirect(
                    url_for("AuthApi.oauth_authorized", provider=provider, _external=True),
                    state=state.decode("ascii") if isinstance(state, bytes) else state,
                )

        except Exception as e:
            print(e)
            return self.response_500()

    @expose("/oauth-authorized/<provider>")
    def oauth_authorized(self, provider):
        """OAuth redirect endpoint for the API, creates a session cookie
           Make sure to add this endpoint as the redirect uri of your provider
         ---
          get:
            description: >-
              Authenticate and create a session cookie
            parameters:
              - in: path
                name: provider
                schema:
                  type: str
                required: true
                description: Provider to authenticate against

            responses:
              302:
                $ref: '#/components/responses/202'
              400:
                $ref: '#/components/responses/400'
              500:
                $ref: '#/components/responses/500'
         """
        if provider not in self.appbuilder.sm.oauth_remotes:
            return self.response_400(message="Provider not supported")
        try:
          resp = self.appbuilder.sm.oauth_remotes[provider].authorize_access_token()
        except Exception as e:
            return self.response_500(message=f"Error authorizing OAuth access token for {str(e)}")
        
        if resp is None:
            return self.response_400(message="Request for sign in was denied.")

        # Retrieves specific user info from the provider
        try:
            self.appbuilder.sm.set_oauth_session(provider, resp)
            userinfo = self.appbuilder.sm.oauth_user_info(provider, resp)
        except Exception as e:
            user = None
        else:
            # User email is not whitelisted
            if provider in self.appbuilder.sm.oauth_whitelists:
                whitelist = self.appbuilder.sm.oauth_whitelists[provider]
                allow = False
                for email in whitelist:
                    if "email" in userinfo and re.search(email, userinfo["email"]):
                        allow = True
                        break
                if not allow:
                    self.response_401()
            user = self.appbuilder.sm.auth_user_oauth(userinfo)
        if user is None:
            return self.response_400(message="Invalid login. Please try again.")
        else:
            try:
                # redirect uri could be stored in state, I don't see the point though
                state = jwt.decode(
                    request.args["state"],
                    self.appbuilder.app.config["SECRET_KEY"],
                    algorithms=["HS256"],
                )
            except jwt.InvalidTokenError:
                raise Exception("State signature is not valid!")

            login_user(user)

            next_url = self.appbuilder.app.config.get("REDIRECT_URI", self.appbuilder.get_url_for_index)
            # Check if there is a next url on state
            if "next" in state and len(state["next"]) > 0:
                next_url = get_safe_redirect(state["next"][0])

            return redirect(next_url)

    @expose('/logout', methods=["GET"])
    @safe
    def logout(self):
        """Logs the user out and deletes session cookie"""
        logout_user()
        return self.response(200, message="Logout successful")

    @expose('/signup', methods=["POST"])
    @safe
    def signup(self):
        """
        This endpoint creates a new user

        More info:
        - The base logic will register users for LDAP and OAuth automatically with a predefined model.
          DB will expect user data by the client using a predefined model.
        - To customize the registration flow for DB, LDAP or OAuth (for example to add custom data to registration)
          create a custom SecurityManager class. As a starting point see `auth_user_db`, `auth_user_ldap` or
          `auth_user_oauth` methods in flask_appbuilder.security.sqla/manager.manager.SecurityManager.
          Adjust the front end accordingly.
        ---
        post:
          description: >-
            Register user and create a session cookie
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    username:
                      description: The username of the new user
                      example: user1234
                      type: string
                      required: true
                    firstname:
                      description: The first name of the new user
                      example: John
                      type: string
                      required: true
                    lastname:
                      description: The last name of the new user
                      example: Doe
                      type: string
                      required: true
                    email:
                      description: The last name of the new user
                      example: Doe
                      type: string
                      required: true
                    password:
                      description: The password for authentication
                      example: complex-password
                      type: string
                      required: true
          responses:
            200:
              description: Authentication Successful
            400:
              $ref: '#/components/responses/400'
            500:
              $ref: '#/components/responses/500'
         """
        if not self.appbuilder.get_app.config["AUTH_USER_REGISTRATION"]:
            self.response_500()

        # read and validate data
        username = request.json.get(API_SECURITY_USERNAME_KEY, None)
        firstname = request.json.get(API_SECURITY_FIRSTNAME_KEY, None)
        lastname = request.json.get(API_SECURITY_LASTNAME_KEY, None)
        email = request.json.get(API_SECURITY_EMAIL_KEY, None)
        password = request.json.get(API_SECURITY_PASSWORD_KEY, None)

        if not username or not firstname or not lastname or not email or not password:
            return self.response_400(message="Missing required parameter")

        password = generate_password_hash(password)
        if not self.appbuilder.sm.add_user(
                username=username,
                email=email,
                first_name=firstname,
                last_name=lastname,
                role=self.appbuilder.sm.find_role(
                    self.appbuilder.sm.auth_user_registration_role
                ),
                hashed_password=password,
        ):
            return self.response_500()
        else:
            return self.response(200, message="Registration successful")

    @expose('/user', methods=["GET"])
    @login_required
    @safe
    def user(self):
        """User endpoint for the API, returns the current user data
         ---
         get:
           description: >-
             Get user data
           responses:
             200:
               description: Authentication Successful
         """
        user_data = self.get_client_user_data(current_user)
        return self.response(200, **user_data)

    @expose('/user', methods=["PUT"])
    @safe
    def update(self):
        """Update user endpoint for the API, updates user data
             ---
             post:
               description: >-
                 Update user information
               requestBody:
                 required: true
                 content:
                   application/json:
                     schema:
                       type: object
                       properties:
                         firstname:
                           description: The username for authentication
                           example: john
                           type: string
                           required: true
                         lastname:
                           description: The password for authentication
                           example: doe
                           type: string
                           required: true
               responses:
                 200:
                   description: Update Successful
                 400:
                   $ref: '#/components/responses/400'
                 401:
                   $ref: '#/components/responses/401'
                 500:
                   $ref: '#/components/responses/500'
             """
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        item = self.appbuilder.sm.get_user_by_id(current_user.id)

        # update user
        item.first_name = firstname
        item.last_name = lastname
        self.appbuilder.sm.update_user(item)

        # get public user data
        user_data = self.get_client_user_data(item)
        return self.response(200, **user_data)

    @expose('/resetpassword', methods=["PUT"])
    @safe
    def reset_password(self):
        """Reset user password endpoint for the API, resets user password
             ---
             post:
               description: >-
                 Reset user password
               requestBody:
                 required: true
                 content:
                   application/json:
                     schema:
                       type: object
                       properties:
                         password:
                           description: The password to rest
                           example: complex-password
                           type: string
                           required: true
               responses:
                 200:
                   description: Update Successful
                 400:
                   $ref: '#/components/responses/400'
                 401:
                   $ref: '#/components/responses/401'
                 500:
                   $ref: '#/components/responses/500'
             """
        password = request.json.get('password', None)
        self.appbuilder.sm.reset_password(current_user.id, password)
        return self.response(200, message="Update successful")

    # testing endpoint (might be useful in general)

    @expose('/authenticate', methods=["GET"])
    @login_required
    @safe
    def authenticate(self):

        user_data = self.get_client_user_data(current_user)
        return self.response(200, **user_data)

    # -------------------------------------------- WIP --------------------------------------------
    # @expose('/signup/email', methods=["POST"])
    # @safe
    # def init_signup(self):
    #     """
    #     This endpoint creates registration request and sends an email to
    #     the user (see flaskappbuilder.security.registerviews) . Make sure the config is
    #     setup properly (see https://flask-appbuilder.readthedocs.io/en/latest/user_registration.html).
    #     Keep in mind, this is only implemented for the auth method "db".
    #    ---
    #    post:
    #      description: >-
    #        Register user and create a session cookie
    #      requestBody:
    #        required: true
    #        content:
    #          application/json:
    #            schema:
    #              type: object
    #              properties:
    #                username:
    #                  description: The username of the new user
    #                  example: user1234
    #                  type: string
    #                  required: true
    #                firstname:
    #                  description: The first name of the new user
    #                  example: John
    #                  type: string
    #                  required: true
    #                lastname:
    #                  description: The last name of the new user
    #                  example: Doe
    #                  type: string
    #                  required: true
    #                email:
    #                  description: The last name of the new user
    #                  example: Doe
    #                  type: string
    #                  required: true
    #                password:
    #                  description: The password for authentication
    #                  example: complex-password
    #                  type: string
    #                  required: true
    #      responses:
    #        200:
    #          description: Authentication Successful
    #        400:
    #          $ref: '#/components/responses/400'
    #        500:
    #          $ref: '#/components/responses/500'
    #     """
    #     username = request.json.get(API_SECURITY_USERNAME_KEY, None)
    #     firstname = request.json.get(API_SECURITY_FIRSTNAME_KEY, None)
    #     lastname = request.json.get(API_SECURITY_LASTNAME_KEY, None)
    #     email = request.json.get(API_SECURITY_EMAIL_KEY, None)
    #     password = request.json.get(API_SECURITY_PASSWORD_KEY, None)
    #
    #     register_user = self.appbuilder.sm.add_register_user(
    #         username, firstname, lastname, email, password
    #     )
    #     if register_user:
    #         if self.send_email(register_user):
    #             return self.response(200, message="A confirmation email was send to you.")
    #         else:
    #             self.appbuilder.sm.del_register_user(register_user)
    #             return self.response_400(message="Not possible to register you at the moment, try again later")
    #
    # def send_email(self, register_user):
    #     """
    #         Method for sending the registration Email to the user
    #     """
    #     try:
    #         from flask_mail import Mail, Message
    #     except Exception:
    #         log.error("Install Flask-Mail to use User registration")
    #         return False
    #     mail = Mail(self.appbuilder.get_app)
    #     msg = Message()
    #     msg.subject = self.email_subject
    #     url = url_for(
    #         ".activation",
    #         _external=True,
    #         activation_hash=register_user.registration_hash,
    #     )
    #     msg.html = self.render_template(
    #         self.email_template,
    #         url=url,
    #         username=register_user.username,
    #         first_name=register_user.first_name,
    #         last_name=register_user.last_name,
    #     )
    #     msg.recipients = [register_user.email]
    #     try:
    #         mail.send(msg)
    #     except Exception as e:
    #         log.error("Send email exception: {0}".format(str(e)))
    #         return False
    #     return True



class PermissionViewApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(PermissionView)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "permissionview"
    base_permissions = ['can_get', 'can_info']



class PermissionsApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(Permission)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "permissions"
    base_permissions = ['can_get', 'can_info']


class RolesApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(Role)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "roles"
    list_columns = ['name', 'permissions']



class UsersApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(User)

    resource_name = "users"
    list_columns = ["first_name", "last_name", "username", "email", "active", "last_login", "login_count", "roles"]
    label_columns = {"username": "Benutzername", "first_name": 'Vorname', "last_name": "Nachname", "email": "Email",
                     "active": 'Aktiv', "login_count": "Anzahl Logins", "roles": "Rollen "}
    show_exclude_columns = ["password", "changed"]
    search_columns = ["username", "first_name", "last_name", "active", "email", "created_by", "changed_by", "roles"]
    edit_columns = ["first_name", "last_name", "username", "email", "active", "roles", "password"]
    add_columns = ["first_name", "last_name", "username", "active", "email", "roles", "password"]

    def put_headless(self, pk: str | int) -> Response:
        if request.json.get('password'):
            request.json['password'] = generate_password_hash(request.json.get('password'))
        return super().put_headless(pk)

    def pre_update(self, item):
        item.changed_on = datetime.datetime.now()
        item.changed_by_fk = g.user.id

    def pre_add(self, item):
        item.password = generate_password_hash(item.password)


class ViewsMenusApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(ViewMenu)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "viewsmenus"
    base_permissions = ['can_get', 'can_info']



def resolver(schema):
    schema_cls = resolve_schema_cls(schema)
    name = schema_cls.__name__
    if name == "MetaSchema":
        if hasattr(schema_cls, "Meta"):
            return (
                f"{schema_cls.Meta.parent_schema_name}.{schema_cls.Meta.model.__name__}"
            )
    if name.endswith("Schema"):
        return name[:-6] or name
    return name


class OpenApi(BaseApi):
    route_base = "/api"
    allow_browser_login = True

    @expose("/<version>/_openapi")
    @safe
    def get(self, version):
        """Endpoint that renders an OpenApi spec for all views that belong
            to a certain version
        ---
        get:
          description: >-
            Get the OpenAPI spec for a specific API version
          parameters:
          - in: path
            schema:
              type: string
            name: version
          responses:
            200:
              description: The OpenAPI spec
              content:
                application/json:
                  schema:
                    type: object
            404:
              $ref: '#/components/responses/404'
            500:
              $ref: '#/components/responses/500'
        """
        version_found = False
        api_spec = self._create_api_spec(version)
        for base_api in current_app.appbuilder.baseviews:
            if isinstance(base_api, BaseApi) and base_api.version == version:
                base_api.add_api_spec(api_spec)
                version_found = True
        if version_found:
            return self.response(200, **api_spec.to_dict())
        else:
            return self.response_404()

    @staticmethod
    def _create_api_spec(version):
        servers = current_app.config.get(
            "FAB_OPENAPI_SERVERS", [{"url": request.host_url}]
        )
        return APISpec(
            title=current_app.appbuilder.app_name,
            version=version,
            openapi_version="3.0.2",
            info=dict(description=current_app.appbuilder.app_name),
            plugins=[MarshmallowPlugin(schema_name_resolver=resolver)],
            servers=servers,
        )