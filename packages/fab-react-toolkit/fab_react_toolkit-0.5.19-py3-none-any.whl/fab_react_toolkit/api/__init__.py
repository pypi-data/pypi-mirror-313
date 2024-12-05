import functools
from inspect import isfunction
import json
import urllib
from typing import Any, Callable, Optional, Dict
import jsonschema
import prison as prison
from flask_appbuilder.api import BaseApi, ModelRestApi as FABModelRestApi, merge_response_func, expose, safe, rison, get_info_schema, get_item_schema
from flask_appbuilder._compat import as_unicode
from .utils import generate_report

from flask_appbuilder.const import (
    API_ADD_COLUMNS_RES_KEY,
    API_ADD_COLUMNS_RIS_KEY,
    API_ADD_TITLE_RES_KEY,
    API_ADD_TITLE_RIS_KEY,
    API_DESCRIPTION_COLUMNS_RES_KEY,
    API_DESCRIPTION_COLUMNS_RIS_KEY,
    API_EDIT_COLUMNS_RES_KEY,
    API_EDIT_COLUMNS_RIS_KEY,
    API_EDIT_TITLE_RES_KEY,
    API_EDIT_TITLE_RIS_KEY,
    API_FILTERS_RES_KEY,
    API_FILTERS_RIS_KEY,
    API_LABEL_COLUMNS_RES_KEY,
    API_LABEL_COLUMNS_RIS_KEY,
    API_LIST_COLUMNS_RES_KEY,
    API_LIST_COLUMNS_RIS_KEY,
    API_LIST_TITLE_RES_KEY,
    API_LIST_TITLE_RIS_KEY,
    API_ORDER_COLUMN_RIS_KEY,
    API_ORDER_COLUMNS_RES_KEY,
    API_ORDER_COLUMNS_RIS_KEY,
    API_ORDER_DIRECTION_RIS_KEY,
    API_PAGE_INDEX_RIS_KEY,
    API_PAGE_SIZE_RIS_KEY,
    API_PERMISSIONS_RES_KEY,
    API_PERMISSIONS_RIS_KEY,
    API_RESULT_RES_KEY,
    API_SELECT_COLUMNS_RIS_KEY,
    API_SHOW_COLUMNS_RES_KEY,
    API_SHOW_COLUMNS_RIS_KEY,
    API_SHOW_TITLE_RES_KEY,
    API_SHOW_TITLE_RIS_KEY,
    API_URI_RIS_KEY,
    PERMISSION_PREFIX,
)

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TYPE_CHECKING,
    Union,
)

from flask_appbuilder.security.decorators import permission_name, protect
from flask import Response, request
from flask_appbuilder.const import API_ADD_COLUMNS_RIS_KEY, API_ADD_TITLE_RIS_KEY, API_PERMISSIONS_RIS_KEY, \
    API_EDIT_COLUMNS_RIS_KEY, API_FILTERS_RIS_KEY, API_EDIT_TITLE_RIS_KEY, API_FILTERS_RES_KEY, \
    API_ORDER_COLUMNS_RIS_KEY, API_LABEL_COLUMNS_RIS_KEY, API_DESCRIPTION_COLUMNS_RIS_KEY, API_LIST_COLUMNS_RIS_KEY, \
    API_LIST_TITLE_RIS_KEY, API_URI_RIS_KEY
from flask_appbuilder.api.schemas import get_list_schema
from .convert import Model2SchemaConverter

from copy import deepcopy

ModelKeyType = Union[str, int]


