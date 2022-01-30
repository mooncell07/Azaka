__all__ = ("construct_wikidata_link",)


def construct_wikidata_link(identifier: str) -> str:
    """
    Constructs a wikidata link from the given identifier.

    Args:
        identifier: The identifier to construct the wikidata link from.

    Returns:
        The constructed wikidata link.
    """
    if isinstance(identifier, str):
        return f"https://www.wikidata.org/wiki/{identifier}"
    else:
        raise ValueError(
            f"identifier must be of type `str`. Got {type(identifier)} instead."
        )
