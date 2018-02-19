# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2018. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "Rubens Ulysse <urubens@uliege.be>"
__contributors__ = ["Marée Raphaël <raphael.maree@uliege.be>", "Mormont Romain <r.mormont@uliege.be>"]
__copyright__ = "Copyright 2010-2018 University of Liège, Belgium, http://www.cytomine.be/"

from cytomine.models.collection import Collection
from cytomine.models.model import Model


class Storage(Model):
    def __init__(self, name=None, **attributes):
        super(Storage, self).__init__()
        self.name = name
        self.basePath = None
        self.user = None
        self.populate(attributes)


class StorageCollection(Collection):
    def __init__(self, filters=None, max=0, offset=0, **parameters):
        super(StorageCollection, self).__init__(Storage, filters, max, offset)
        self.set_parameters(parameters)


class UploadedFile(Model):
    def __init__(self, **attributes):
        super(UploadedFile, self).__init__()
        self.user = None
        self.projects = None
        self.storages = None
        self.filename = None
        self.originalFilename = None
        self.ext = None
        self.size = None
        self.path = None
        self.status = None
        self.populate(attributes)

    def __str__(self):
        return "[{}] {} : {}".format(self.callback_identifier, self.id, self.filename)


class UploadedFileCollection(Collection):
    def __init__(self, filters=None, max=0, offset=0, **parameters):
        super(UploadedFileCollection, self).__init__(UploadedFile, filters, max, offset)
        self.set_parameters(parameters)