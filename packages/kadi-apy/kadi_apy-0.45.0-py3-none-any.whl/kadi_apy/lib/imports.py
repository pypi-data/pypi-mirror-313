# Copyright 2023 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import hashlib
import json
import os
import zipfile
from tempfile import TemporaryDirectory
from urllib.parse import unquote

import jsonref
from dateutil import parser
from rdflib import DCTERMS
from rdflib import RDF
from rdflib import SH
from rdflib import XSD
from rdflib import Graph
from rdflib.collection import Collection as RDFCollection

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import generate_identifier
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template


def import_eln(manager, file_path):
    """Import an RO-Crate file following the "ELN" file specification."""
    with zipfile.ZipFile(file_path) as ro_crate, TemporaryDirectory() as tmpdir:
        if not (namelist := ro_crate.namelist()):
            raise KadiAPYInputError("Archive is empty.")

        # We assume the first path contains the root directory of the crate.
        root_dir = namelist[0].split("/")[0]
        metadata_file_name = "ro-crate-metadata.json"

        if f"{root_dir}/{metadata_file_name}" not in namelist:
            raise KadiAPYInputError("Missing metadata file in RO-Crate.")

        ro_crate.extractall(tmpdir)

        root_path = os.path.join(tmpdir, root_dir)
        metadata_file_path = os.path.join(root_path, metadata_file_name)

        try:
            with open(metadata_file_path, mode="rb") as metadata_file:
                metadata = json.load(metadata_file)
        except Exception as e:
            raise KadiAPYInputError("Error opening or parsing metadata file.") from e

        # Collect all entities in the JSON-LD graph.
        if (
            not isinstance((graph := metadata.get("@graph", [])), list)
            or not len(graph) > 0
        ):
            _raise_invalid_content("Graph is not an array or empty.")

        entities = {}

        for entity in graph:
            if isinstance(entity, dict) and "@id" in entity:
                entities[entity["@id"]] = entity

        if (metadata_file_entity := entities.get("ro-crate-metadata.json")) is None:
            _raise_invalid_content(
                f"Entity describing '{metadata_file_name}' is missing."
            )

        is_kadi4mat = False
        if (
            publisher_entity := metadata_file_entity.get("sdPublisher")
        ) is not None and isinstance(publisher_entity, dict):
            publisher_data = entities.get(publisher_entity.get("@id"), publisher_entity)
            publisher_name = publisher_data.get("name")

            if publisher_name == "Kadi4Mat":
                is_kadi4mat = True

        if (root_entity := entities.get("./")) is None:
            _raise_invalid_content("Root dataset missing in graph.")

        root_parts = _extract_list(root_entity, "hasPart")

        collection_id = None
        genre = root_entity.get("genre")

        # Create a collection.
        if genre == "collection" or (genre != "record" and len(root_parts) > 1):
            response = _create_resource(
                manager,
                Collection.base_path,
                {"title": root_entity.get("name", root_dir)},
            )
            collection_id = response.json()["id"]

        # If applicable, collect all link data so records contained in the crate can be
        # linked accordingly after their creation.
        record_links_data = {}

        # Import all datasets as records.
        for root_part in root_parts:
            if not isinstance(root_part, dict) or "@id" not in root_part:
                _raise_invalid_content("Root part is not an object or missing an @id.")

            if (dataset_entity := entities.get(root_part["@id"])) is None:
                _raise_invalid_content(f"Entity {root_part['@id']} missing in graph.")

            if dataset_entity.get("@type") != "Dataset":
                continue

            record_metadata = {
                "title": dataset_entity.get("name", dataset_entity["@id"]),
                "description": _extract_description(dataset_entity, entities),
            }

            # Try to support both lists and comma-separated values.
            if isinstance((keywords := dataset_entity.get("keywords")), list):
                record_metadata["tags"] = keywords
            elif isinstance(keywords, str):
                record_metadata["tags"] = keywords.split(",")

            response = _create_resource(manager, Record.base_path, record_metadata)
            record = manager.record(id=response.json()["id"])

            # Add the record to the collection, if applicable.
            if collection_id is not None:
                record.add_collection_link(collection_id)

            has_json_export = False
            dataset_parts = _extract_list(dataset_entity, "hasPart")

            # Import all files of the dataset.
            for dataset_part in dataset_parts:
                if not isinstance(dataset_part, dict) or "@id" not in dataset_part:
                    _raise_invalid_content(
                        "Dataset part is not an object or missing an @id."
                    )

                if (file_entity := entities.get(dataset_part["@id"])) is None:
                    _raise_invalid_content(
                        f"Entity {dataset_part['@id']} missing in graph."
                    )

                if file_entity.get("@type") != "File":
                    continue

                file_id = unquote(file_entity["@id"]).split("/", 1)[-1]
                file_path = os.path.realpath(os.path.join(root_path, file_id))

                # Ensure that the file path is contained within the root path in the
                # temporary directory.
                if os.path.commonpath([root_path, file_path]) != root_path:
                    _raise_invalid_content(f"Referenced file {file_path} is invalid.")

                file_name = file_entity.get("name", os.path.basename(file_path))
                file_description = _extract_description(file_entity, entities)
                file_encoding_format = file_entity.get("encodingFormat", "")
                file_checksum = file_entity.get("sha256")

                if file_checksum:
                    checksum = hashlib.sha256()

                    with open(file_path, mode="rb") as f:
                        while True:
                            buf = f.read(1_000_000)

                            if not buf:
                                break

                            checksum.update(buf)

                    if checksum.hexdigest() != file_checksum:
                        raise KadiAPYInputError(
                            f"SHA256 checksum mismatch for '{file_id}'."
                        )

                record.upload_file(file_path, file_name, file_description)

                if (
                    is_kadi4mat
                    and file_encoding_format == "application/json"
                    and file_name == f'{dataset_entity.get("identifier")}.json'
                ):
                    has_json_export = True
                    record_id, link_data = _handle_kadi_json_export(file_path, record)
                    record_links_data[record_id] = {
                        "link_data": link_data,
                        "record": record,
                    }

            if not has_json_export:
                property_values = _extract_list(dataset_entity, "variableMeasured")
                extras = _map_properties_to_extras(property_values, entities)
                record.edit(extras=extras)

        if record_links_data:
            for record_meta in record_links_data.values():
                record = record_meta["record"]
                links_data = record_meta["link_data"]

                for link_data in links_data:
                    # Only use outgoing links to avoid attempting to create duplicates.
                    if "record_to" in link_data:
                        prev_record_id = link_data["record_to"]["id"]

                        # Skip records that are not contained in the crate.
                        if prev_record_id not in record_links_data:
                            continue

                        new_record_id = record_links_data[prev_record_id]["record"].id

                        record.link_record(
                            new_record_id, link_data["name"], link_data["term"]
                        )


