#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from glob import glob
from os import popen, makedirs
from os.path import join as joinpath, split as splitpath, dirname, expanduser, abspath, isfile
from sys import argv, exit
from warnings import simplefilter

# classes

class args:
    'container for arguments'
    pass

# constants

LETTERS = 'mtplsbc' 

COMMENT = { 
    'm': 'minimize visible windows',
    't': 'reshape visible windows as tiles',
    'p': 'reshape visible windows as portraits',
    'l': 'reshape visible windows as landscapes',
    's': 'reshape visible windows as a stack',
    'b': 'maximize visible windows',
    'c': 'gracefully close visible windows'}

RENAMED = { # 0.9.5 arguments renamed in 1.0.0
    '-i':         '-L',
    '--install':  '--launchers',
    '-k':         '-S',
    '--keyboard': '--shortcuts',
    '--big':      '--maximize'}

# generic functions

def longpath(path):
    'return abspath(expanduser(path))'
    return abspath(expanduser(path))

def shell(command):
    'perform shell command and return stdout as a list of rstripped lines'
    return [line.rstrip() for line in popen(command)]

def package_file(file):
    'return abspath of package local file'
    return joinpath(dirname(__file__), file)

def take(string, chars, default=''):
    'return string with any char not in chars translated into default'
    return ''.join(char if char in chars else default for char in string)

def drop(string, chars, default=''):
    'return string with any char in chars translated into default'
    return ''.join(default if char in chars else char for char in string)

def shrink(string):
    'return string with no initial and final blanks and with internal multiple blanks reduced to single blanks'
    return ' '.join(string.split())

def nocomment(string):
    "extract statement from string by eliminating '#'-comments"
    return string.split('#')[0].strip()

def error(message):
    'print error message and exit'
    exit('ERROR: ' + message)

def warning(message):
    'print warning message'
    print('WARNING: ' + message)

def look_for(program, whereis=None):
    'check if program is reachable'
    if not shell(f'which {program}'):
        error(f'{program!r} not found, please install {whereis or program!r}')
    
# specific functions

def current_desktop_fields():
    'return current desktop as a list of fields'
    return [fields for fields in [drop(line, 'x,/', ' ').split() for line in shell('wmctrl -d')] if fields[1] == '*'][0]

def desktop_windows(desktop):
    "return a list of windows in a given desktop"
    return [fields[0] for fields in [line.split() for line in shell('wmctrl -l')] if int(fields[1]) == desktop]

def is_visible(window):
    'is window visible = not hidden = not minimized?'
    return all(line.strip() != 'Hidden' for line in shell(f'xwininfo -all -id {window}'))

def reshape(window, xpos, ypos, width, height):
    'change position and dimensions of a window'
    shell(f'wmctrl -i -a {window}')
    shell(f'wmctrl -i -r {window} -b remove,maximized_vert,maximized_horz')
    shell(f'wmctrl -i -r {window} -e 0,{xpos},{ypos},{width},{height}')

# main functions

