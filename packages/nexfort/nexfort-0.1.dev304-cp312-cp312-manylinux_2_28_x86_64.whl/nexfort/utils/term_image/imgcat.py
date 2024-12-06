from __future__ import print_function
import base64
import os
import sys

def print_osc(terminal):
    if terminal.startswith('screen') or terminal.startswith('tmux'):
        print_partial('\x1bPtmux;\x1b\x1b]')
    else:
        print_partial('\x1b]')

def print_st(terminal):
    if terminal.startswith('screen') or terminal.startswith('tmux'):
        print_partial('\x07\x1b\\')
    else:
        print_partial('\x07')

def print_image(image_file_name=None, data=None, width=None, height=None):
    terminal = os.environ.get('TERM', '')
    print_osc(terminal)
    print_partial('1337;File=')
    args = []
    if image_file_name:
        b64_file_name = base64.b64encode(image_file_name.encode('ascii')).decode('ascii')
        args.append('name=' + b64_file_name)
        with open(image_file_name, 'rb') as image_file:
            b64_data = base64.b64encode(image_file.read()).decode('ascii')
    elif data:
        b64_data = base64.b64encode(data).decode('ascii')
    else:
        raise ValueError('Expected image_file_name or data')
    args.append('size=' + str(len(b64_data)))
    if width is not None:
        args.append('width=' + str(width))
    if height is not None:
        args.append('height=' + str(height))
    args.append('inline=1')
    print_partial(';'.join(args))
    print_partial(':')
    print_partial(b64_data)
    print_st(terminal)

def show_help():
    print('Usage: imgcat filename ...')
    print('   or: cat filename | python imgcat.py -')
    exit()

def print_partial(msg):
    print(msg, end='')

def _read_binary_stdin():
    PY3 = sys.version_info >= (3, 0)
    if PY3:
        source = sys.stdin.buffer
    else:
        if sys.platform == 'win32':
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        source = sys.stdin
    return source.read()

def main():
    filename = None
    data = None
    if len(sys.argv) != 2:
        show_help()
    if sys.argv[1] != '-':
        filename = sys.argv[1]
        print_image(image_file_name=filename)
    else:
        data = _read_binary_stdin()
        print_image(data=data)
    if not filename and (not data):
        show_help()
if __name__ == '__main__':
    main()