def _raise_invalid_content(msg):
    raise KadiAPYInputError(f"Invalid content in metadata file: {msg}")


def _extract_description(entity, entities):
    description = entity.get("description", "")

    if isinstance(description, dict):
        description_entity = entities.get(description.get("@id"))

        if (
            isinstance(description_entity, dict)
            and description_entity.get("@type") == "TextObject"
        ):
            description = description_entity.get("text", "")

    return str(description)


def _extract_list(entity, name):
    property = entity.get(name, [])

    if not isinstance(property, list):
        return []

    return property


def _map_properties_to_extras(property_values, entities):
    extras_list = []

    for property_value in property_values:
        property_value_entity = entities.get(property_value.get("@id"))

        if not isinstance(property_value_entity, dict):
            continue

        keys = str(property_value_entity.get("propertyID", "")).split(".")
        value = property_value_entity.get("value")

        if value is None:
            continue

        current_list = extras_list

        for index, key in enumerate(keys[:-1]):
            found = False

            for item in current_list:
                if item.get("key") == key:
                    current_list = item["value"]
                    found = True
                    break

            if not found:
                key_is_digit = (
                    keys[index + 1].isdigit() if index + 1 < len(keys) else False
                )

                nested_extra = {
                    # Kadi will simply ignore keys within lists.
                    "key": key,
                    "type": "list" if key_is_digit else "dict",
                    "value": [],
                }
                current_list.append(nested_extra)
                current_list = nested_extra["value"]

        extra = {
            "key": keys[-1],
            "type": type(value).__name__,
        }

        if extra["type"] == "str":
            try:
                value = parser.isoparse(value).isoformat()
                extra["type"] = "date"
            except:
                pass

        extra["value"] = value

        if property_value_entity.get("description") is not None:
            extra["description"] = _extract_description(property_value_entity, entities)

        if (term_iri := property_value_entity.get("identifier")) is not None:
            extra["term"] = str(term_iri)

        if (unit := property_value_entity.get("unitText")) is not None:
            extra["unit"] = str(unit)

        validation = {}

        minimum = property_value_entity.get("minValue")
        maximum = property_value_entity.get("maxValue")

        if minimum is not None or maximum is not None:
            validation["range"] = {"min": minimum, "max": maximum}

        if validation:
            extra["validation"] = validation

        current_list.append(extra)

    return extras_list


