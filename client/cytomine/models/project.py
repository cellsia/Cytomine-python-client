# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2015. Authors: see NOTICE file.
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

__author__ = "Stévens Benjamin <b.stevens@ulg.ac.be>"
__contributors__ = ["Marée Raphaël <raphael.maree@ulg.ac.be>", "Rollus Loïc <lrollus@ulg.ac.be"]
__copyright__ = "Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/"

from collection import Collection
from model import Model


class Project(Model):
    def __init__(self, name=None, id_ontology=None, **attributes):
        super(Project, self).__init__()
        self.name = name
        self.ontology = id_ontology
        self.ontologyName = None
        self.discipline = None
        self.blindMode = None
        self.disciplineName = None
        self.numberOfSlides = None
        self.numberOfImages = None
        self.numberOfAnnotations = None
        self.numberOfJobAnnotations = None
        self.retrievalProjects = None
        self.numberOfReviewedAnnotations = None
        self.retrievalDisable = None
        self.retrievalAllOntology = None
        self.isClosed = None
        self.isReadOnly = None
        self.hideUsersLayers = None
        self.hideAdminsLayers = None
        self.populate(attributes)


class ProjectCollection(Collection):
    def __init__(self, filters=None, max=0, offset=0, **parameters):
        super(ProjectCollection, self).__init__(Project, filters, max, offset)
        self._allowed_filters = ["user", "software", "ontology"]
        self.set_parameters(parameters)


class Discipline(Model):
    def __init__(self, name=None, **attributes):
        super(Discipline, self).__init__()
        self.name = name
        self.populate(attributes)


class DisciplineCollection(Collection):
    def __init__(self, filters=None, max=0, offset=0, **parameters):
        super(DisciplineCollection, self).__init__(Discipline, filters, max, offset)
        self.set_parameters(parameters)
