from __future__ import annotations

import typing as t

from .proxy import ConditionProxy
from ..objects import UlistLabels


__all__ = (
    "VNCondition",
    "BaseCondition",
    "ReleaseCondition",
    "ProducerCondition",
    "CharacterCondition",
    "StaffCondition",
    "QuoteCondition",
    "UserCondition",
    "UlistLabelsCondition",
    "UlistCondition",
    "_condition_selector",
)


class Operator:

    """
    An object for storing operators for XCondition attributes to check condition support.

    Warning:
        This object is not meant to be created by users.
    """

    __slots__ = ("symbols",)

    def __init__(self, *symbols: str) -> None:
        """
        Operator constructor.

        Args:
            *symbols (str): The symbols of the operator.

        Attributes:
            symbols (t.Tuple[str]): The symbols of the operator.
        """
        self.symbols = symbols

    @classmethod
    def fill_some(cls, *symbols: str) -> Operator:
        """
        A factory method for creating an Operator object with some symbols.

        Args:
            *symbols (str): The additional symbols of the operator.

        Returns:
            Operator: The created Operator object.

        Info:
            This method fills the `=` and `!=` symbols.
        """
        return cls("=", "!=", *symbols)

    @classmethod
    def fill_all(cls, *symbols: str) -> Operator:
        """
        A factory method for creating an Operator object with all symbols.

        Args:
            *symbols (str): The additional symbols of the operator.

        Returns:
            Operator: The created Operator object.

        Info:
            This method fills the `=`, `!=`, `>`, `<`, `>=`, `<=` symbols.
        """
        return cls("=", "!=", ">", ">=", "<", "<=", *symbols)


class BaseCondition:
    """
    A base class storing the comman condition attributes.

    Tip:
        `ALL` below means all operators (`==`, `!=`, `>`, `<`, `>=`, `<=`) are supported.

        `SOME` means only operators (`==`, `!=`) are supported.

        `SOME + X` means `SOME` and `X` operators are supported.

        For example:

        `|BaseCondition.ID| ALL |` supports (`==`, `!=`, `>`, `<`, `>=`, `<=`) operators.

        `|BaseCondition.ID_ARRAY| SOME |` supports only (`==`, `!=`) operators.

        `|UserCondition.USERNAME| SOME + (%)|` supports (`==`, `!=`, `%`) operators.

        If there is neither `ALL` nor `SOME` in the condition but an operator is specified, then that means
        only that operator is supported.

        I hope you understand the above. :)

    Tip:
        `Field Value Type` means the type of value against which the field should be conditioned.

    Tip:
        All `X_ARRAY` fields must be conditioned against an Iterable of values and
        these fields yield an iterable of objects which match the values from the API.

    | Field    | Field Value Type                  | Operations Supported | Description                    |
    |----------|-----------------------------------|----------------------|--------------------------------|
    | ID       | [int][]                           | ALL                  | Filter using an `ID`           |
    | ID_ARRAY | A [typing.Iterable][] of [int][]s | SOME                 | Filter using an array of `ID`s.|
    """  # noqa: E501

    ID: t.Final[ConditionProxy] = ConditionProxy("id", operator=Operator.fill_all())
    ID_ARRAY: t.Final[ConditionProxy] = ConditionProxy(
        "id", operator=Operator.fill_some()
    )

    __slots__ = ()


