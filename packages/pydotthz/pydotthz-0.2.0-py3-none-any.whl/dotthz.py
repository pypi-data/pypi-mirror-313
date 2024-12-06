import h5py
from dataclasses import dataclass, field
from typing import Dict
import numpy as np
from pathlib import Path


@dataclass
class DotthzMetaData:
    user: str = ""
    email: str = ""
    orcid: str = ""
    institution: str = ""
    description: str = ""
    md: Dict[str, str] = field(default_factory=dict)
    version: str = "1.00"
    mode: str = ""
    instrument: str = ""
    time: str = ""
    date: str = ""

    def add_field(self, key, value):
        self.md[key] = value


@dataclass
class DotthzMeasurement:
    datasets: Dict[str, np.ndarray] = field(default_factory=dict)
    meta_data: DotthzMetaData = field(default_factory=DotthzMetaData)


class DotthzFile:
    def __init__(self, name, mode="r", driver=None, libver=None, userblock_size=None, swmr=False,
                 rdcc_nslots=None, rdcc_nbytes=None, rdcc_w0=None, track_order=None,
                 fs_strategy=None, fs_persist=False, fs_threshold=1, fs_page_size=None,
                 page_buf_size=None, min_meta_keep=0, min_raw_keep=0, locking=None,
                 alignment_threshold=1, alignment_interval=1, meta_block_size=None, **kwds):
        self.groups = {}
        self.file = h5py.File(name, mode, driver=driver, libver=libver, userblock_size=userblock_size, swmr=swmr,
                              rdcc_nslots=rdcc_nslots,
                              rdcc_nbytes=rdcc_nbytes, rdcc_w0=rdcc_w0, track_order=track_order,
                              fs_strategy=fs_strategy, fs_persist=fs_persist, fs_threshold=fs_threshold,
                              fs_page_size=fs_page_size,
                              page_buf_size=page_buf_size, min_meta_keep=min_meta_keep, min_raw_keep=min_raw_keep,
                              locking=locking, alignment_threshold=alignment_threshold,
                              alignment_interval=alignment_interval, meta_block_size=meta_block_size, **kwds)

        if "r" in mode or "a" in mode:
            self._load()

    def __enter__(self):
        """Enable the use of the `with` statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close any resources if applicable."""
        if self.file is not None:
            self.file.close()
            self.file = None


    def _load(self):
        groups = {}
        for group_name, group in self.file.items():
            measurement = DotthzMeasurement()

            # Load datasets
            if "dsDescription" in group.attrs:
                ds_description_attr = group.attrs["dsDescription"]
                if isinstance(ds_description_attr, np.ndarray):
                    ds_description_str = ds_description_attr[0] if ds_description_attr.size == 1 else ", ".join(
                        map(str, ds_description_attr))
                else:
                    ds_description_str = ds_description_attr

                ds_descriptions = [ds.strip() for ds in ds_description_str.split(",")] if isinstance(ds_description_str,
                                                                                                     str) else []
                for i, desc in enumerate(ds_descriptions):
                    dataset_name = f"ds{i + 1}"
                    if dataset_name in group:
                        measurement.datasets[desc] = group[dataset_name][...]

            # Load metadata attributes
            for attr in ["description", "date", "instrument", "mode", "time"]:
                if attr in group.attrs:
                    setattr(measurement.meta_data, attr, group.attrs[attr])

            if "thzVer" in group.attrs:
                measurement.meta_data.version = group.attrs["thzVer"][0] if isinstance(group.attrs["thzVer"], list) else \
                    group.attrs["thzVer"]

            if "user" in group.attrs:
                user_info = group.attrs["user"].split("/")
                fields = ["orcid", "user", "email", "institution"]
                for i, part in enumerate(user_info):
                    if i < len(fields):
                        setattr(measurement.meta_data, fields[i], part)

            if "mdDescription" in group.attrs:
                md_description_attr = group.attrs["mdDescription"]
                if isinstance(md_description_attr, np.ndarray):
                    md_description_str = md_description_attr[0] if md_description_attr.size == 1 else ", ".join(
                        map(str, md_description_attr))
                else:
                    md_description_str = md_description_attr

                md_descriptions = [md.strip() for md in md_description_str.split(",")] if isinstance(md_description_str,
                                                                                                     str) else []
                for i, desc in enumerate(md_descriptions):
                    md_name = f"md{i + 1}"
                    if md_name in group.attrs:
                        measurement.meta_data.md[desc] = str(group.attrs[md_name])

            groups[group_name] = measurement

        self.groups.update(groups)

    def get_measurements(self):
        return self.groups

    def get_measurement_names(self):
        return self.groups.keys()

    def get_measurement(self, group_name):
        return self.groups.get(group_name)

    def write_measurement(self, group_name: str, measurement: DotthzMeasurement):
        group = self.file.create_group(group_name)

        # Write dataset descriptions
        ds_descriptions = ", ".join(measurement.datasets.keys())
        group.attrs["dsDescription"] = ds_descriptions

        # Write datasets
        for i, (name, dataset) in enumerate(measurement.datasets.items()):
            ds_name = f"ds{i + 1}"
            group.create_dataset(ds_name, data=dataset)

        # Write metadata
        for attr_name, attr_value in measurement.meta_data.__dict__.items():
            if attr_name == "md":
                # Write md descriptions as an attribute
                md_descriptions = ", ".join(measurement.meta_data.md.keys())
                group.attrs["mdDescription"] = md_descriptions
                for i, (md_key, md_value) in enumerate(measurement.meta_data.md.items()):
                    md_name = f"md{i + 1}"
                    try:
                        # Attempt to save as float if possible
                        group.attrs[md_name] = float(md_value)
                        print(md_name, group.attrs[md_name])
                    except ValueError:
                        group.attrs[md_name] = md_value
            elif attr_name == "version":
                group.attrs["thzVer"] = measurement.meta_data.version

            elif attr_name in ["orcid", "user", "email", "institution"]:
                continue
            else:
                if attr_value:  # Only write non-empty attributes
                    group.attrs[attr_name] = attr_value

        # Write user metadata in the format "ORCID/user/email/institution"
        user_info = "/".join([
            measurement.meta_data.orcid,
            measurement.meta_data.user,
            measurement.meta_data.email,
            measurement.meta_data.institution
        ])
        group.attrs["user"] = user_info
