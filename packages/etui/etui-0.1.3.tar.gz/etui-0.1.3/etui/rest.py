import requests
import itertools

from .data import is_json


def get_nested_paging(paging_r: dict, next_param: list) -> str:
    """Get nested paging URL

    Args:
        paging_r (dict): Response containing paging
        next_param (list): List of (nested) paging param(s)

    Returns:
        str: Paging URL
    """
    if not next_param:
        return ""

    while next_param:
        if next_param[0] not in paging_r.keys():
            return ""

        for np, pp in itertools.product(next_param, paging_r):
            if np == pp:
                if len(next_param) <= 1:
                    return paging_r[np]

                next_param.pop(next_param.index(np))
                paging_r = paging_r[np]


def paginator(r: requests, data_param: str, next_param: list) -> list:
    """Query all API paginations and return complete list

    Args:
        r (requests): requests-object
        data_param (str): Param containing data
        next_param (list): List of (nested) paging param(s)

    Returns:
        list: Return complete list
    """

    if not is_json(r.text):
        return []
    if data_param not in r.text:
        raise KeyError(f"{data_param} not in response. ")

    complete_data = r.json()[data_param]

    while next_url := get_nested_paging(r.json(), next_param[:]):
        r = requests.get(next_url)

        if data_param in r.text:
            if not r.json()[data_param]:
                break
            complete_data.extend(r.json()[data_param])

    return complete_data


if __name__ == "__main__":
    url = ""
    r = requests.get(url)
    data = paginator(r, "data", ["paging", "next"])

    print(len(data))