def _handle_kadi_json_export(file_path, record):
    try:
        with open(file_path, mode="rb") as f:
            json_data = json.load(f)
    except Exception as e:
        raise KadiAPYInputError("Error opening or parsing JSON export file.") from e

    record.edit(
        extras=json_data.get("extras", []),
        license=json_data.get("license"),
        type=json_data.get("type"),
    )

    return json_data["id"], json_data.get("links", [])


def import_json_schema(manager, file_path, template_type):
    """Import JSON Schema file and create a template."""
    if template_type not in {"record", "extras"}:
        raise KadiAPYRequestError("Template type must be either 'record' or 'extras'")

    try:
        with open(file_path, mode="rb") as f:
            json_schema = jsonref.load(f)
    except Exception as e:
        raise KadiAPYInputError("Error opening or parsing JSON file.") from e

    template_data = {
        "title": json_schema.get(
            "title", os.path.basename(file_path).rsplit(".", 1)[0]
        ),
        "description": str(json_schema.get("description", "")),
        "type": template_type,
    }

    if not (properties := json_schema.get("properties", {})):
        raise KadiAPYInputError("Only objects are supported as top-level types.")

    propertiesOrder = json_schema.get("propertiesOrder", [])
    required = json_schema.get("required", [])

    extras = _json_schema_to_extras(properties, propertiesOrder, required)

    if template_type == "record":
        template_data["data"] = {"extras": extras}
    else:
        template_data["data"] = extras

    _create_resource(manager, Template.base_path, template_data)


JSON_SCHEMA_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
}


def _ordered_properties(properties, properties_order):
    if not properties_order:
        return properties.items()

    def _order_func(item):
        try:
            return properties_order.index(item[0])
        except ValueError:
            return 0

    return sorted(properties.items(), key=_order_func)


def _json_schema_to_extras(properties, properties_order=None, required_props=None):
    required_props = required_props if required_props is not None else []
    properties_order = properties_order if properties_order is not None else []

    extras = []

    if isinstance(properties, dict):
        properties_iter = _ordered_properties(properties, properties_order)
    else:
        properties_iter = enumerate(properties)

    for key, value in properties_iter:
        # Keys within lists will simply be ignored by Kadi.
        extra = {"key": key}

        if (extra_description := value.get("description")) is not None:
            extra["description"] = str(extra_description)

        # We just use "string" as fallback type, as extras always need an explicit type.
        value_type = value.get("type", "string")

        if isinstance(value_type, list):
            value_type = value_type[0]

        if value_type in {"object", "array"}:
            extra["type"] = "dict" if value_type == "object" else "list"

            if value_type == "object":
                result = _json_schema_to_extras(
                    value.get("properties", {}),
                    value.get("propertiesOrder", []),
                    value.get("required", []),
                )
            else:
                if (items := value.get("items")) is not None:
                    result = _json_schema_to_extras([items])
                else:
                    result = _json_schema_to_extras(value.get("prefixItems", []))

            extra["value"] = result
        else:
            if value_type == "string":
                extra["type"] = "date" if value.get("format") == "date-time" else "str"
            else:
                extra["type"] = JSON_SCHEMA_TYPE_MAPPING.get(value_type, "str")

            if (default := value.get("default")) is not None:
                extra["value"] = default

            # This handling of the custom "unit" property only works for files exported
            # via Kadi.
            if (unit := value.get("unit")) is not None:
                extra["unit"] = unit.get("default")

            validation = {}

            if key in required_props:
                validation["required"] = True

            if (options := value.get("enum")) is not None:
                validation["options"] = options

            minimum = value.get("minimum")
            maximum = value.get("maximum")

            if minimum is not None or maximum is not None:
                validation["range"] = {"min": minimum, "max": maximum}

            if validation:
                extra["validation"] = validation

        extras.append(extra)

    return extras


def import_shacl(manager, file_path, template_type):
    """Import SHACL Shapes file and create a template."""
    if template_type not in {"record", "extras"}:
        raise KadiAPYRequestError("Template type must be either 'record' or 'extras'")

    try:
        graph = Graph()

        with open(file_path, mode="rb") as f:
            graph.parse(f)
    except Exception as e:
        raise KadiAPYInputError(
            "Error opening or parsing the SHACL shapes file."
        ) from e

    # This assumes that the "root" subject is always listed first.
    if (current_ref := graph.value(predicate=RDF.type, object=SH.NodeShape)) is None:
        raise KadiAPYInputError(
            "sh:NodeShape at the root is missing as an object with rdf:type."
        )

    template_data = {
        "title": str(
            graph.value(
                current_ref,
                DCTERMS.title,
                default=os.path.basename(file_path).rsplit(".", 1)[0],
            )
        ),
        "description": str(graph.value(current_ref, DCTERMS.description, default="")),
        "type": template_type,
    }

    extras = _shacl_to_extras(current_ref, graph)

    if template_type == "record":
        template_data["data"] = {"extras": extras}
    else:
        template_data["data"] = extras

    _create_resource(manager, Template.base_path, template_data)


