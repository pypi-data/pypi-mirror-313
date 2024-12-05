from flask_appbuilder.models.generic.filters import \
    FilterContains as FABGenericFilterContains
from flask_appbuilder.models.generic.filters import \
    FilterEqual as FABGenericFilterEqual
from flask_appbuilder.models.generic.filters import \
    FilterGreater as FABGenericFilterGreater
from flask_appbuilder.models.generic.filters import \
    FilterIContains as FABGenericFilterIContains
from flask_appbuilder.models.generic.filters import \
    FilterNotContains as FABGenericFilterNotContains
from flask_appbuilder.models.generic.filters import \
    FilterNotEqual as FABGenericFilterNotEqual
from flask_appbuilder.models.generic.filters import \
    FilterSmaller as FABGenericFilterSmaller
from flask_appbuilder.models.generic.filters import \
    FilterStartsWith as FABGenericFilterStartsWith
from flask_appbuilder.models.generic.filters import \
    GenericFilterConverter as FABGenericFilterConverter


class GenericFilterEqual(FABGenericFilterEqual):
    arg_name = "generic_eq"


class GenericFilterNotEqual(FABGenericFilterNotEqual):
    arg_name = "generic_ne"


class GenericFilterEqualBoolean(GenericFilterEqual):

    def apply(self, query, value):
        if value == 1 or value == "1":
            value = True
        else:
            value = False
        return super().apply(query, value)


class GenericFilterNotEqualBoolean(GenericFilterNotEqual):

    def apply(self, query, value):
        if value == 1 or value == "1":
            value = True
        else:
            value = False
        return super().apply(query, value)


class GenericFilterContains(FABGenericFilterContains):
    arg_name = "generic_ct"


class GenericFilterIContains(FABGenericFilterIContains):
    arg_name = "generic_ict"


class GenericFilterNotContains(FABGenericFilterNotContains):
    arg_name = "generic_nct"


class GenericFilterStartsWith(FABGenericFilterStartsWith):
    arg_name = "generic_sw"


class GenericFilterGreater(FABGenericFilterGreater):
    arg_name = "generic_gt"


class GenericFilterSmaller(FABGenericFilterSmaller):
    arg_name = "generic_lt"


class GenericFilterConverter(FABGenericFilterConverter):

    conversion_table = (
        ("is_enum", [GenericFilterEqual, GenericFilterNotEqual]),
        ("is_boolean", [GenericFilterEqualBoolean,
         GenericFilterNotEqualBoolean]),
        (
            "is_text",
            [
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterStartsWith,
            ],
        ),
        (
            "is_string",
            [
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterStartsWith,
            ],
        ),
        ("is_integer", [GenericFilterEqual, GenericFilterNotEqual,
         GenericFilterGreater, GenericFilterSmaller]),
        ("is_date", [GenericFilterEqual, GenericFilterNotEqual,
         GenericFilterGreater, GenericFilterSmaller]),
    )
