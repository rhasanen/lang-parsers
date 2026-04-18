from parsers.rpg_plex import parse_file


def test_parse_file_is_callable():
    assert callable(parse_file)
