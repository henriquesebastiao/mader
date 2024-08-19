from madr.utils import sanitize


def test_sanitize_with_title_text():
    text_origin = 'Text Text'
    text = sanitize(text_origin)

    assert text == 'text text'


def test_sanitize_with_text_uppercase():
    text_origin = 'TEXT TEXT'
    text = sanitize(text_origin)

    assert text == 'text text'


def test_sanitize_with_mores_spaces_in_middle():
    text_origin = 'TEXT      TEXT'
    text = sanitize(text_origin)

    assert text == 'text text'


def test_sanitize_with_mores_spaces_init_and_end():
    text_origin = ' TEXT TEXT '
    text = sanitize(text_origin)

    assert text == 'text text'
