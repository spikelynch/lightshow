#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
Utility to make HSV lerp gradients and build them from JSON config files
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'


import argparse, json, random, colorsys
from color_ansi_rgb import ColorANSIRGB



def toholiday(f):
    return int(63 * f)

def holidayrgb(h, s, v):
    ( r0, g0, b0 ) = colorsys.hsv_to_rgb(h, s, v)
    return ( toholiday(r0), toholiday(g0), toholiday(b0) )

def hexint(f):
    return "{:02x}".format(int(f * 255))

def hexrgb(h, s, v):
    ( r0, g0, b0 ) = colorsys.hsv_to_rgb(h, s, v)
    return "#" + hexint(r0) + hexint(g0) + hexint(b0)

def rgbtuple(h, s, v):
    ( r0, g0, b0 ) = colorsys.hsv_to_rgb(h, s, v)
    return ( int(255 * r0), int(255 * g0), int(255 * b0) )    

def lerpl(x1, x2, m):
    """Linear interpolation between x1 and x2 where 0 <= k <= m"""
    return lambda k: x1 + (x2 - x1) * (1.0 * k / m)

def hsvgrad(targetfn, n, c1, c2):
    """Return an array of n RGB tuples, interpolated between the
    two HSV endpoints

    todo: presets where you can pass in strings like "red" or "green"
    """

    hl = lerpl(c1[0], c2[0], n - 1)
    sl = lerpl(c1[1], c2[1], n - 1)
    vl = lerpl(c1[2], c2[2], n - 1)
    return [ targetfn(hl(i), sl(i), vl(i)) for i in range(0, n) ]
    

def json_old(json):
    """Build a list of colours from a JSON structure"""
    start = { 'h': 0, 's': 0, 'v': 0 }
    grad = []
    for gdef in json:
        if 'start' in gdef:
            start = gdef['start']
        end = gdef['end']
        grad += hsvgrad(
            gdef['n'],
            start['h'], start['s'], start['v'],
            end['h'], end['s'], end['v']
            )
        start = end
    return grad

def makeGradient(target, n, grads):
    """
target - 'holiday' or 'ansi'
n - number of colours in output
grads - an array of [ h, s, v ] colors
"""
    ngrads = len(grads) - 1
    gradls = partition(n, ngrads)
    grad = []
    start = None
    if target == 'holiday':
        targetfn = holidayrgb
    else:
        targetfn = hexrgb
    for i in range(ngrads):
        grad += hsvgrad(targetfn, gradls[i], grads[i], grads[i + 1])
    return grad

def partition(m, n):
    """Partition the integer m into n integers which sum to m and are just about equal
    adapted from https://mathematica.stackexchange.com/questions/27959/partitioning-an-integer-into-k-equal-parts
    """
    return [ ( m + i - 1 ) // n for i in range(1, n + 1 )]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", type=int, help="Length of gradient")
    parser.add_argument("-c", "--colours", type=str, help="JSON list of hsv triples")
    args = parser.parse_args()
    ansi = ColorANSIRGB()
    if args.length and args.colours:
        gradient = makeGradient('ansi', args.length, json.loads(args.colours))
        output = "".join([ ansi.rgb(c) + '█' for c in gradient ])
        print(output)
        print(ansi.reset())
    else:
        print("gradient.py -l LENGTH -c JSON_COLOURS")
