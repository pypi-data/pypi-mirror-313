from typing import TypedDict, Optional, Annotated, Union, Dict

def replace_reducer(state, new_state):
    return new_state

def dict_reducer(a, b):
    result = a.copy()
    result.update(b)
    return result

def list_reducer(a: Optional[list], b: Optional[list]):
    if (a is None):
        return b
    # Create a set to track unique objects based on their string representation
    unique_items = {str(item): item for item in a}  # Add items from list a
    unique_items.update({str(item): item for item in b})  # Add items from list b
    result = list(unique_items.values())
    return result

class Error(TypedDict):
    message: Annotated[str, replace_reducer]

class AirtopBaseState(TypedDict):
    url: Annotated[str, replace_reducer] # Input: The url of the page to prompt or scrape
    output_schema: Annotated[Optional[Union[str, Dict]], replace_reducer] # Input: The output schema to use for the prompt
    session_id: Annotated[Optional[str], replace_reducer] # Output: The session id used on the graph flow
    window_id: Annotated[Optional[str], replace_reducer] # Output: The window id used on the graph flow
    profile_id: Annotated[Optional[str], replace_reducer] # Output: The profile id used on the graph flow
    live_view_url: Annotated[Optional[str], replace_reducer] # Output: The url of the live view used on the graph flow
    response: Annotated[Optional[any], replace_reducer] # Output: The response from the prompt or scrape
    response_errors: Annotated[Optional[list[Error]], list_reducer] # Output: The errors from the prompt or scrape
    response_meta: Annotated[Optional[any], replace_reducer] # Output: The metadata from the prompt or scrape

# Configurable parameters
# This is for reference only as the config is passed in through the RunnableConfig
# Pass into remote graph as `config={'configurable': <AIRTOP_CONFIGURABLE>}`
class AirtopConfigurable(TypedDict):
    api_key: str # The api key to use for the graph flow
    session_id: Annotated[Optional[str], dict_reducer] # The existing session id to use, otherwise a new session will be created
    window_id: Annotated[Optional[str], dict_reducer] # The existing window id to use, otherwise a new window will be created
    keep_session_alive: bool # Do not terminate the session after the graph flow completes
    base_profile_id: str # The base profile id to use for the graph flow
    persist_profile: bool # Persist the profile after the graph flow completes
    follow_pagination_links: bool # Follow pagination links when scraping