XSD_TYPE_MAPPING = {
    XSD.integer: "int",
    XSD.int: "int",
    XSD.float: "float",
    XSD.decimal: "float",
    XSD.double: "float",
    XSD.boolean: "bool",
    XSD.dateTime: "date",
}


def _ordered_objects(graph, subject, predicate):
    def _order_func(obj):
        order = graph.value(obj, SH.order)
        return order.value if order is not None else 0

    return sorted(graph.objects(subject, predicate), key=_order_func)


def _shacl_to_extras(graph, current_subject, visited=None):
    extras = []

    if visited is None:
        # Keep track of visited nodes to avoid potential loops, depending on the SHACL
        # structure.
        visited = set()

    # Handle (nested) objects that are referenced via sh:node.
    for node_objects in _ordered_objects(graph, current_subject, SH.node):
        extras.extend(_shacl_to_extras(graph, node_objects))

    # Handle objects that are referenced via sh:property.
    for property_object in _ordered_objects(graph, current_subject, SH.property):
        if (extra_key := graph.value(property_object, SH.name)) is None:
            continue

        extra = {
            # Keys within lists will simply be ignored by Kadi.
            "key": extra_key.value,
            "type": "str",
            "value": None,
        }

        if (term_iri := graph.value(property_object, SH.path)) is not None:
            extra["term"] = str(term_iri)

        if (
            extra_description := graph.value(property_object, SH.description)
        ) is not None:
            extra["description"] = str(extra_description)

        # Handle nested objects that are referenced via sh:qualifiedValueShape or
        # sh:node.
        nested_objects = _ordered_objects(
            graph, property_object, SH.qualifiedValueShape
        ) or _ordered_objects(graph, property_object, SH.node)

        for nested_object in nested_objects:
            if nested_object is not None and nested_object not in visited:
                visited.add(nested_object)
                nested_extras = _shacl_to_extras(graph, nested_object, visited)

                # Use a list if the first key looks like an index, which is mostly
                # relevant for SHACL data exported via Kadi.
                if len(nested_extras) > 0 and nested_extras[0]["key"] == "0":
                    extra["type"] = "list"
                else:
                    extra["type"] = "dict"

                extra["value"] = nested_extras

        # Handle the individual extra objects.
        if (value_type := graph.value(property_object, SH.datatype)) is not None:
            # We use "str" as fallback type, as extras always need an explicit type.
            extra["type"] = XSD_TYPE_MAPPING.get(value_type, "str")

            if (
                default_value := graph.value(property_object, SH.defaultValue)
            ) is not None:
                extra["value"] = default_value.value

            validation = {}

            if value_type == XSD.anyURI:
                validation["iri"] = True

            if (
                min_count := graph.value(property_object, SH.minCount)
            ) is not None and min_count.value >= 1:
                validation["required"] = True

            if (options := graph.value(property_object, SH["in"])) is not None:
                options_list = RDFCollection(graph, options)
                validation["options"] = [option.value for option in options_list]

            minimum = graph.value(property_object, SH.minInclusive)
            maximum = graph.value(property_object, SH.maxInclusive)

            if minimum is not None or maximum is not None:
                validation["range"] = {
                    "min": minimum.value if minimum is not None else None,
                    "max": maximum.value if maximum is not None else None,
                }

            if validation:
                extra["validation"] = validation

        extras.append(extra)

    return extras


def _create_resource(manager, base_path, metadata):
    base_identifier = generate_identifier(metadata["title"])
    metadata["identifier"] = base_identifier

    index = 1

    while True:
        response = manager._post(base_path, json=metadata)

        if response.status_code == 201:
            return response

        errors = response.json().get("errors", {})

        # Check if only the identifier was the problem and attempt to fix it.
        if "identifier" in errors and len(errors) == 1:
            suffix = f"-{str(index)}"
            metadata["identifier"] = f"{base_identifier[:50-len(suffix)]}{suffix}"

            index += 1
        else:
            raise KadiAPYRequestError(response.json())

        # Just in case, to make sure we never end up in an endless loop.
        if index > 100:
            break

    raise KadiAPYRequestError("Error attempting to create resource.")
