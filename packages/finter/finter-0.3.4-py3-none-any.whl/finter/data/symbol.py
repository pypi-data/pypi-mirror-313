from finter.api import SymbolApi
from finter.settings import get_api_client
from finter.api import MapperApi
import json
import pandas as pd


class Symbol:
    """
    A class to handle the conversion of financial symbols between different identifiers based on API responses.

    This class provides a method to convert financial symbol identifiers from one format to another using the SymbolApi.

    Methods:
        convert(_from: str, to: str, source: Union[str, list], date: Optional[str] = None, universe: Optional[int] = None) -> Optional[dict]:
            Converts financial symbols from one identifier format to another and handles potential errors during API calls.

    Attributes:
        _from (str): The source identifier type (e.g., 'id').
        to (str): The target identifier type (e.g., 'entity_name').
        source (Union[str, list]): The actual identifier(s) to be converted. Can be a single identifier or a list of identifiers.
        date (Optional[str]): The date for which the conversion is applicable (default is None, implying the current date).
        universe (Optional[int]): An optional parameter to specify the universe of the identifiers (default is None).
    """

    @classmethod
    def convert(cls, _from, to, source, date=None, universe=None):
        """
        Converts identifiers from one type to another using the SymbolApi service.

        Args:
            _from (str): The type of the source identifier.
            to (str): The type of the target identifier.
            source (Union[str, list]): The identifier or list of identifiers to convert.
            date (Optional[str]): The date for which the identifier conversion is relevant (not used in current implementation).
            universe (Optional[int]): The universe context for the conversion (not used in current implementation).

        Returns:
            Optional[dict]: A dictionary mapping the source identifiers to the converted identifiers, or None if the API call fails.

        Raises:
            Exception: Captures any exceptions raised during the API call, logs the error, and returns None.
        """
        if isinstance(source, pd.Index):
            source = source.to_list()
        if isinstance(
            source, list
        ):  # Check if the source is a list and convert it to a comma-separated string if true.
            source = ",".join(map(str, source))
        try:
            api_response = SymbolApi(get_api_client()).id_convert_create(
                _from=_from, to=to, source=source
            )
            result = api_response.code_mapped
            if _from == "id":
                result = {int(k): v for k, v in result.items()}
            if _from == "short_code":
                result = {k: v[0] if len(v) == 1 else v for k, v in result.items()}
            return result  # Return the mapping from the API response.
        except Exception as e:
            if hasattr(e, "body"):
                try:
                    error_json = json.loads(e.body)
                    message = error_json.get("message", "Unknown error occurred")
                except (ValueError, AttributeError):
                    message = str(e)
            else:
                message = str(e)
            print(f"Symbol API call failed: {message}")
            return None


class Mapper:
    """
    A class to handle the conversion of financial symbols using different MapperApi functions.

    This class provides methods to retrieve mappers for converting financial symbol identifiers between different formats using MapperApi.

    Methods:
        get_ccid_to_short_code_mapper() -> Optional[dict]:
            Retrieves the CCID to short code mapper.
        get_entity_id_to_ccid_mapper() -> Optional[dict]:
            Retrieves the entity ID to CCID mapper.
    """

    @classmethod
    def get_ccid_to_short_code_mapper(cls):
        """
        Retrieves the CCID to short code mapper using the MapperApi service.

        Args:
            None

        Returns:
            Optional[dict]: A dictionary containing the CCID to short code mappings, or None if the API call fails.

        Raises:
            Exception: Captures any exceptions raised during the API call, logs the error, and returns None.
        """
        try:
            api_response = MapperApi(
                get_api_client()
            ).mapper_ccid_to_short_code_retrieve()
            return api_response.mapper  # Return the mapping from the API response.
        except Exception as e:
            print(
                f"Mapper API call failed: {e}"
            )  # Log any exceptions encountered during the API call.
            return None

    @classmethod
    def get_entity_id_to_ccid_mapper(cls):
        """
        Retrieves the entity ID to CCID mapper using the MapperApi service.

        Args:
            None

        Returns:
            Optional[dict]: A dictionary containing the entity ID to CCID mappings, or None if the API call fails.

        Raises:
            Exception: Captures any exceptions raised during the API call, logs the error, and returns None.
        """
        try:
            api_response = MapperApi(
                get_api_client()
            ).mapper_entity_id_to_ccid_retrieve()
            return api_response.mapper  # Return the mapping from the API response.
        except Exception as e:
            print(
                f"Mapper API call failed: {e}"
            )  # Log any exceptions encountered during the API call.
            return None