class VNCondition(BaseCondition):
    """
    A class storing all the attributes `VN` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute       | Field Value Type                  | Operations Supported | Description                                                                                           |
    |-----------------|-----------------------------------|----------------------|-------------------------------------------------------------------------------------------------------|
    | TITLE           | [str][]                           | *SOME + (%)*         | Filter using the TITLE Field.                                                                         |
    | PLATFORMS       | [None][] or [str][]               | *SOME*               | Filter using the PLATFORMS field.                                                                     |
    | PLATFORMS_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using an array of PLATFORMS.                                                                   |
    | RELEASED        | [None][]                          | *SOME*               | Filter using a `None` value for `RELEASED`.                                                           |
    | RELEASED_DATE   | date                              | *ALL*                | Filter using the release date of the VN.                                                              |
    | LANGUAGES       | [None][] or [str][]               | *SOME*               | Filter using the language, the VN is available in.                                                    |
    | LANGUAGES_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using the array of languages, the VN is available in.                                          |
    | FIRST_CHAR      | [None][] or [str][]               | *SOME*               | Filter using the first character of the VN or None to match all the vn not starting with an alphabet. |
    | ORIG_LANG       | [str][]                           | *SOME*               | Filter using the original language of the VN.                                                         |
    | ORIG_LANG_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using an array of the original languages of the VN.                                            |
    | SEARCH          | [str][]                           | *(%)*                | Search for the VN using it's title and releases.                                                      |
    | TAGS            | [int][]                           | *SOME*               | Find VNs by tag.                                                                                      |
    | TAGS_ARRAY      | A [typing.Iterable][] of [int][]s | *SOME*               | Find VNs using an array of tags.
    """  # noqa: E501

    TITLE: t.Final[ConditionProxy] = ConditionProxy(
        "title", operator=Operator.fill_some("~")
    )

    PLATFORMS: t.Final[ConditionProxy] = ConditionProxy(
        "platforms", operator=Operator.fill_some()
    )
    PLATFORMS_ARRAY: t.Final[ConditionProxy] = PLATFORMS

    RELEASED: t.Final[ConditionProxy] = ConditionProxy(
        "released", operator=Operator.fill_some()
    )
    RELEASED_DATE: t.Final[ConditionProxy] = ConditionProxy(
        "released", operator=Operator.fill_all()
    )

    LANGUAGES: t.Final[ConditionProxy] = ConditionProxy(
        "languages", operator=Operator.fill_some()
    )
    LANGUAGES_ARRAY: t.Final[ConditionProxy] = LANGUAGES

    FIRSTCHAR: t.Final[ConditionProxy] = ConditionProxy(
        "firstchar", operator=Operator.fill_some()
    )

    ORIG_LANG: t.Final[ConditionProxy] = ConditionProxy(
        "orig_lang", operator=Operator.fill_some()
    )
    ORIG_LANG_ARRAY: t.Final[ConditionProxy] = ORIG_LANG

    SEARCH: t.Final[ConditionProxy] = ConditionProxy("search", operator=Operator("~"))

    TAGS: t.Final[ConditionProxy] = ConditionProxy("tags", Operator.fill_some())
    TAGS_ARRAY: t.Final[ConditionProxy] = TAGS

    __slots__ = ()


class ReleaseCondition(BaseCondition):
    """
    A class storing all the attributes `Release` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute       | Field Value Type                  | Operations Supported | Description                                                                                  |
    |-----------------|-----------------------------------|----------------------|----------------------------------------------------------------------------------------------|
    | VN              | [int][]                           | *ALL*                | Find releases linked to the given visual novel ID.                                           |
    | VN_ARRAY        | A [typing.Iterable][] of [int][]s | *SOME*               | Find all the releases linked to the given visual novel IDs in the array.                     |
    | PRODUCER        | [int][]                           | *(==)*               | Find releases linked to the given producer ID.                                               |
    | TITLE           | [str][]                           | *SOME + (%)*         | Find the release using the title.                                                            |
    | ORIGINAL        | [None][] or [str][]               | *SOME + (%)*         | Find the release using the original/official title. (`%` operation not supported for `None`) |
    | RELEASED        | [None][]                          | *SOME*               | Filter using a `None` value for `RELEASED`.                                                  |
    | RELEASED_DATE   | [datetime.date][]                 | *ALL*                | Filter using the release date of the VN.                                                     |
    | PATCH           | [bool][]                          | *(==)*               | Check if the release is a patch.                                                             |
    | FREEWARE        | [bool][]                          | *(==)*               | Check if the release is a freeware.                                                          |
    | DOUJIN          | [bool][]                          | *(==)*               | Check if the release is a doujin.                                                            |
    | TYPE            | [str][]                           | *SOME*               | Filter using the type of release.                                                            |
    | GTIN            | [int][]                           | *SOME*               | Filter using the JAN/UPC/EAN code.                                                           |
    | CATALOG         | [str][]                           | *SOME*               | Filter using the Catalog number.                                                             |
    | LANGUAGES       | [str][]                           | *SOME*               | Filter using the language, the release is available in.                                      |
    | LANGUAGES_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using the array of languages, the release is available in.                            |
    | PLATFORMS       | [str][]                           | *SOME*               | Filter using an array of PLATFORMS.                                                          |
    | PLATFORMS_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using an array of PLATFORMS.                                                          |
    """  # noqa: E501

    VN: t.Final[ConditionProxy] = ConditionProxy("vn", operator=Operator.fill_some())
    VN_ARRAY: t.Final[ConditionProxy] = VN

    PRODUCER: t.Final[ConditionProxy] = ConditionProxy(
        "producer", operator=Operator("=")
    )
    TITLE: t.Final[ConditionProxy] = ConditionProxy(
        "title", operator=Operator.fill_some("~")
    )
    ORIGINAL: t.Final[ConditionProxy] = ConditionProxy(
        "original", operator=Operator.fill_some("~")
    )

    RELEASED: t.Final[ConditionProxy] = ConditionProxy(
        "date", operator=Operator.fill_some()
    )
    RELEASED_DATE: t.Final[ConditionProxy] = ConditionProxy(
        "date", operator=Operator.fill_all()
    )

    PATCH: t.Final[ConditionProxy] = ConditionProxy("patch", operator=Operator("="))
    FREEWARE: t.Final[ConditionProxy] = ConditionProxy(
        "freeware", operator=Operator("=")
    )
    DOUJIN: t.Final[ConditionProxy] = ConditionProxy("doujin", operator=Operator("="))

    TYPE: t.Final[ConditionProxy] = ConditionProxy(
        "type", operator=Operator.fill_some()
    )
    GTIN: t.Final[ConditionProxy] = ConditionProxy(
        "gtin", operator=Operator.fill_some()
    )
    CATALOG: t.Final[ConditionProxy] = ConditionProxy(
        "catalog", operator=Operator.fill_some()
    )

    LANGUAGES: t.Final[ConditionProxy] = ConditionProxy(
        "languages", operator=Operator.fill_some()
    )
    LANGUAGES_ARRAY: t.Final[ConditionProxy] = LANGUAGES

    PLATFORMS: t.Final[ConditionProxy] = ConditionProxy(
        "platforms", operator=Operator.fill_some()
    )
    PLATFORMS_ARRAY: t.Final[ConditionProxy] = PLATFORMS

    __slots__ = ()


