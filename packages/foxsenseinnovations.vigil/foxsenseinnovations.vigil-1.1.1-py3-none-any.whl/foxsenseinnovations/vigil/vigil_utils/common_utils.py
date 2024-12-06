from typing import Any, Dict, List
import re

class MaskOptions:
    """
    MaskOptions is used to define options for masking sensitive data in API requests.
    Attributes:
        mask_with (str): The character used for masking sensitive data.
        fields (List[str]): List of fields to be masked.
        prefixes (List[str]): List of prefixes of fields to be masked.
    """
    def __init__(self, mask_with: str, fields: List[str], prefixes: List[str]) -> None:
        self.mask_with = mask_with
        self.fields = fields
        self.prefixes = prefixes

def mask_data(data: Dict[str, Any], mask_options: MaskOptions) -> Dict[str, Any]:
    """
    Mask sensitive data in the provided dictionary based on the given MaskOptions.
    Args:
        data (Dict[str, Any]): The dictionary containing data to be masked.
        mask_options (MaskOptions): Options for masking sensitive data.
    Returns:
        Dict[str, Any]: The dictionary with sensitive data masked.
    """
    for key in data.keys():
        if key in mask_options.fields or any(key.startswith(prefix) for prefix in mask_options.prefixes):
            data[key] = mask_options.mask_with * 5
    return data

def generate_path(path: str, params: dict) -> str:
    """
    Generate a path with substituted parameters.
    Args:
        path (str): The original path containing placeholders.
        params (dict): Dictionary containing parameter values for substitution.
    Returns:
        str: The generated path with substituted parameters.
    """
    # Use regular expression to find placeholders in the path
    placeholders = re.findall(r'<([^>]+)>', path)
    if len(placeholders)==len(params):
      # Replace placeholders with corresponding values from params
      for i, placeholder in enumerate(placeholders):
          parts = placeholder.split(':')
          placeholder_name = parts[-1]  # Take the last part after the colon

          if placeholder_name in params:
              path = path.replace(f'<{placeholder}>', str(params[placeholder_name]))
              placeholders[i] = placeholder_name  # Update the list with the correct placeholder name

    return path