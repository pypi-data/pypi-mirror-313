"""
Tools to fetch and parses flashcards from a Quizlet set (from ID).
"""

import json
from .curl import curl_api


def get_flashcards_from_id(id: int | str):
    """
    Fetches flashcards from a Quizlet set by ID.

    Args:
        id (int | str): The ID of the Quizlet set to fetch.

    Returns:
        list: A list of flashcards from the set.
    """

    endpoint = f"https://quizlet.com/webapi/3.4/studiable-item-documents?filters%5BstudiableContainerId%5D={id}&filters%5BstudiableContainerType%5D=1&perPage=1000&page=1"
    raw = curl_api(endpoint)

    if raw:
        try:
            json_data = json.loads(raw)

            items = json_data["responses"][0]["models"]["studiableItem"]

            cards = [
                {
                    "front": item["cardSides"][1]["media"][0]["plainText"],
                    "back": item["cardSides"][0]["media"][0]["plainText"],
                }
                for item in items
            ]

            return cards

        except Exception as e:
            # print(e)
            return (
                "Please go to \n"
                + f"https://quizlet.com/webapi/3.4/studiable-item-documents?filters%5BstudiableContainerId%5D={id}&filters%5BstudiableContainerType%5D=1&perPage=1000&page=1"
                + "\n and check if the set is accessable."
            )
    else:
        return (
            "Please go to \n"
            + f"https://quizlet.com/webapi/3.4/studiable-item-documents?filters%5BstudiableContainerId%5D={id}&filters%5BstudiableContainerType%5D=1&perPage=1000&page=1"
            + "\n and check if the set is accessable."
        )
