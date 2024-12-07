import functools

from trosnoth.utils.utils import run_async_main_function
from trosnoth.welcome.common import initialise_qt_application
from trosnoth.welcome.welcome import WelcomeScreen


def launch_trosnoth(show_replay=None):
    initialise_qt_application()
    welcome_screen = WelcomeScreen()
    run_async_main_function(functools.partial(welcome_screen.run, show_replay=show_replay))
