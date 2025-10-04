import os
import re
import json
from typing import List

def get_payload_filepaths(payloads_dir: str = "/opt/metasploit-framework/embedded/framework/modules/payloads/") -> List[str]:
    """Returns the filepath of every payload in the Metasploit payload directory specified.
    
    Returns:
        List.
    
    """
    payload_filenames = []
    for root, _, files in os.walk(payloads_dir):
        for file in files:
            if file.endswith(".rb"): 
                payload_filenames.append(os.path.join(root, file))
    return payload_filenames

def get_payload_metadata(filepath) -> dict[str, str]:
    """Parses the given Metasploit payload for metadata.
    
    Returns:
        Dict.
    
    """
    # Open the file at the filepath given and copy it's contents into memory.
    with open(filepath, encoding="utf-8", mode="r") as buffer:
        payload = buffer.read()
    
    # Save the payload's metadata fields to variables.
    name_match = re.search(r"'Name'\s*=>\s*'([^']+)'", payload)
    description_match = re.search(r"'Description'\s*=>\s*'([^']+)'", payload)
    platform_match = re.search(r"'Platform'\s*=>\s*'([^']+)'", payload)
    arch_match = re.search(r"'Arch'\s*=>\s*([^,]+)", payload)
    handler_match = re.search(r"'Handler'\s*=>\s*([^,]+)", payload)
    session_match = re.search(r"'Session'\s*=>\s*([^,]+)", payload)
    payload_type_match = re.search(r"'PayloadType'\s*=>\s*'([^']+)'", payload)

    # Init a dict containing the payload's metadata.
    payload_metadata = {
        "name": name_match.group(1) if name_match else None,
        "description": description_match.group(1) if description_match else None,
        "platform": platform_match.group(1) if platform_match else None,
        "arch": arch_match.group(1) if arch_match else None,
        "handler": handler_match.group(1) if handler_match else None,
        "session": session_match.group(1).strip() if session_match else None,
        "payload_type": payload_type_match.group(1) if payload_type_match else None
    }

    # Remove fields that null and return the resulting dict.
    return {key: value for key, value in payload_metadata.items() if value is not None}

def get_payloads() -> List[dict]:
    """Used for getting metadata about all of Metasploit's payloads.
    
    Returns:
        List.
    
    """
    payloads = []
    for payload_filepath in get_payload_filepaths():
        payloads.append(get_payload_metadata(payload_filepath))
    return payloads
