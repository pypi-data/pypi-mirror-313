# Copyright (c) 2021-2024, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

# Standard Library
import glob
import json
import os
import re
from pathlib import Path

# Third Party
import yaml
from config_path import ConfigPath

cfg_path = ConfigPath("datasets", "scene-synth", ".yaml")
cfg_path_dir = cfg_path.readFolderPath(mkdir=True)

cfg_fname = cfg_path_dir / "config.yaml"
cfg_fname_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default_config.yaml")

if not cfg_fname.exists():
    # Standard Library
    from shutil import copyfile

    copyfile(cfg_fname_default, cfg_fname)


if "SCENE_SYNTH_DATASETS_CONFIG" in os.environ:
    cfg_fname = Path(
        os.path.expanduser(os.path.expandvars(os.environ["SCENE_SYNTH_DATASETS_CONFIG"]))
    )

    if not cfg_fname.exists():
        raise ValueError(
            f"Environment variable SCENE_SYNTH_DATASETS_CONFIG={cfg_fname} points to a non-existing"
            " file. Either set properly or unset."
        )

    cfg_path_dir = cfg_fname.parent


cfg = yaml.load(open(cfg_fname, "r"), Loader=yaml.FullLoader)
cfg_dict = {x["name"]: x for x in cfg}


def write_cfg(cfg):
    """Write config."""
    with open(cfg_fname, "w") as file:
        yaml.dump(cfg, file)


registered_dataset_classes = {}


def register(cls):
    """Register class decorator."""
    registered_dataset_classes[cls.__name__] = cls
    return cls


def splitall(path):
    """Split all path string helper function."""
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


@register
class Dataset(object):
    """Dataset class."""

    def __init__(self, name, root_dir, scale=1.0, file_globber=None, only_volumes=False, **kwargs):
        """Initialize a new `Dataset` object."""
        if root_dir is None:
            root_dir = ""

        self._root_dir = root_dir
        self._scale = scale
        self._name = name
        self._attributes = {}

        self._metadata = kwargs

        self._setup()

        self._all_filenames, self._filenames = self._setup_filenames(
            file_globber=file_globber,
            only_volumes=only_volumes,
        )

    @property
    def name(self):
        """Get the `name` attribute."""
        return self._name

    @property
    def root_dir(self):
        """Get the `root_dir` attribute."""
        return self._root_dir

    @property
    def scale(self):
        """Get the `scale` attribute."""
        return self._scale

    def _setup(self):
        pass

    def _get_categories(self, filename, file_globber):
        try:
            category_index = file_globber.split("/").index("*") - len(file_globber.split("/"))
        except ValueError:
            category_index = -1
        return [splitall(filename)[category_index]]

    def _setup_filenames(self, file_globber, only_volumes):
        all_filenames_raw = glob.glob(os.path.join(self._root_dir, file_globber))

        # print("All filenames:", all_filenames_raw)

        all_filenames = []
        filenames = {}
        for f in all_filenames_raw:
            if only_volumes:
                # Third Party
                import trimesh

                m = trimesh.load(f)
                if not m.is_volume:
                    continue

            all_filenames.append(f)
            cats = self._get_categories(filename=f, file_globber=file_globber)

            for cat in cats:
                if cat in filenames.keys():
                    filenames[cat].append(f)
                else:
                    filenames[cat] = [f]

        # print("Categories:", list(filenames.keys()))
        # print("Number of files:", len(all_filenames))
        return all_filenames, filenames

    def get_categories(self):
        """Returns a list of all categories/classes that the files in this dataset belong to.

        Returns:
            list[str]: Categories of elements in this dataset.
        """
        return sorted(list(self._filenames.keys()))

    def get_filenames(self, categories=None, filter_fn=None):
        """Get filenames in dataset.

        Return all elements in the dataset that belong to the queried category/ies and satisfy
        the filter function.

        Args:
            categories (str or list[str] or re.Pattern, optional): Query category/ies. None means
                any category is valid. Defaults to None.
            filter_fn (lambda, optional): A function to further filter the results. Defaults to
                None.

        Returns:
            list[str]: File names.
        """
        if categories is None:
            # Ignore category filter
            tmp = self._all_filenames
        else:
            if isinstance(categories, str):
                categories = [categories]
            elif isinstance(categories, re.Pattern):
                categories = list(filter(categories.match, self.get_categories()))

            tmp = []
            for cat in categories:
                if cat not in self._filenames:
                    raise ValueError(
                        f"Invalid category '{cat}' for dataset '{self.name}'. "
                        f"Valid categories: {self.get_categories()}"
                    )
                tmp.extend(self._filenames[cat])

        if filter_fn:
            tmp = list(filter(filter_fn, tmp))

        return tmp

    def get_filename(self, categories=None, index=0, pattern=None):
        """Returns the index-th element of the datasets that matches the queried category/ies.

        Args:
            categories (str or list[str] or re.Pattern, optional): Query category/ies. None means
                any category is valid. Defaults to None.
            index (int, optional): The index of the requested element. With overflow protection.
                Defaults to 0.
            pattern (str or re.Pattern, optional): Substring or regular expression of the returned
                file name. Defaults to None.

        Returns:
            str: File name of an element in the dataset that match the query category/ies and
                pattern.
        """
        fnames = self.get_filenames(categories=categories)
        if pattern is not None:
            if isinstance(pattern, str):
                fnames = [fname for fname in fnames if pattern in fname]
            elif isinstance(pattern, re.Pattern):
                fnames = list(filter(pattern.match, fnames))
            else:
                raise TypeError("Argument 'pattern' needs to be of type str or re.Pattern")
        if len(fnames) == 0:
            raise ValueError("No filename matches the specified category (and pattern).")

        return fnames[index % len(fnames)]

    def get_metadata(self, fname):
        """Returns metadata of an element of the dataset.

        Args:
            fname (str): File name of the dataset element.

        Returns:
            dict: Metadata of the dataset element.
        """
        return self._attributes[fname]


@register
class PartNetMobility(Dataset):
    def _get_categories(self, filename, file_globber):
        dirname = os.path.dirname(filename)
        metadata = json.load(open(os.path.join(dirname, "meta.json"), "r"))
        return [metadata["model_cat"]]

def list_datasets():
    """Return a list of all available datasets.

    Returns:
        list[str]: Names of all available datasets.
    """
    return list(cfg_dict.keys())


def load_dataset(name):
    """Factory method for Dataset objects.

    Args:
        name (str): Name of the requested dataset.

    Raises:
        ValueError: Dataset name does not exist.
        ValueError: Dataset cannot be instantiated.

    Returns:
        :obj:`datasets.Dataset`: Dataset.
    """
    available_datasets = list_datasets()
    if name not in available_datasets:
        raise ValueError(
            f"Dataset {name} cannot be loaded. See list_datasets() for available datasets."
        )

    if cfg_dict[name]["parser"] not in registered_dataset_classes:
        raise ValueError(
            f"Dataset '{name}' cannot be instantiated. ",
            f"No parser '{cfg_dict[name]['parser']}' registered: {registered_dataset_classes}.",
        )

    return registered_dataset_classes[cfg_dict[name]["parser"]](**cfg_dict[name])
