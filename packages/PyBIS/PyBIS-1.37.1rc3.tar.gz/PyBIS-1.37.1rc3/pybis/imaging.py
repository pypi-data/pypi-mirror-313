#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright ETH 2023 - 2024 Zürich, Scientific IT Services
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""
imaging.py

Work with Openbis Imaging technology with Python.

"""
import abc
import json
import base64
import threading



class AtomicIncrementer:
    def __init__(self, value=0):
        self._value = int(value)
        self._lock = threading.Lock()

    def inc(self, d=1):
        with self._lock:
            self._value += int(d)
            return self._value


class AbstractImagingClass(metaclass=abc.ABCMeta):
    def to_json(self):

        c = AtomicIncrementer()

        def dictionary_creator(x):
            dictionary = x.__dict__
            val = c.inc()
            dictionary['@id'] = val
            return dictionary

        return json.dumps(self, default=dictionary_creator, sort_keys=True, indent=4)

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__)


class AbstractImagingRequest(AbstractImagingClass, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _validate_data(self):
        return


class ImagingDataSetPreview(AbstractImagingRequest):
    config: dict
    format: str
    # bytes: str | None
    width: int
    height: int
    index: int
    show: bool
    metadata: dict
    comment: str
    tags: list

    def __init__(self, preview_format, config=None, metadata=None, index=0, comment="", tags=[]):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetPreview"
        self.bytes = None
        self.format = preview_format
        self.config = config if config is not None else dict()
        self.metadata = metadata if metadata is not None else dict()
        self.index = index
        self.comment = comment
        self.tags = tags
        self._validate_data()

    def set_preview_image_bytes(self, width, height, bytes):
        self.width = width
        self.height = height
        self.bytes = bytes

    def _validate_data(self):
        assert self.format is not None, "Format can not be null"

    def save_to_file(self, file_path):
        assert self.bytes is not None, "There is no image information!"
        img_data = bytearray(self.bytes, encoding='utf-8')
        with open(file_path, "wb") as fh:
            fh.write(base64.decodebytes(img_data))

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        preview = cls('', None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            preview.__dict__[prop] = attribute
        return preview

class ImagingDataSetExportConfig(AbstractImagingClass):
    archiveFormat: str
    imageFormat: str
    resolution: str
    include: list

    def __init__(self, archive_format, image_format, resolution, include=None):
        if include is None:
            include = ["IMAGE", "RAW_DATA"]
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetExportConfig"
        self.imageFormat = image_format
        self.archiveFormat = archive_format
        if resolution is None:
            resolution = "original"
        self.resolution = resolution
        self.include = include
        self._validate_data()

    def _validate_data(self):
        assert self.imageFormat is not None, "image format can not be null"
        assert self.archiveFormat is not None, "image format can not be null"

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        preview = cls(None, None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            preview.__dict__[prop] = attribute
        return preview



class ImagingDataSetExport(AbstractImagingRequest):
    config: ImagingDataSetExportConfig
    metadata: dict

    def __init__(self, config, metadata=None):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetExport"
        self.config = config
        self.metadata = metadata if metadata is not None else dict()
        self._validate_data()

    def _validate_data(self):
        assert self.config is not None, "Config can not be null"



class ImagingDataSetMultiExport(AbstractImagingRequest):
    permId: str
    imageIndex: int
    previewIndex: int
    config: ImagingDataSetExportConfig
    metadata: dict

    def __init__(self, permId, imageIndex, previewIndex, config, metadata=None):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetMultiExport"
        self.permId = permId
        self.imageIndex = imageIndex
        self.previewIndex = previewIndex
        self.config = config
        self.metadata = metadata if metadata is not None else dict()
        self._validate_data()

    def _validate_data(self):
        assert self.permId is not None, "PermId can not be null"
        assert self.imageIndex is not None, "imageIndex can not be null"
        assert self.previewIndex is not None, "previewIndex can not be null"


class ImagingDataSetControlVisibility(AbstractImagingClass):
    label: str
    values: list[str]
    range: list[str]
    unit: str

    def __init__(self, label: str, values: list[str], values_range: list[str], unit: str = None):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetControlVisibility"
        self.label = label
        self.values = values
        self.range = values_range
        self.unit = unit

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        control = cls(None, None, None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            control.__dict__[prop] = attribute
        return control


class ImagingDataSetControl(AbstractImagingClass):
    label: str
    section: str
    type: str
    values: list[str]
    unit: str
    range: list[str]
    multiselect: bool
    playable: bool
    speeds: list[int]
    visibility: list[ImagingDataSetControlVisibility]
    metadata: dict

    def __init__(self, label: str, control_type: str, section: str = None, values: list[str] = None,
                 unit: str = None, values_range: list[str] = None, multiselect: bool = None,
                 playable: bool = False, speeds: list[int] = None,
                 visibility: list[ImagingDataSetControlVisibility] = None, metadata: dict = None):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetControl"
        self.label = label
        self.type = control_type
        self.section = section
        self.unit = unit
        if control_type.lower() in ["slider", "range"]:
            self.range = values_range
        elif control_type.lower() in ["dropdown", "colormap"]:
            self.values = values
            if multiselect is None:
                self.multiselect = False
            else:
                self.multiselect = multiselect

        if playable is True:
            self.playable = True
            self.speeds = speeds
        self.visibility = visibility
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        control = cls(None, "", None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            if prop == 'visibility' and attribute is not None:
                attribute = [ImagingDataSetControlVisibility.from_dict(visibility) for visibility in attribute]
            control.__dict__[prop] = attribute
        return control


class ImagingDataSetConfig(AbstractImagingClass):
    adaptor: str
    version: float
    speeds: list[int]
    resolutions: list[str]
    playable: bool
    exports: list[ImagingDataSetControl]
    inputs: list[ImagingDataSetControl]
    metadata: dict

    def __init__(self, adaptor: str, version: float, resolutions: list[str], playable: bool,
                 speeds: list[int] = None, exports: list[ImagingDataSetControl] = None,
                 inputs: list[ImagingDataSetControl] = None, metadata: dict = None):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetConfig"
        self.adaptor = adaptor
        self.version = version
        self.resolutions = resolutions
        self.playable = playable
        if playable:
            self.speeds = speeds
        self.exports = exports
        self.inputs = inputs
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        config = cls(None, None, None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            if prop in ['exports', 'inputs'] and attribute is not None:
                attribute = [ImagingDataSetControl.from_dict(control) for control in attribute]
            config.__dict__[prop] = attribute
        return config


class ImagingDataSetImage(AbstractImagingClass):
    config: ImagingDataSetConfig
    previews: list[ImagingDataSetPreview]
    image_config: dict
    index: int
    metadata: dict

    def __init__(self, config: ImagingDataSetConfig, image_config=None, previews=None, metadata=None, index=0):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetImage"
        assert config is not None, "Config must not be None!"
        self.config = config
        self.image_config = image_config if image_config is not None else dict()
        self.previews = previews if previews is not None else [ImagingDataSetPreview("png")]
        self.metadata = metadata if metadata is not None else dict()
        self.index = index if index is not None else 0
        assert isinstance(self.previews, list), "Previews must be a list!"

    def add_preview(self, preview):
        self.previews += [preview]

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if "@id" in data:
            del data["@id"]
        config = ImagingDataSetConfig.from_dict(data.get('config'))
        image = cls(config,None, None, None)
        for prop in cls.__annotations__.keys():
            attribute = data.get(prop)
            if prop == 'previews' and attribute is not None:
                attribute = [ImagingDataSetPreview.from_dict(preview) for preview in attribute]
            image.__dict__[prop] = attribute
        return image


class ImagingDataSetPropertyConfig(AbstractImagingClass):
    images: list[ImagingDataSetImage]

    def __init__(self, images: list[ImagingDataSetImage]):
        self.__dict__["@type"] = "imaging.dto.ImagingDataSetPropertyConfig"
        self.images = images if images is not None else []

    @classmethod
    def from_dict(cls, data: dict):
        assert data is not None and any(data), "There is no property config found!"
        if "@id" in data:
            del data["@id"]
        attr = data.get('images')
        images = [ImagingDataSetImage.from_dict(image) for image in attr] if attr is not None else None
        return cls(images)

    def add_image(self, image: ImagingDataSetImage):
        if self.images is None:
            self.images = []
        self.images += [image]