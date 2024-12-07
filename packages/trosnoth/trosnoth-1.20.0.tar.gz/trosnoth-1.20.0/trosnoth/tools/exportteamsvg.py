#!/usr/bin/env python3

import argparse
import os
import pathlib
import subprocess
import sys
import tempfile
import traceback

import pygame
from lxml import etree

from trosnoth.const import MAP_TO_SCREEN_SCALE

# This script takes an SVG source file and uses it to generate a png
# base file, a png overlay file, and optionally a PNG file for the
# neutral / no team colour case.
#
# The SVG file should have some layers with names beginning with
# TROSNOTH:RedTeam, TROSNOTH:BlueTeam and/or TROSNOTH:NoTeam. These
# layers will be switched on and off to generate the images.
#
# This script will generate more correct results than teamify.py.


SVG = '{http://www.w3.org/2000/svg}'
INKSCAPE = '{http://www.inkscape.org/namespaces/inkscape}'
RED_PREFIX = 'TROSNOTH:RedTeam'
BLUE_PREFIX = 'TROSNOTH:BlueTeam'
TEAMLESS_PREFIX = 'TROSNOTH:NoTeam'
TEAM_PREFIXES = [RED_PREFIX, BLUE_PREFIX, TEAMLESS_PREFIX]


parser = argparse.ArgumentParser()
parser.add_argument('in_file')
parser.add_argument('out_stem', nargs='?')
parser.add_argument('--build-teamless', '-n', action='store_true')


class ElementWrapper:
    svg = None
    element = None

    def get(self, *args, **kwargs):
        return self.element.get(*args, **kwargs)

    def set(self, *args, **kwargs):
        return self.element.set(*args, **kwargs)

    def hide(self):
        self.set('style', 'display:none')

    def show(self):
        self.set('style', '')

    def get_parent(self):
        return SVGGroup(self.svg, self.element.getparent())

    def get_groups(self):
        for element in self.element.findall(SVG + 'g'):
            yield SVGGroup(self, element)


class SVGFile(ElementWrapper):
    def __init__(self, document):
        self.document = document
        self.element = document

    def get_dimensions(self):
        width = float(self.document.get('width'))
        height = float(self.document.get('height'))
        return width, height

    def get_layers(self, base=None):
        if base is None:
            base = self
        for group in base.get_groups():
            if group.get(INKSCAPE + 'groupmode') == 'layer':
                yield group
                yield from self.get_layers(group)   # Sub-layers


class SVGGroup(ElementWrapper):
    def __init__(self, svg, element):
        self.svg = svg
        self.element = element


def build_graphics(svg, build_teamless=False, verbose=False, scale=MAP_TO_SCREEN_SCALE):
    if verbose:
        print('Rendering red team graphics…')
    red_graphics = render_graphics(svg, team_layer=RED_PREFIX, scale=scale)
    if verbose:
        print('Rendering blue team graphics…')
    blue_graphics = render_graphics(svg, team_layer=BLUE_PREFIX, scale=scale)
    if build_teamless:
        if verbose:
            print('Rendering teamless graphics…')
        teamless_graphics = render_graphics(svg, team_layer=TEAMLESS_PREFIX, scale=scale)
    else:
        teamless_graphics = None

    if verbose:
        print('Calculating pixels…')
    w = red_graphics.get_width()
    h = red_graphics.get_height()
    base_graphics = pygame.surface.Surface((w, h), pygame.SRCALPHA)
    base_graphics.fill((255, 255, 255, 0))
    overlay_graphics = pygame.surface.Surface((w, h), pygame.SRCALPHA)
    overlay_graphics.fill((255, 255, 255, 0))

    red_graphics.lock()
    blue_graphics.lock()
    base_graphics.lock()
    overlay_graphics.lock()

    neutral_pixel = (127, 127, 127, 0)
    for y in range(h):
        for x in range(w):
            red_pixel = red_graphics.get_at((x, y))
            blue_pixel = blue_graphics.get_at((x, y))
            base_pixel, overlay_pixel = get_base_colours(red_pixel, blue_pixel)
            base_graphics.set_at((x, y), base_pixel)
            overlay_graphics.set_at((x, y), overlay_pixel)

    red_graphics.unlock()
    blue_graphics.unlock()
    base_graphics.unlock()
    overlay_graphics.unlock()

    return base_graphics, overlay_graphics, teamless_graphics


