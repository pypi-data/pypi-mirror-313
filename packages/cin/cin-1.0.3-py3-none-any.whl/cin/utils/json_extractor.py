import re
import json

def extract_json(input_string: str) -> str:
    """
    Extracts a single JSON array from an unstructured string.

    Args:
        input_string (str): The potentially unstructured json string containing the embedded JSON array.

    Returns:
        str: A JSON array as a string. Only wraps in additional array if the extracted content
             is not already an array.

    Raises:
        ValueError: If no valid JSON array is found
    """
    # First, try to handle markdown code blocks with ```json
    code_block_pattern = r'```json\n([\s\S]*?)```'
    code_block_match = re.search(code_block_pattern, input_string)
    if code_block_match:
        input_string = code_block_match.group(1).strip()
        try:
            # If the extracted content is valid JSON and already an array, return as is
            parsed = json.loads(input_string)
            if isinstance(parsed, list):
                return input_string
            # If it's not an array, wrap it
            return f'[{input_string}]'
        except json.JSONDecodeError:
            pass

    # Look for outermost array pattern
    array_pattern = r'^\s*(\[(?:[^[\]]|\[(?:[^[\]]|\[(?:[^[\]]|\[[^[\]]*\])*\])*\])*\])'
    matches = re.finditer(array_pattern, input_string, re.MULTILINE)

    valid_arrays = []
    for match in matches:
        potential_array = match.group(1)
        try:
            # Verify it's valid JSON by attempting to parse it
            parsed = json.loads(potential_array)
            # Only wrap in additional array if not already an array
            if isinstance(parsed, list):
                valid_arrays.append(potential_array)
            else:
                valid_arrays.append(f'[{potential_array}]')
        except json.JSONDecodeError:
            continue

    if not valid_arrays:
        raise ValueError("No valid JSON array found in the input string")

    # Return the first valid array found
    return valid_arrays[0]