def wmtile(argv): 
    'a window tiler for XFCE desktop environment'
    # wmtile itself
    wmtile = longpath('~/.local/bin/wmtile')
    # do external programs exist?
    look_for('wmctrl')
    look_for('xdotool')
    look_for('xwininfo','x11-utils')
    # obsolete arguments?
    for arg in argv[1:]:
        if arg in RENAMED:
            error(f'argument {arg!r} is obsolete, use {RENAMED[arg]!r} instead.')
    # get arguments
    parser = Parser(prog='wmtile', formatter_class=Formatter, description=description)
    parser.add_argument('-H', '--user-manual', action='store_true', help='browse the User Manual in PDF format and exit')
    parser.add_argument('-Y', '--pdf-browser', default='xdg-open',  help="PDF browser used by -H, default: 'xdg-open'")
    parser.add_argument('-V', '--version',     action='version',    version='WMTile ' + version)
    parser.add_argument('-L', '--launchers',   action='store_true', help='create 7 panel launchers')
    parser.add_argument('-S', '--shortcuts',   action='store_true', help='create 7 keyboard shortcuts')
    parser.add_argument('-m', '--minimize',    action='store_true', help=COMMENT['m'])
    parser.add_argument('-t', '--tile',        action='store_true', help=COMMENT['t'])
    parser.add_argument('-p', '--portrait',    action='store_true', help=COMMENT['p'])
    parser.add_argument('-l', '--landscape',   action='store_true', help=COMMENT['l'])
    parser.add_argument('-s', '--stack',       action='store_true', help=COMMENT['s'])
    parser.add_argument('-b', '--maximize',    action='store_true', help=COMMENT['b'])
    parser.add_argument('-c', '--close',       action='store_true', help=COMMENT['c'])
    parser.parse_args(argv[1:], args)
    # check arguments
    num_options = (args.user_manual + args.launchers + args.shortcuts + args.minimize + args.tile +
                 args.portrait + args.landscape + args.stack + args.maximize + args.close)
    if num_options != 1:
        error(f"options are {num_options} but they must be exactly 1, only -H and -Y can go together")
    if args.user_manual: # -H
        user_manual_file = package_file(f'docs/WMTile {version} User Manual.pdf')
        shell(f'{args.pdf_browser} {user_manual_file!r}')
        exit()
    # set parameter defaults
    bottom_space = 24 
    right_space  = 10
    top_stack    = 20
    left_stack   = 20
    # read parameters from configuration file (if any)
    configuration_file = longpath('~/.config/wmtile/wmtile.cfg')
    makedirs(dirname(configuration_file), exist_ok=True)
    if isfile(configuration_file):
        for jline, line in enumerate(open(configuration_file)):
            line = line.rstrip()
            statement = nocomment(line)
            if statement:
                try:
                    parameter, value = statement.split('=')
                    parameter, value = parameter.strip(), int(value.strip())
                    if value < 0:
                        raise ValueError
                    elif parameter == 'bottom_space':
                        bottom_space = value
                    elif parameter == 'right_space':
                        right_space = value
                    elif parameter == 'top_stack':
                        top_stack = value
                    elif parameter == 'left_stack':
                        left_stack = value
                    else:
                        raise ValueError
                except ValueError:
                    error(f'line {jline+1} {line!r} in configuration file {configuration_file!r}, ')
    # perform an action
    if args.launchers: # -L
        print('Creating 7 panel launchers...')
        existing_letters = set()
        for pathfile in glob(longpath('~/.config/xfce4/panel/launcher-*/*.desktop')):
            for line in open(pathfile):
                line = line.rstrip()
                if line.startswith('Name=wmtile-'):
                    existing_letters.add(line[-1])
        for x in LETTERS:
            wmtile_x = f'wmtile-{x}'
            if x in existing_letters:
                print(f"    panel launcher {wmtile_x!r} already exists")
            else:
                desktop_file = package_file(f"desktops/{wmtile_x}.desktop")
                icon_file = package_file(f"icons/{wmtile_x}.ico")
                open(desktop_file, "w").write(f"""[Desktop Entry]
Name={wmtile_x}
Exec={wmtile} -{x}
Comment={COMMENT[x]}
Icon={icon_file}
Terminal=false
Type=Application
StartupNotify=false
MimeType=text/plain;
Categories=Utility;""")
                shell(f"xfce4-panel --add=launcher {desktop_file}")
                print(f"    panel launcher {wmtile_x!r} not found, created")
    elif args.shortcuts: # -S
        print('Creating 7 keyboard shortcuts...')
        xfce_xml_file = longpath('~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml')
        if not isfile(xfce_xml_file):
            error('XFCE4 not found')
        buf = [line.rstrip() for line in open(xfce_xml_file)]
        first = True
        with open(xfce_xml_file, 'w') as xml:
            for line in buf:
                if 'wmtile' not in line:
                    print(line, file=xml)
                if first and '<property name="custom" type="empty">' in line:
                    first = False
                    for x in LETTERS:
                        X = x.upper()
                        print(f'    <property name="&lt;Alt&gt;&lt;Shift&gt;{X}" type="string" value="{wmtile} -{x}"/>', file=xml)
                        print(f"    keyboard shortcut Alt+Shift+{X} --> 'wmtile -{x}' created")
        print('Please reboot in order to make the keyboard shortcuts effective.')
    else:
        desktop_fields = current_desktop_fields()
        desktop, area_xpos, area_ypos, area_width, area_height = [int(desktop_fields[j]) for j in [0, 9, 10, 11, 12]]
        windows = desktop_windows(desktop)
        visible_windows = [window for window in windows if is_visible(window)]
        if visible_windows:
            windows = visible_windows
        if windows:
            num_windows = len(windows)
            if args.minimize: # -m
                for window in windows: 
                    shell(f'xdotool windowminimize {window}')
            elif args.stack: # -s
                window_width = area_width - left_stack * (num_windows - 1) - right_space
                window_height = area_height - top_stack * (num_windows - 1) - bottom_space
                for j_win, window in enumerate(windows):
                    window_xpos = area_xpos + left_stack * j_win
                    window_ypos = area_ypos + top_stack * j_win
                    reshape(window, window_xpos, window_ypos, window_width, window_height)
            elif args.maximize: # -b 
                for window in windows: 
                    shell(f'xdotool windowsize {window} 100% 100%')
            elif args.close: # -c
                for window in windows:
                    shell(f'wmctrl -i -c {window}')
            else: 
                if args.tile: # -t 
                    for num_rows, num_cols in ((rows, cols) for cols in range(1, 1000) for rows in [cols, cols + 1]):
                        if num_rows * num_cols >= num_windows:
                            break
                elif args.landscape: # -l
                    num_rows, num_cols = 1, num_windows 
                else: # args.portrait # -p
                    num_rows, num_cols = num_windows, 1
                window_width = area_width // num_rows - right_space
                window_height = area_height // num_cols - bottom_space
                for j_win, window in enumerate(windows):
                    j_row, j_col = divmod(j_win, num_rows)
                    window_xpos = area_xpos + j_col * (window_width + right_space)
                    window_ypos = area_ypos + j_row * (window_height + bottom_space)
                    reshape(window, window_xpos, window_ypos, window_width, window_height)
                        
def main():
    try:
        simplefilter('ignore')
        wmtile(argv)
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()
