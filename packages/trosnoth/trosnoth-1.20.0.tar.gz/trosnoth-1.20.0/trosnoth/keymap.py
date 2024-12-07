import pygame

from trosnoth.const import (
    ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE, ACTION_LEFT,
    ACTION_DOWN, ACTION_RIGHT, ACTION_JUMP, ACTION_HOOK, ACTION_FOLLOW,
    ACTION_RADIAL_UPGRADE_MENU, ACTION_USE_UPGRADE, ACTION_BUY_AMMO,
    ACTION_RESPAWN,
    ACTION_READY, ACTION_CLEAR_UPGRADE, ACTION_CHAT,
    ACTION_PAUSE_GAME, ACTION_TERMINAL_TOGGLE, ACTION_NEXT_WEAPON, ACTION_PREVIOUS_WEAPON,
    ACTION_CONTRIBUTE_TO_TEAM_BOOST, ACTION_NEXT_TEAM_BOOST, ACTION_TOGGLE_FULLSCREEN,
    ACTION_GUN_SLOT_1, ACTION_GUN_SLOT_2, ACTION_GUN_SLOT_3, ACTION_GUN_SLOT_4, ACTION_GUN_SLOT_5,
)
from trosnoth.gui.keyboard import VirtualKeySet, mouseButton

# Define virtual keys and their default bindings.
default_game_keys = VirtualKeySet((
    # Movement keys.
    (ACTION_LEFT, pygame.K_a),
    (ACTION_DOWN, pygame.K_s),
    (ACTION_RIGHT, pygame.K_d),
    (ACTION_JUMP, pygame.K_w),
    (ACTION_HOOK, mouseButton(3)),
    (ACTION_SHOW_TRAJECTORY, pygame.K_LSHIFT),
    (ACTION_DEBUGKEY, mouseButton(2)),
    (ACTION_PREVIOUS_WEAPON, mouseButton(4)),
    (ACTION_NEXT_WEAPON, mouseButton(5)),
    (ACTION_BUY_AMMO, pygame.K_e),

    # Used in replay mode.
    (ACTION_FOLLOW, pygame.K_EQUALS),
    (ACTION_TOGGLE_FULLSCREEN, pygame.K_F11),

    (ACTION_RADIAL_UPGRADE_MENU, pygame.K_TAB),
    (ACTION_USE_UPGRADE, pygame.K_SPACE),
    (ACTION_RESPAWN, pygame.K_r),
    (ACTION_READY, pygame.K_y),
    (ACTION_EMOTE, pygame.K_t),
    (ACTION_CONTRIBUTE_TO_TEAM_BOOST, pygame.K_c),
    (ACTION_NEXT_TEAM_BOOST, pygame.K_x),

    (ACTION_CLEAR_UPGRADE, pygame.K_0),

    (ACTION_CHAT, pygame.K_RETURN),
    (ACTION_PAUSE_GAME, pygame.K_PAUSE),

    (ACTION_GUN_SLOT_1, pygame.K_1),
    (ACTION_GUN_SLOT_2, pygame.K_2),
    (ACTION_GUN_SLOT_3, pygame.K_3),
    (ACTION_GUN_SLOT_4, pygame.K_4),
    (ACTION_GUN_SLOT_5, pygame.K_5),

    (ACTION_TERMINAL_TOGGLE, pygame.K_SCROLLOCK),
))

from trosnoth.model.upgrades import allUpgrades, gun_types

for upgradeClass in allUpgrades:
    if upgradeClass.default_key is not None:
        default_game_keys[upgradeClass.action] = upgradeClass.default_key
del upgradeClass

for gun_type in gun_types:
    if gun_type.default_key is not None:
        default_game_keys[gun_type.action] = gun_type.default_key
del gun_type
