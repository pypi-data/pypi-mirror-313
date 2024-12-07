import pygame
import collections

from trosnoth.data import user_path


def mouseButton(button):
    return -button


# 1. We want to be able to represent a shortcut as a string.
def shortcutName(key, modifiers=0):
    try:
        name = NAMED[key]
    except KeyError:
        if key < 0:
            name = 'Mouse%d' % (-key,)
        else:
            name = pygame.key.name(key)

    # Add the modifiers.
    modString = ''
    for kmod, modName in KMOD_NAMES:
        if modifiers & kmod:
            modString = '%s%s+' % (modString, modName)

    return '%s%s' % (modString, name)


NAMED = {
    -1: 'L.Click', -2: 'M.Click', -3: 'R.Click', -4: 'Scroll up', -5: 'Scroll down',

    pygame.K_BACKSPACE: 'Backspace', pygame.K_BREAK: 'Break',
    pygame.K_CAPSLOCK: 'Capslock', pygame.K_CLEAR: 'Clear',
    pygame.K_DELETE:
    'Del', pygame.K_DOWN: 'Down', pygame.K_END: 'End', pygame.K_ESCAPE:
    'Escape', pygame.K_EURO: 'Euro', pygame.K_F1: 'F1', pygame.K_F2: 'F2',
    pygame.K_F3: 'F3', pygame.K_F4: 'F4', pygame.K_F5: 'F5', pygame.K_F6:
    'F6', pygame.K_F7: 'F7', pygame.K_F8: 'F8', pygame.K_F9: 'F9',
    pygame.K_F10: 'F10', pygame.K_F11: 'F11', pygame.K_F12: 'F12',
    pygame.K_F13: 'F13', pygame.K_F14: 'F14', pygame.K_F15: 'F15',
    pygame.K_HELP: 'Help', pygame.K_HOME: 'Home',
    pygame.K_INSERT: 'Ins', pygame.K_LALT: 'L.Alt', pygame.K_LCTRL:
    'L.Ctrl', pygame.K_LEFT: 'Left', pygame.K_LMETA: 'L.Meta',
    pygame.K_LSHIFT: 'L.Shift', pygame.K_LSUPER: 'L.Super', pygame.K_MENU:
    'Menu', pygame.K_MODE: 'Mode', pygame.K_NUMLOCK: 'Numlock',
    pygame.K_PAGEDOWN: 'PgDn', pygame.K_PAGEUP: 'PgUp', pygame.K_PAUSE:
    'Pause', pygame.K_POWER: 'Power', pygame.K_PRINT: 'Print',
    pygame.K_RALT: 'R.Alt', pygame.K_RCTRL: 'R.Ctrl', pygame.K_RETURN:
    'Return', pygame.K_RIGHT: 'Right', pygame.K_RMETA: 'R.Meta',
    pygame.K_RSHIFT: 'R.Shift', pygame.K_RSUPER: 'R.Super',
    pygame.K_SCROLLOCK: 'Scrolllock', pygame.K_SYSREQ: 'SysRq', pygame.K_TAB:
    'Tab', pygame.K_UP: 'Up', pygame.K_SPACE: 'Space',

    pygame.K_KP0: 'keypad-0', pygame.K_KP1: 'keypad-1', pygame.K_KP2:
    'keypad-2', pygame.K_KP3: 'keypad-3', pygame.K_KP4: 'keypad-4',
    pygame.K_KP5: 'keypad-5', pygame.K_KP6: 'keypad-6', pygame.K_KP7:
    'keypad-7', pygame.K_KP8: 'keypad-8', pygame.K_KP9: 'keypad-9',
    pygame.K_KP_DIVIDE: 'keypad divide', pygame.K_KP_ENTER: 'keypad enter',
    pygame.K_KP_EQUALS: 'keypad equals', pygame.K_KP_MINUS: 'keypad minus',
    pygame.K_KP_MULTIPLY: 'keypad asterisk', pygame.K_KP_PERIOD:
    'keypad full stop', pygame.K_KP_PLUS: 'keypad plus',
 }

