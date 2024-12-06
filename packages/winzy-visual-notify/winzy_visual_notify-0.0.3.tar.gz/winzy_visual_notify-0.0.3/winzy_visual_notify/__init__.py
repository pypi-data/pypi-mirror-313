import winzy
from winzy_visual_notify.pyside6_speech_bubble import mainrun, get_character_choices
import sys
from random import choice


def create_parser(subparser):
    parser = subparser.add_parser("tell", description="Notify using visual artefacts like clippy and other things. ")
    # Add subprser arguments here.
    parser.add_argument("-t", "--text", type=str, nargs="*", help="Text to display")
    parser.add_argument("-c", "--character", choices = get_character_choices()+["random"], default="random",
                         help="Name of Character to display")
    return parser


class WinzyPlugin:
    """ Notify using visual artefacts like clippy and other things.  """
    __name__ = "tell"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)
    
    def main(self, args):
        text= args.text
        character_name = args.character.lower()
        if "-" in text:
            text = sys.stdin.read()
        else:
            text = " ".join(text)
        

        if character_name == "random":
            character_name = choice(get_character_choices())

        iret = mainrun(text, character_name)

    def hello(self, args):
        # this routine will be called when "winzy tell" is called.
        print("Hello! This is an example ``winzy`` plugin.")

tell_plugin = WinzyPlugin()

