import logging
import pathlib

from trosnoth.data import makeDirs, user_path
from trosnoth.gamerecording.replays import ReplayRecorder

log = logging.getLogger(__name__)

REPLAY_DIR = user_path / 'replays'


class GameRecorder:
    '''
    In old versions of Trosnoth, this class was used to save an
    information file about every game played. It now just acts as a
    proxy to a ReplayRecorder, doing the work of deciding what filename
    to save to, and whether to actually save the replay.
    '''
    def __init__(self, world, save_replay=False, game_prefix='unnamed', replay_path=REPLAY_DIR):
        self.alias = f'{game_prefix} game'
        self.world = world
        self.save_replay = save_replay
        self.replay_base = pathlib.Path(replay_path)
        self.replay_path = None
        self.currently_saving = False
        self.replay_recorder = None

    def consume_msg(self, msg):
        if self.currently_saving:
            self.replay_recorder.consumeMsg(msg)

    def select_available_filename(self):
        makeDirs(self.replay_base)
        copy_count = 0
        while True:
            filepath = self.replay_base / f'{self.alias} ({copy_count}).trosrepl'
            if not filepath.exists():
                return filepath
            copy_count += 1

    def match_started(self):
        self.stop_saving()
        if not (self.save_replay and self.world.scenarioManager.level.recordGame):
            return

        self.currently_saving = True
        self.replay_path = self.select_available_filename()
        self.replay_recorder = ReplayRecorder(self.world, self.replay_path)

    def start(self):
        self.world.onStartMatch.addListener(self.match_started)
        self.world.on_end_match.addListener(self.stop_saving)

    def stop(self):
        self.world.onStartMatch.removeListener(self.match_started)
        self.world.on_end_match.removeListener(self.stop_saving)
        self.stop_saving()

    def stop_saving(self, *args, **kwargs):
        if not self.currently_saving:
            return
        if self.replay_recorder:
            self.replay_recorder.stop()
        self.currently_saving = False
