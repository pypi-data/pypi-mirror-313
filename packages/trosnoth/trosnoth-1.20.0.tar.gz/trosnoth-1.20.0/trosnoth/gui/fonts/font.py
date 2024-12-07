from pathlib import Path

from trosnoth.data import get_overridable_path
from trosnoth.gui.fonts import fontcache


class Font(object):
    def __init__(self, name, size, bold=False):
        self._name = name
        self._size = size
        self._bold = bold
        self._filename = None

    def render(self, app, text, antialias, colour, background=None):
        if background is None:
            return self._getFont(app).render(text, antialias, colour)
        else:
            return self._getFont(app).render(text, antialias, colour, background)

    def size(self, app, text):
        return self._getFont(app).size(text)

    def getLineSize(self, app):
        return self._getFont(app).get_linesize()

    def getHeight(self, app):
        return self._getFont(app).get_height()

    def _getFont(self, app):
        if self._filename is None:
            self._filename = str(get_overridable_path(Path('fonts') / self._name))
        return fontcache.get(self._filename, self._size, self._bold)

    def __repr__(self):
        return 'Font: %s size %d' % (self._name, self._size)


class ScaledFont(Font):
    def _getFont(self, app):
        if self._filename is None:
            self._filename = str(get_overridable_path(Path('fonts') / self._name))
        return fontcache.get(
            self._filename, int(self._size * app.screenManager.scaleFactor + 0.5), self._bold)

    def __repr__(self):
        return 'Scaled Font: %s size %d' % (self._name, self._size)