class ProducerCondition(BaseCondition):
    """
    A class storing all the attributes `Producer` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute       | Field Value Type                  | Operations Supported | Description                                                                   |
    |-----------------|-----------------------------------|----------------------|-------------------------------------------------------------------------------|
    | NAME            | [str][]                           | *SOME + (%)*         | Find using name of producer.                                                  |
    | ORIGINAL        | [None][] or [str][]               | *SOME + (%)*         | Find using original/official name of the producer. Can't use `%` with `None`. |
    | TYPE            | [str][]                           | *SOME*               | Filter using type of producer.                                                |
    | LANGUAGE        | [str][]                           | *SOME*               | Filter using language of producer.                                            |
    | LANGUAGES_ARRAY | A [typing.Iterable][] of [str][]s | *SOME*               | Filter using an array of languages of producer.                               |
    | SEARCH          | [str][]                           | *(%)*                | Performs a search on the name, original and aliases fields.                   |
    """  # noqa: E501

    NAME: t.Final[ConditionProxy] = ConditionProxy(
        "name", operator=Operator.fill_some("~")
    )
    ORIGINAL: t.Final[ConditionProxy] = ConditionProxy(
        "original", operator=Operator.fill_some("~")
    )
    TYPE: t.Final[ConditionProxy] = ConditionProxy(
        "type", operator=Operator.fill_some()
    )

    LANGUAGE: t.Final[ConditionProxy] = ConditionProxy(
        "language", operator=Operator.fill_some()
    )
    LANGUAGES_ARRAY: t.Final[ConditionProxy] = LANGUAGE

    SEARCH: t.Final[ConditionProxy] = ConditionProxy("search", operator=Operator("~"))

    __slots__ = ()


class CharacterCondition(BaseCondition):
    """
    A class storing all the attributes `Character` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute    | Field Value Type                  | Operations Supported | Description                                                                                                                                                              |
    |--------------|-----------------------------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | NAME         | [str]                             | *SOME + (%)*         | Find using name of character.                                                                                                                                            |
    | ORIGINAL     | [None][] or [str][]               | *SOME + (%)*         | Find using original/official name of the character. Can't use `%` with `None`.                                                                                           |
    | SEARCH       | [str][]                           | *(%)*                | Performs a search on the name, original and aliases fields.                                                                                                              |
    | VN           | [int][]                           | *(==)*               | Find characters linked to the given visual novel ID.                                                                                                                     |
    | VN_ARRAY     | A [typing.Iterable][] of [int][]s | *(==)*               | Find characters linked to the given visual novel ID array.                                                                                                               |
    | TRAITS       | [int][]                           | *SOME*               | Find characters by trait.                                                                                                                                                |
    | TRAITS_ARRAY | A [typing.Iterable][] of [int][]s | *SOME*               | The `=` filter will return chars that are linked to any (not all) of the given traits, the `!=` filter will return chars that are not linked to any of the given traits. |
    """  # noqa: E501

    NAME: t.Final[ConditionProxy] = ConditionProxy(
        "name", operator=Operator.fill_some("~")
    )
    ORIGINAL: t.Final[ConditionProxy] = ConditionProxy(
        "original", operator=Operator.fill_some("~")
    )
    SEARCH: t.Final[ConditionProxy] = ConditionProxy("search", operator=Operator("~"))

    VN: t.Final[ConditionProxy] = ConditionProxy("vn", operator=Operator("="))
    VN_ARRAY: t.Final[ConditionProxy] = VN

    TRAITS: t.Final[ConditionProxy] = ConditionProxy(
        "traits", operator=Operator.fill_some()
    )
    TRAITS_ARRAY: t.Final[ConditionProxy] = TRAITS

    __slots__ = ()


