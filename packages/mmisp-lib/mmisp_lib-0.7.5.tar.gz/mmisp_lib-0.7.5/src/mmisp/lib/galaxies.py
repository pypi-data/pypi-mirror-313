import json


def json_or_original_string(s: str) -> str | dict | list:
    try:
        return json.loads(s)
    except json.decoder.JSONDecodeError:
        return s


def parse_galaxy_authors(str_authors: str | list) -> list[str]:
    if isinstance(str_authors, list):
        return str_authors
    parsed_author = json_or_original_string(str_authors)
    if isinstance(parsed_author, str):
        parsed_author = [parsed_author]  # force to be a list
    assert isinstance(parsed_author, list)

    return parsed_author


def galaxy_tag_name(galaxy_type: str, galaxy_cluster_uuid: str) -> str:
    return f'misp-galaxy:{galaxy_type}="{galaxy_cluster_uuid}"'
