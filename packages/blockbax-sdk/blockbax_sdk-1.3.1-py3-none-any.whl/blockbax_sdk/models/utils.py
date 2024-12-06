from typing import Dict, Any


def remove_property_value_if_id_exists(properties_object: Dict[str, Any]):
    # FIXME: When fields are in here that are added in the API but not in the SDK these fields will not be removed
    #   This will result in fields being pushed together with the ValueId
    #   This currently results in an client error
    for data_type in ["NUMBER", "TEXT", "LOCATION", "MAP_LAYER", "IMAGE", "AREA"]:
        if data_type.lower() in properties_object:
            del properties_object[data_type.lower()]
    return properties_object