try:
    NAMED[pygame.K_AC_BACK] = '←'
    NAMED[pygame.K_CURRENCYSUBUNIT] = 'Cents'
except AttributeError:
    # These symbols don't exist in pygame 1
    pass

KMOD_NAMES = ((pygame.KMOD_CTRL, 'Ctrl'), (pygame.KMOD_ALT, 'Alt'),
              (pygame.KMOD_META, 'Meta'), (pygame.KMOD_SHIFT, 'Shift'))


# VirtualKeySet is a mapping from name -> default value.
class VirtualKeySet(collections.UserDict):
    pass


# KeyboardMapping is a mapping from key -> virtual key name.
class KeyboardMapping(collections.UserDict):
    def __init__(self, virtualKeys):
        self.virtualKeys = virtualKeys
        super().__init__(((default, vk) for (vk, default) in virtualKeys.items()))

    def load(self, string=None):
        '''
        Restores a keyboard mapping from a configuration string.
        '''
        if string is None:
            try:
                f = open(user_path / 'keymap')
            except FileNotFoundError:
                string = ''
            else:
                with f:
                    string = f.read()

        self.data = {}

        # Update from string.
        unmappedKeys = dict(self.virtualKeys)

        lines = string.split('\n')
        if lines[0] == '0:pygame2':
            lines.pop(0)
            load_map = lambda x: x
        else:
            load_map = convert_from_pygame1

        for record in lines:
            if record == '':
                continue
            key, vk = record.split(':')
            self.data[load_map(int(key))] = vk
            if vk in unmappedKeys:
                del unmappedKeys[vk]

        # Fill in any unmapped keys from the defaults if possible.
        for vk, default in unmappedKeys.items():
            if default not in self.data:
                self.data[default] = vk

    def dumps(self):
        '''
        Returns a configuration string for this keyboard mapping.
        '''
        records = ['%d:%s' % item for item in self.data.items()]
        records.insert(0, '0:pygame2')
        return '\n'.join(records)

    def save(self, filename=None):
        if filename is None:
            filename = user_path / 'keymap'
        with open(filename, 'w') as f:
            f.write(self.dumps())

    def getkey(self, action):
        '''
        Returns one key that results in the given action or raises KeyError.
        '''
        for k, v in self.data.items():
            if v == action:
                return k
        raise KeyError(action)


PYGAME1_TO_PYGAME2 = {
    318: 1073741896, 301: 1073741881, 12: 1073741980, 274: 1073741905, 279: 1073741901,
    321: 1073742004, 282: 1073741882, 291: 1073741891, 292: 1073741892, 293: 1073741893,
    294: 1073741928, 295: 1073741929, 296: 1073741930, 283: 1073741883,
    284: 1073741884, 285: 1073741885, 286: 1073741886, 287: 1073741887,
    288: 1073741888, 289: 1073741889, 290: 1073741890, 315: 1073741941,
    278: 1073741898, 277: 1073741897, 256: 1073741922, 257: 1073741913,
    258: 1073741914, 259: 1073741915, 260: 1073741916, 261: 1073741917,
    262: 1073741918, 263: 1073741919, 264: 1073741920, 265: 1073741921,
    267: 1073741908, 271: 1073741912, 272: 1073741927, 269: 1073741910,
    268: 1073741909, 266: 1073741923, 270: 1073741911, 308: 1073742050,
    306: 1073742048, 276: 1073741904, 310: 1073742051, 304: 1073742049,
    311: 1073742051, 319: 1073741942, 313: 1073742081, 300: 1073741907,
    281: 1073741902, 280: 1073741899, 19: 1073741896, 320: 1073741926,
    316: 1073741894, 307: 1073742054, 305: 1073742052, 275: 1073741903,
    309: 1073742055, 303: 1073742053, 312: 1073742055, 302: 1073741895,
    317: 1073741978, 273: 1073741906,
}


def convert_from_pygame1(key):
    return PYGAME1_TO_PYGAME2.get(key, key)
