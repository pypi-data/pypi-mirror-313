import pytest
import winzy_visual_notify as w
from winzy_visual_notify.pyside6_speech_bubble import get_character_choices

from argparse import ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(['--text', 'hello'])
    assert result.text == ["hello"]
    assert result.character == "random"


def test_plugin(capsys):
    w.tell_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out


def test_get_character_choices():
    choices = get_character_choices()
    assert len(choices) == 9
    assert "dog2" in choices
    assert "watermellon" in choices