def get_base_colours(red_tinted_pixel, blue_tinted_pixel):
    '''
    This method accepts a colour from the red and blue team images, and
    calculates a base and overlay that would give these approximate
    results. It assumes that the red channel of the blue-tinted pixel
    has no team component, and that the blue and green channels of the
    red-tinted pixel have no team component.
    '''
    # Calculations are performed on a scale of 0…1
    rt_r, rt_g, rt_b, rt_a = [e / 255 for e in red_tinted_pixel]
    bt_r, bt_g, bt_b, bt_a = [e / 255 for e in blue_tinted_pixel]

    # Both input alphas should be the same, but we average them just
    # in case they're not
    in_a = (rt_a + bt_a) / 2
    if in_a == 0:
        # It's completely transparent, and continuing on will give a
        # division by zero error
        return red_tinted_pixel, red_tinted_pixel

    o_a = max(0, (rt_r - bt_r) * in_a)
    b_a = (in_a - o_a) / (1 - o_a)
    squish = 1 - o_a / in_a
    if squish == 0:
        # Pixel is 100% team colour, so base colour doesn't matter
        b_r = b_g = b_b  = .5
    else:
        b_r = bt_r / squish
        b_g = rt_g / squish
        b_b = rt_b / squish

    base_pixel = [round(255 * max(0, min(1, e))) for e in (b_r, b_g, b_b, b_a)]
    overlay_pixel = [round(255 * max(0, min(1, e))) for e in (1, 1, 1, o_a)]

    return base_pixel, overlay_pixel


def render_graphics(svg, team_layer, scale=MAP_TO_SCREEN_SCALE):
    for layer in svg.get_layers():
        label = layer.get(INKSCAPE + 'label')
        if label.startswith(team_layer):
            layer.show()
        else:
            for prefix in TEAM_PREFIXES:
                if label.startswith(prefix):
                    layer.hide()

    width, height = svg.get_dimensions()
    document = svg.document

    handle, infile = tempfile.mkstemp()
    os.close(handle)
    with open(infile, 'wb') as f:
        f.write(etree.tostring(document))

    handle, outfile = tempfile.mkstemp(suffix='.png')
    os.close(handle)
    out_width = int(width * scale + 0.5)
    out_height = int(height * scale + 0.5)
    proc = subprocess.run([
        'inkscape', infile,
        '--export-type=png',
        '--export-filename=%s' % (outfile,),
        '--export-width=%s' % (out_width,),
        '--export-height=%s' % (out_height,),
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError(f'inkscape returned code {proc.returncode}:\n{proc.stdout}')

    result = pygame.image.load(outfile)

    os.unlink(infile)
    os.unlink(outfile)
    return result


def main():
    args = parser.parse_args()

    in_file = pathlib.Path(args.in_file)
    if not in_file.is_file():
        parser.error('File not found: {}'.format(in_file))

    out_stem = args.out_stem
    if out_stem is None:
        if in_file.absolute().parent.name == 'source':
            out_stem = in_file.absolute().parents[1]
        else:
            out_stem = in_file.absolute().parent
    else:
        out_stem = pathlib.Path(out_stem)

    if out_stem.is_dir():
        out_stem /= in_file.stem

    run_export(in_file, out_stem, build_teamless=args.build_teamless)


def run_export(in_file, out_stem, build_teamless=False):
    with open(in_file, 'r') as f:
        document = etree.parse(f).getroot()
        svg = SVGFile(document)

    print('Calculating team masks…')
    base, overlay, no_team = build_graphics(svg, build_teamless=build_teamless, verbose=True)
    print('Saving files…')
    pygame.image.save(base, str(out_stem) + '-base.png')
    pygame.image.save(overlay, str(out_stem) + '-overlay.png')
    if no_team:
        pygame.image.save(no_team, str(out_stem) + '-no-team.png')
    print('Done.')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
