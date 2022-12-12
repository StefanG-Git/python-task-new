from typing import List, Any


def get_color_code_by_number(number: int) -> str:
    """
    Gets the color code depending on the given number.

    Parameters
    ----------
    number: int
        Comparison number.

    Returns
    -------
    Color code: str
        The code of color
    """
    if number <= 3:
        return "007500"
    elif number <= 12:
        return "FFA500"

    return "b30000"


def add_unique_items_to_list(unique_list: List[Any], *items: Any) -> List[Any]:
    """
    Adds items to list if they are not in the list

    Parameters
    ----------
    unique_list : List[Any]
        List with unique items.
    items : Tuple[Any]
        Items to add.

    Returns
    -------
    unique_list : List[Any]
        List + new unique items.
    """
    for item in items:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list