class StaffCondition(BaseCondition):
    """
    A class storing all the attributes `Staff` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute | Field Value Type                  | Operations Supported | Description                                                 |
    |-----------|-----------------------------------|----------------------|-------------------------------------------------------------|
    | AID       | [int][]                           | *(==)*               | Find staff by alias ID.                                     |
    | AID_ARRAY | A [typing.Iterable][] of [int][]s | *(==)*               | Find staff by an array of alias IDs.                        |
    | SEARCH    | [str][]                           | *(%)*                | Performs a search on the name, original and aliases fields. |
    """  # noqa: E501

    AID: t.Final[ConditionProxy] = ConditionProxy("aid", operator=Operator("="))
    AID_ARRAY: t.Final[ConditionProxy] = AID

    SEARCH: t.Final[ConditionProxy] = ConditionProxy("search", operator=Operator("~"))

    __slots__ = ()


class QuoteCondition(BaseCondition):
    """
    A class storing all the attributes `Staff` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    Info:
        This one only supports `ID` and `ID_ARRAY` filters of `BaseCondition`.
    """  # noqa: E501

    __slots__ = ()


class UserCondition(BaseCondition):
    """
    A class storing all the attributes `User` type supports as condition.

    Hint:
        Check the `BaseCondition` class for more information.

    | Attribute      | Field Value Type                  | Operations Supported | Description                            |
    |----------------|-----------------------------------|----------------------|----------------------------------------|
    | USERNAME       | [str][]                           | *SOME + (%)*         | Find user by their username.           |
    | USERNAME_ARRAY | A [typing.Iterable][] of [str][]s | *(==)*               | Find user using an array of usernames. |

    """  # noqa: E501

    USERNAME: t.Final[ConditionProxy] = ConditionProxy(
        "username", operator=Operator.fill_some("~")
    )
    USERNAME_ARRAY: t.Final[ConditionProxy] = ConditionProxy(
        "username", operator=Operator("=")
    )

    __slots__ = ()


class UlistLabelsCondition:
    """
    A class storing all the attributes `UlistLabels` type supports as condition.

    Info:
        This class doesn't inherit from `BaseCondition` and doesn't have `ID` and `ID_ARRAY` filters.

    | Attribute | Field Value Type | Operations Supported | Description                                                                              |
    |-----------|------------------|----------------------|------------------------------------------------------------------------------------------|
    | UID       | [int][]          | *(==)*               | Find using user ID. The special value '0' is recognized as the currently logged in user. |
    """  # noqa: E501

    UID: t.Final[ConditionProxy] = ConditionProxy("uid", operator=Operator("="))


class UlistCondition(UlistLabelsCondition):
    """
    A class storing all the attributes `Ulist` type supports as condition.

    Hint:
        Check the `UlistLabelsCondition` class for more information.

    | Attribute | Field Value Type                  | Operations Supported | Description                              |
    |-----------|-----------------------------------|----------------------|------------------------------------------|
    | VN        | [int][]                           | *ALL*                | Find by visual novel ID.                 |
    | VN_ARRAY  | A [typing.Iterable][] of [int][]s | *SOME*               | Find using an array of visual novel IDs. |
    | LABEL     | [int][]                           | *(==)*               | Label assigned to the VN.                |
    """  # noqa: E501

    VN: t.Final[ConditionProxy] = ConditionProxy("vn", operator=Operator.fill_all())
    VN_ARRAY: t.Final[ConditionProxy] = ConditionProxy(
        "vn", operator=Operator.fill_some()
    )
    LABEL: t.Final[ConditionProxy] = ConditionProxy("label", operator=Operator("~"))

    __slots__ = ()


def _condition_selector(
    type: t.Any,
) -> t.Any:
    condition_map = {
        "vn": VNCondition,
        "release": ReleaseCondition,
        "producer": ProducerCondition,
        "character": CharacterCondition,
        "staff": StaffCondition,
        "quote": QuoteCondition,
        "user": UserCondition,
        "ulist-labels": UlistLabelsCondition,
        "ulist": UlistCondition,
    }
    return condition_map[
        type.__name__.lower() if type != UlistLabels else "ulist-labels"
    ]
