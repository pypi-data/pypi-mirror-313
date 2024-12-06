from filtertree import __version__, filtertree
import subprocess
import argparse


def main():
    args = parse_arguments()
    if args.script:
        def cmdfunc(src_file_path, dest_file_path):
            src = str(src_file_path)
            dest = str(dest_file_path)
            oneliner = args.script.replace("$1", src).replace("$2", dest)
            subprocess.call(oneliner, shell=True)
    elif args.cmd:
        def cmdfunc(src_file_path, dest_file_path):
            subprocess.call(f"{args.cmd} {src_file_path} {dest_file_path}", shell=True)
    else:
        cmdfunc = _echo
    filtertree(cmdfunc, args.src_dir, args.dest_dir)


def _echo(src_file_path, dest_file_path):
    cmd = f"echo FROM {str(src_file_path)} TO {str(dest_file_path)}"
    subprocess.call(cmd, shell=True)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Apply filter to directory tree."
    )
    parser.add_argument(
        "src_dir",
        metavar="SRCDIR",
        action="store",
        help="source directory"
    )
    parser.add_argument(
        "dest_dir",
        metavar="DESTDIR",
        action="store",
        help="destination directory"
    )
    parser.add_argument(
        "cmd",
        metavar="CMD",
        action="store",
        nargs="?",
        default=None,
        help="command"
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"v{__version__}",
        help="show version and exit"
    )
    parser.add_argument(
        "-c",
        metavar="SCRIPT",
        action="store",
        dest="script",
        help="one line script"
    )
    args = parser.parse_args()
    return args
