# Copyright (c) 2021-2024, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

"""This is the command line interface to the datsets module of scene_synthesizer."""

# Standard Library
import argparse
import logging
import os
import pprint
import shutil
import sys

# SRL
from scene_synthesizer import __version__

# Local Folder
from . import datasets

_logger = logging.getLogger(__name__)


def colored(r, g, b, text):
    """Return colored text for printing to console.

    Args:
        r (int): Red value. Between 0 and 255.
        g (int): Green value. Between 0 and 255.
        b (int): Blue value. Between 0 and 255.
        text (str): Text.

    Returns:
        str: Colored text.
    """
    return f"\033[38;2;{r};{g};{b}m{text} \033[0m"


def cmd_list(args):
    """Subcommand list."""
    for m in datasets.list_datasets():
        d = datasets.load_dataset(m)
        print(m)
        print(
            f"\t{d.root_dir} "
            f"{colored(255, 0, 0, ' [N/A]') if not os.path.exists(d.root_dir) else ''}"
        )
        print(f"\t{len(d.get_filenames())} files")
        print(f"\t{len(d.get_categories())} categories")


def cmd_show(args):
    """Subcommand show."""
    if args.dataset_name not in datasets.cfg_dict:
        raise ValueError(f"Unknown dataset: '{args.dataset_name}'")

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(datasets.cfg_dict[args.dataset_name])


def cmd_config(args):
    """Subcommand config."""
    if args.dataset_name not in datasets.cfg_dict:
        raise ValueError(f"Unknown dataset: '{args.dataset_name}'")

    updated_cfg = datasets.cfg_dict[args.dataset_name].copy()
    updated_cfg.update({args.key: args.value})

    new_cfg = datasets.cfg.copy()
    index = list([x["name"] for x in new_cfg]).index(args.dataset_name)
    new_cfg[index] = updated_cfg

    datasets.write_cfg(new_cfg)


def cmd_reset(args):
    """Subcommand reset."""
    if query_yes_no(
        f"Do you want to overwrite {datasets.cfg_fname} with default values?",
        default="no",
        args=args,
    ):
        shutil.copyfile(datasets.cfg_fname_default, datasets.cfg_fname)


def cmd_wtf(args):
    """Subcommand wtf."""
    for m in datasets.list_datasets():
        print("\nChecking dataset '%s'..." % (m,))
        d = datasets.load_dataset(m)
        print(f"\tparser: {d.__class__.__name__}")

        help_msg = (
            f" --> Modify root_dir directly in {datasets.cfg_fname} or via `scene_synth_datasets"
            f" '{m}' root_dir <directory where dataset was extracted>`"
        )
        if not os.path.exists(d.root_dir):
            colored_help_msg = colored(255, 0, 0, "DOES NOT EXIST!") + help_msg
        else:
            colored_help_msg = colored(0, 255, 0, "OK")
        full_msg = f"\troot_dir ('{d.root_dir}'): {colored_help_msg}"
        print(full_msg)
        if isinstance(d, datasets.Dataset) and "file_globber" in datasets.cfg_dict[m]:
            print(
                f"\troot_dir + file_globber ('{datasets.cfg_dict[m]['file_globber']}'):"
                f" {os.path.join(d.root_dir, datasets.cfg_dict[m]['file_globber'])}"
            )

        num_files = len(d.get_filenames())
        print(
            "\tNumber of files found: "
            f"{colored(255, 0, 0, num_files) if num_files == 0 else colored(0, 255, 0, num_files)}"
        )
        num_categories = len(d.get_categories())

        if num_categories == 0:
            colored_msg = colored(255, 0, 0, num_categories)
        else:
            colored_msg = colored(0, 255, 0, num_categories)
        print(f"\tNumber of categories found: {colored_msg}")

        if num_files == 0 and "url" in datasets.cfg_dict[m]:
            print(f"\tDid you download this dataset? --> {datasets.cfg_dict[m]['url']}")


def query_yes_no(question, default="yes", args=None):
    """Ask a yes/no question via input() and return their answer.

    Args:
        question (str): Text presented to the user.
        default (str, optional): The presumed answer if the user just hits <Enter>. It must be "yes"
            (the default), "no" or None (meaning an answer is required of the user). Defaults to
            "yes".
        args (:obj:`argparse.Namespace`, optional): Command line parameters. If it contains 'yes'
            function will return True. Defaults to None.

    Raises:
        ValueError: Invalid default answer.

    Returns:
        bool: True for "yes" or False for "no".
    """
    if args and args.yes:
        return True

    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def make_parser():
    """Create command line parser.

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.ArgumentParser`: command line parser
    """
    parser = argparse.ArgumentParser(
        description=(
            "Configure and view status of datasets. "
            f"All information can also be directly edited in the config file: {datasets.cfg_fname}"
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version="scene_synthesizer.datasets {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-y",
        "--yes",
        dest="yes",
        help="Answer all prompts with yes.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    subparsers = parser.add_subparsers(dest="command")
    list_parser = subparsers.add_parser("list", help="Lists all available datasets.")
    list_parser.set_defaults(func=cmd_list)
    show_parser = subparsers.add_parser("show", help="Shows information about a specific dataset.")
    show_parser.add_argument(
        dest="dataset_name", type=str, metavar="DATASET", help="The name of the dataset"
    )
    show_parser.set_defaults(func=cmd_show)
    config_parser = subparsers.add_parser(
        "config", help="Configures information about a specific dataset."
    )
    config_parser.add_argument(
        dest="dataset_name", type=str, metavar="DATASET", help="The name of the dataset"
    )
    config_parser.add_argument(
        dest="key",
        type=str,
        metavar="KEY",
        help="The key of the dict entry to be edited.",
    )
    config_parser.add_argument(
        dest="value",
        type=str,
        metavar="VALUE",
        help="The value of the dict entry to be edited.",
    )
    config_parser.set_defaults(func=cmd_config)
    reset_parser = subparsers.add_parser("reset", help="Resets the configuration file.")
    reset_parser.set_defaults(func=cmd_reset)
    wtf_parser = subparsers.add_parser(
        "wtf", help="Shows potential problems with the current configuration file."
    )
    wtf_parser.set_defaults(func=cmd_wtf)

    return parser


def setup_logging(loglevel):
    """Setup basic logging.

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Main entry point allowing external calls.

    Args:
      args ([str]): command line parameter list
    """
    parser = make_parser()
    args = parser.parse_args(args)

    setup_logging(args.loglevel)
    _logger.debug("Starting...")
    if hasattr(args, "func"):
        if args.func:
            args.func(args)
    else:
        # program was called without any arguments
        parser.print_help()
    _logger.info("Finshed")


def run():
    """Entry point for console_scripts."""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
