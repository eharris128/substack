from typing import Dict, List

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


def get_user_id(username: str) -> int:
    """
    Get the user ID of a Substack user.

    Parameters
    ----------
    username : str
        The username of the Substack user.
    """
    endpoint = f"https://substack.com/api/v1/user/{username}/public_profile"
    r = requests.get(endpoint, headers=HEADERS, timeout=30)
    user_id = r.json()["id"]
    return user_id


def get_user_reads(username: str) -> List[Dict[str, str]]:
    """
    Get newsletters from the "Reads" section of a user's profile.

    Parameters
    ----------
    username : str
        The username of the Substack user.
    """
    endpoint = f"https://substack.com/api/v1/user/{username}/public_profile"
    r = requests.get(endpoint, headers=HEADERS, timeout=30)
    user_data = r.json()
    reads = [
        {
            "publication_id": i["publication"]["id"],
            "publication_name": i["publication"]["name"],
            "subscription_status": i["membership_state"],
        }
        for i in user_data["subscriptions"]
    ]
    return reads


def get_user_likes(user_id: int):
    """
    Get liked posts from a user's profile.

    Parameters
    ----------
    user_id : int
        The user ID of the Substack user.
    """
    endpoint = (
        f"https://substack.com/api/v1/reader/feed/profile/{user_id}?types%5B%5D=like"
    )
    r = requests.get(endpoint, headers=HEADERS, timeout=30)
    likes = r.json()["items"]
    return likes


def get_user_items(user_id: int):
    """
    Get notes and comments posted by a user.

    Parameters
    ----------
    user_id : int
        The user ID of the Substack user.
    """
    endpoint = f"https://substack.com/api/v1/reader/feed/profile/{user_id}"
    r = requests.get(endpoint, headers=HEADERS, timeout=30)
    notes = r.json()["items"]
    return notes

def get_user_notes(user_id: int):
    """
    Get notes posted by a user.

    Parameters
    ----------
    user_id : int
        The user ID of the Substack user.
    """
    endpoint = f"https://substack.com/api/v1/reader/feed/profile/{user_id}"
    r = requests.get(endpoint, headers=HEADERS, timeout=30)
    next_cursor = r.json()["nextCursor"]
    print(f"Next cursor: {next_cursor}")
    notes = r.json()["items"]
    
    # Get notes
    all_reactions = []
    # Get note reaction count
    filtered_notes = [note["comment"]["reaction_count"] for note in notes if note["type"] == "comment"]
    all_reactions.extend(filtered_notes)
    endpoint_with_cursor = f"https://substack.com/api/v1/reader/feed/profile/{user_id}?cursor={next_cursor}"
    next_page_response = requests.get(endpoint_with_cursor, headers=HEADERS, timeout=30)

    # The following cursor
    next_page_response_cursor = next_page_response.json()["nextCursor"]
    next_cursor = r.json()["nextCursor"]
    
    notes = next_page_response.json()["items"]
    filtered_notes = [note["comment"]["reaction_count"] for note in notes if note["type"] == "comment"]
    all_reactions.extend(filtered_notes)

    return all_reactions
