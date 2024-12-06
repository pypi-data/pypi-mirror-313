import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('--doctor', default=False, action='store_true', required=False)
args = parser.parse_args()

def main():
    if args.doctor:
        import nexfort
        print('path:', nexfort.__path__)
        print('version:', nexfort.__version__)
        print('build torch version:', '2.4.0+cu121')
if __name__ == '__main__':
    main()