def better_rison(
        schema: Optional[Dict[str, Any]] = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Use this decorator to parse URI *Rison* arguments to
    a python data structure, your method gets the data
    structure on kwargs['rison']. Response is HTTP 400
    if *Rison* is not correct::

        class ExampleApi(BaseApi):
                @expose('/risonjson')
                @rison()
                def rison_json(self, **kwargs):
                    return self.response(200, result=kwargs['rison'])

    You can additionally pass a JSON schema to
    validate Rison arguments::

        schema = {
            "type": "object",
            "properties": {
                "arg1": {
                    "type": "integer"
                }
            }
        }

        class ExampleApi(BaseApi):
                @expose('/risonjson')
                @rison(schema)
                def rison_json(self, **kwargs):
                    return self.response(200, result=kwargs['rison'])

    """

    def _rison(f: Callable[..., Any]) -> Callable[..., Any]:
        def wraps(self: "BaseApi", *args: Any, **kwargs: Any) -> Response:
            value = request.args.get(API_URI_RIS_KEY, None)
            kwargs["rison"] = dict()
            if value:
                try:
                    kwargs["rison"] = prison.loads(value)
                except prison.decoder.ParserException:
                    try:
                        kwargs["rison"] = json.loads(value)
                    except Exception:
                        return self.response_400(
                            message="Not a valid rison/json argument"
                        )
            if schema:
                try:
                    jsonschema.validate(
                        instance=kwargs["rison"], schema=schema)
                except jsonschema.ValidationError as e:
                    return self.response_400(message=f"Not a valid rison schema {e}")
            return f(self, *args, **kwargs)

        return functools.update_wrapper(wraps, f)

    return _rison


class ModelRestApi(FABModelRestApi):
    allow_browser_login = True
    quick_filters = None
    filter_options = None
    search_model_schema = None
    search_query_rel_fields = None
    icon = "Table"
    related_apis = []

    """
        List with ModelRestApi classes
        Will add related_apis information to the info endpoint

            class MyApi(ModelRestApi):
                datamodel = SQLAModel(Group, db.session)
                related_apis = [MyOtherApi]

    """

    model2schemaconverter = Model2SchemaConverter

    def __init__(self):
        super().__init__()
        name = self.resource_name or self.__class__.__name__.lower()
        self.list_title = name.capitalize()
        self.quick_filters = self.quick_filters or []
        self.filter_options = self.filter_options or {}
        self.search_model_schema_name = f"{self.__class__.__name__}.search"

        self.search_query_rel_fields = self.search_query_rel_fields or dict()

        if self.search_model_schema is None:
            self.search_model_schema = self.model2schemaconverter.convert(
                self.search_columns,
                nested=False,
                parent_schema_name=self.search_model_schema_name,
            )

        self._add_relation_column_order()
        self._add_function_list_columns()

    def merge_relations_info(self, response, **kwargs):
        """
        Adds relationship information to the response
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """
        relations = []
        for related_api in self.related_apis:
            foreign_key = related_api.datamodel.get_related_fk(
                self.datamodel.obj)
            relation_type = "rel_o_m" if related_api.datamodel.is_relation_many_to_one(
                foreign_key) else "rel_m_m"
            relation = {
                'name': related_api.list_title if related_api.list_title else self._prettify_name(
                    related_api.datamodel.model_name),
                'foreign_key': foreign_key,
                'type': relation_type,
                "path": related_api.resource_name + '/' or type(related_api).__name__ + '/'}

            relations.append(relation)

        response["relations"] = relations

    def merge_search_filters(self, response, **kwargs):
        """
        Overrides parent method to add the schema of a filter to the response. Selection is based on show columns.
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """

        # Get possible search fields and all possible operations
        search_filters = dict()
        dict_filters = self._filters.get_search_filters()

        # TODO: this is bugged - since there is no schema for search_columns, search_colums must be a subset of show_columns
        for col in self.search_columns:
            search_filters[col] = {'label': self.label_columns[col], 'filters': [
                {"name": as_unicode(flt.name), "operator": flt.arg_name,
                 }
                for flt in dict_filters[col]
            ]}
            # Add schema info
            search_filters[col]['schema'] = self._get_field_info(self.search_model_schema.fields[col],
                                                                 self.search_query_rel_fields.get(col, []))
        response[API_FILTERS_RES_KEY] = search_filters

    def merge_filter_options(self, response, **kwargs):
        """
        Overrides parent method to add the schema of a filter to the response. Selection is based on show columns.
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """

        # Get possible search fields and all possible operations
        filter_options = deepcopy(self.filter_options)
        for k, v in filter_options.items() or {}.items():
            if callable(v):
                filter_options[k] = v()

        response["filter_options"] = filter_options

    @expose("/_info", methods=["GET"])
    @protect()
    @safe
    @rison(get_info_schema)
    @permission_name("info")
    @merge_response_func(
        BaseApi.merge_current_user_permissions, API_PERMISSIONS_RIS_KEY
    )
    @merge_response_func(FABModelRestApi.merge_add_field_info, API_ADD_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_edit_field_info, API_EDIT_COLUMNS_RIS_KEY)
    @merge_response_func(merge_search_filters, API_FILTERS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_add_title, API_ADD_TITLE_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_edit_title, API_EDIT_TITLE_RIS_KEY)
    @merge_response_func(merge_relations_info, "relations")
    @merge_response_func(merge_filter_options, "filter_options")
    def info(self, **kwargs):
        """ Endpoint that renders a response for CRUD REST meta data
        ---
        get:
          description: >-
            Get metadata information about this API resource
          parameters:
          - in: query
            name: q
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/get_info_schema'
          responses:
            200:
              description: Item from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      add_columns:
                        type: object
                      edit_columns:
                        type: object
                      filters:
                        type: object
                        properties:
                          column_name:
                            type: array
                            items:
                              type: object
                              properties:
                                name:
                                  description: >-
                                    The filter name. Will be translated by babel
                                  type: string
                                operator:
                                  description: >-
                                    The filter operation key to use on list filters
                                  type: string
                      permissions:
                        description: The user permissions for this API resource
                        type: array
                        items:
                          type: string
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        return self.info_headless(**kwargs)

    @expose("/", methods=["GET"])
    @protect()
    @safe
    @permission_name("get")
    @better_rison(get_list_schema)
    @merge_response_func(FABModelRestApi.merge_order_columns, API_ORDER_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_list_label_columns, API_LABEL_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_description_columns, API_DESCRIPTION_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_list_columns, API_LIST_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_list_title, API_LIST_TITLE_RIS_KEY)
    def get_list(self, **kwargs: Any) -> Response:
        """Get list of items from Model
        ---
        get:
          description: >-
            Get a list of models
          parameters:
          - in: query
            name: q
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/get_list_schema'
          responses:
            200:
              description: Items from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      label_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The label for the column name.
                              Will be translated by babel
                            example: A Nice label for the column
                            type: string
                      list_columns:
                        description: >-
                          A list of columns
                        type: array
                        items:
                          type: string
                      description_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The description for the column name.
                              Will be translated by babel
                            example: A Nice description for the column
                            type: string
                      list_title:
                        description: >-
                          A title to render.
                          Will be translated by babel
                        example: List Items
                        type: string
                      ids:
                        description: >-
                          A list of item ids, useful when you don't know the column id
                        type: array
                        items:
                          type: string
                      count:
                        description: >-
                          The total record count on the backend
                        type: number
                      order_columns:
                        description: >-
                          A list of allowed columns to sort
                        type: array
                        items:
                          type: string
                      result:
                        description: >-
                          The result from the get list query
                        type: array
                        items:
                          $ref: '#/components/schemas/{{self.__class__.__name__}}.get_list'  # noqa
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """

        return self.get_list_headless(**kwargs)

    @expose('/bulk/<string:handler>', methods=['POST'])
    @protect()
    @safe
    @permission_name('bulk')
    def post_bulk(self, handler, **kwargs: any) -> Response:
        """
        Perform a bulk operation for the specified handler.

        Args:
            handler: The name of the handler to perform the bulk operation on.
            **kwargs: Additional keyword arguments.

        Returns:
            The response from the bulk operation.

        """
        id_list = request.get_json()
        bulk_func = getattr(self, f"bulk_{handler}")
        return bulk_func(id_list)

    @expose("/download", methods=["POST"])
    @protect(allow_browser_login=True)
    @safe
    @permission_name('download')
    def download(self):
        query_params = request.json.get("queryParams", "")

        query = self.datamodel.session.query(self.datamodel.obj)

        self._filters.clear_filters()

        self._filters.rest_add_filters(query_params['filters'])
        filters = self._filters.get_joined_filters(self._base_filters)

        inner_filters = self.datamodel.get_inner_filters(filters)
        query = self.datamodel.apply_filters(query, inner_filters)
        result = query.yield_per(100)

        response = Response(generate_report(
            result, self.list_columns, self.label_columns), mimetype='text/csv')
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename={name}.csv'.format(
            name='appbybu')
        return response

    @expose("/<pk>", methods=["GET"])
    @protect()
    @safe
    @permission_name("get")
    @rison(get_item_schema)
    @merge_response_func(FABModelRestApi.merge_show_label_columns, API_LABEL_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_show_columns, API_SHOW_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_description_columns, API_DESCRIPTION_COLUMNS_RIS_KEY)
    @merge_response_func(FABModelRestApi.merge_show_title, API_SHOW_TITLE_RIS_KEY)
    def get(self, pk: ModelKeyType, **kwargs: Any) -> Response:
        """Get item from Model
        ---
        get:
          description: >-
            Get an item model
          parameters:
          - in: path
            schema:              
              oneOf:
              - type: string
              - type: integer
            name: pk
          - in: query
            name: q
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/get_item_schema'
          responses:
            200:
              description: Item from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      label_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The label for the column name.
                              Will be translated by babel
                            example: A Nice label for the column
                            type: string
                      show_columns:
                        description: >-
                          A list of columns
                        type: array
                        items:
                          type: string
                      description_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The description for the column name.
                              Will be translated by babel
                            example: A Nice description for the column
                            type: string
                      show_title:
                        description: >-
                          A title to render.
                          Will be translated by babel
                        example: Show Item Details
                        type: string
                      id:
                        description: The item id
                        type: string
                      result:
                        $ref: '#/components/schemas/{{self.__class__.__name__}}.get'
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            404:
              $ref: '#/components/responses/404'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        return self.get_headless(pk, **kwargs)

    @expose("/<pk>", methods=["PUT"])
    @protect()
    @safe
    @permission_name("put")
    def put(self, pk: ModelKeyType) -> Response:
        """PUT item to Model
        ---
        put:
          parameters:
          - in: path
            schema:
              oneOf:
              - type: string
              - type: integer
            name: pk
          requestBody:
            description: Model schema
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/{{self.__class__.__name__}}.put'
          responses:
            200:
              description: Item changed
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      result:
                        $ref: '#/components/schemas/{{self.__class__.__name__}}.put'
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            404:
              $ref: '#/components/responses/404'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        return self.put_headless(pk)

    @expose("/<pk>", methods=["DELETE"])
    @protect()
    @safe
    @permission_name("delete")
    def delete(self, pk: ModelKeyType) -> Response:
        """Delete item from Model
        ---
        delete:
          parameters:
          - in: path
            schema:
              oneOf:
              - type: string
              - type: integer
            name: pk
          responses:
            200:
              description: Item deleted
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
            404:
              $ref: '#/components/responses/404'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        return self.delete_headless(pk)

    def _add_relation_column_order(self, force=False) -> None:
        """
        Adds relation columns to the order_columns list if the order_columns list is the same as the default order_columns list.

        Args:
            force (bool, optional): If set to True, the relation columns will be added to the order_columns list regardless of the default order_columns list. Defaults to False.

        Returns:
            None
        """
        default_order_columns = self.datamodel.get_order_columns_list(
            list_columns=self.list_columns)
        set_default_order_columns = set(default_order_columns)
        set_order_columns = set(self.order_columns)
        if not set_default_order_columns == set_order_columns and not force:
            return

        order_relation_columns = [
            f"{column}.id" for column in self.list_columns if self.datamodel.is_relation(column) and (self.datamodel.is_relation_many_to_one(column) or self.datamodel.is_relation_one_to_one(column))]
        self.order_columns = self.order_columns + order_relation_columns

    def _add_function_list_columns(self, force=False) -> None:
        """
        Adds function columns to the list_columns list if the list_columns list is the same as the default list_columns list.

        Args:
            force (bool, optional): If set to True, the function columns will be added to the list_columns list regardless of the default list_columns list. Defaults to False.

        Returns:
            None
        """
        default_columns = [x for x in self.datamodel.get_user_columns_list() if x not in self.list_exclude_columns
                           ]
        set_default_columns = set(default_columns)
        set_list_columns = set(self.list_columns)
        if not set_default_columns == set_list_columns and not force:
            return

        attrs = vars(self.datamodel.obj)
        model_properties = [key for key, value in attrs.items(
        ) if not key.startswith("_") and isfunction(value) and key not in self.list_exclude_columns]
        model_labels = {key: ' '.join([word.capitalize() for word in key.split('_')])for key in model_properties}
        self.label_columns = {**self.label_columns, **model_labels}
        self.list_columns = self.list_columns + model_properties