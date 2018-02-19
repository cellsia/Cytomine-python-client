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

import os
import re

from cytomine.cytomine import Cytomine
from cytomine.models.collection import Collection
from cytomine.models.model import Model


class Annotation(Model):
    def __init__(self, location=None, id_image=None, id_terms=None, id_project=None, **attributes):
        super(Annotation, self).__init__()
        self.location = location
        self.image = id_image
        self.project = id_project
        self.term = id_terms
        self.geometryCompression = None
        self.area = None
        self.areaUnit = None
        self.perimeter = None
        self.perimeterUnit = None
        self.cropURL = None

        self.populate(attributes)

    def __str__(self):
        return "[{}] {}".format(self.callback_identifier, self.id)

    def dump(self, dest_pattern="{id}.jpg", override=True, mask=False, alpha=False, bits=8,
             zoom=None, max_size=None, increase_area=None, contrast=None, gamma=None, colormap=None, inverse=None):
        if self.id is None:
            raise ValueError("Cannot dump an annotation with no ID.")

        pattern = re.compile("{(.*?)}")
        dest_pattern = re.sub(pattern, lambda m: str(getattr(self, str(m.group(0))[1:-1], "_")), dest_pattern)

        destination = os.path.dirname(dest_pattern)
        filename, extension = os.path.splitext(os.path.basename(dest_pattern))

        if extension not in ("jpg", "png", "tif", "tiff"):
            extension = "jpg"

        if not os.path.exists(destination):
            os.makedirs(destination)

        parameters = {
            "zoom": zoom,
            "maxSize": max_size,
            "increaseArea": increase_area,
            "contrast": contrast,
            "gamma": gamma,
            "colormap": colormap,
            "inverse": inverse,
            "bits": bits
        }

        if mask and alpha:
            image = "alphamask"
            if extension == "jpg":
                extension = "png"
        elif mask:
            image = "mask"
        else:
            image = "crop"

        file_path = os.path.join(destination, "{}.{}".format(filename, extension))

        url = self.cropURL.replace("crop.jpg", "{}.{}".format(image, extension))
        result = Cytomine.get_instance().download_file(url, file_path, override, parameters)
        if result:
            self.filename = file_path
        return result

    """
    Deprecated functions. Still here for backwards compatibility.
    """
    get_annotation_crop_url = None
    get_annotation_crop_tiled_translated = None
    get_annotation_alpha_crop_url = None
    get_annotation_mask_url = None
    # def get_annotation_crop_tiled_translated(self,minx,maxx,miny,maxy,id_image,image_height,tile_size,translate):
    #     #original annotation bounding box width & height
    #     w_width=maxx-minx
    #     w_height=maxy-miny
    #     if translate:
    #         #maximum shift is predefined, it is determined by half of the size of the object such
    # that at least half is still included
    #         translate_x = random.randrange(-w_width/2, w_width/2)
    #         translate_y = random.randrange(-w_height/2, w_height/2)
    #         print "translate_x: %d translate_y: %d" %(translate_x,translate_y)
    #         minx = minx + translate_x
    #         maxx = maxx + translate_x
    #         miny = miny + translate_y
    #         maxy = maxy + translate_y
    #
    #     #we construct new coordinates (for dimension(s) < tile_size) so that we finally have image dimensions
    #  at least of tile_size
    #     #e.g. tile_size=512, if annotation 400x689 it becomes 512x689, if annotation 234x123 it becomes 512x512
    #     if w_width < tile_size:
    #         displace_x = tile_size - w_width
    #         minx = minx - displace_x/2
    #         maxx = minx + tile_size
    #     if w_height < tile_size:
    #         displace_y = tile_size - w_height
    #         miny = miny - displace_y/2
    #         maxy = miny + tile_size
    #     windowURL = "imageinstance/%d/window-%d-%d-%d-%d.jpg" %(id_image,minx,image_height-maxy,maxx-minx,maxy-miny)
    #
    #     return windowURL


class AnnotationCollection(Collection):
    def __init__(self, filters=None, max=0, offset=0, **parameters):
        super(AnnotationCollection, self).__init__(Annotation, filters, max, offset)
        self._allowed_filters = []

        self.showBasic = True
        self.showMeta = False
        self.showWKT = False
        self.showGIS = False
        self.showTerm = False
        self.showAlgo = False
        self.showUser = False
        self.showImage = False
        self.reviewed = False
        self.noTerm = False
        self.noAlgoTerm = False
        self.multipleTerm = False

        self.project = None

        self.job = None
        self.user = None
        self.users = None

        self.image = None
        self.images = None

        self.term = None
        self.terms = None
        self.suggestedTerm = None
        self.userForTermAlgo = None
        self.jobForTermAlgo = None

        self.bbox = None
        self.bboxAnnotation = None
        self.baseAnnotation = None
        self.maxDistanceBaseAnnotation = None

        self.included = False
        self.annotation = None

        self.set_parameters(parameters)

    def uri(self):
        if self.included:
            self.add_filter("imageinstance", self.image)
        uri = super(AnnotationCollection, self).uri()
        if self.included:
            return uri.replace(".json", "/included.json")

        return uri

    def save(self):
        return Cytomine.get_instance().post(self)

    def to_json(self, **dump_parameters):
        return "[{}]".format(",".join([d.to_json() for d in self._data]))


class AnnotationTerm(Model):
    def __init__(self, id_annotation=None, id_term=None, **attributes):
        super(AnnotationTerm, self).__init__()
        self.userannotation = id_annotation
        self.term = id_term
        self.user = None
        self.populate(attributes)

    def uri(self):
        if self.is_new():
            return "annotation/{}/term.json".format(self.userannotation)
        else:
            return "annotation/{}/term/{}.json".format(self.userannotation, self.term)

    def __str__(self):
        return "[{}] Annotation {} - Term {}".format(self.callback_identifier, self.userannotation, self.term)


class AlgoAnnotationTerm(Model):
    def __init__(self, id_annotation=None, id_term=None, id_expected_term=None, rate=1.0, **attributes):
        super(AlgoAnnotationTerm, self).__init__()
        self.annotation = id_annotation
        self.term = id_term
        self.expectedTerm = id_expected_term
        self.user = None
        self.rate = rate
        self.populate(attributes)

    def uri(self):
        if self.is_new():
            return "annotation/{}/term.json".format(self.annotation)
        else:
            return "annotation/{}/term/{}.json".format(self.annotation, self.term)

    def __str__(self):
        return "[{}] Annotation {} - Term {}".format(self.callback_identifier, self.annotation, self.term)


# class AnnotationUnion(Model):
#     def __init__(self, params=None):
#         super(AnnotationUnion, self).__init__(params)
#         self._callback_identifier = "annotationunion"
#
#     def to_url(self):
#         if self.buffer_length:
#             return "algoannotation/union.json?idUser=%d&idImage=%d&idTerm=%d&minIntersectionLength=%d&bufferLength=%d" % (
#             self.id_user, self.id_image, self.id_term, self.min_intersection_length, self.buffer_length)
#         else:
#             return "algoannotation/union.json?idUser=%d&idImage=%d&idTerm=%d&minIntersectionLength=%d" % (
#             self.id_user, self.id_image, self.id_term, self.min_intersection_length)
#
#     def __str__(self):
#         return "Annotation Union %d,%d,%d,%d " % (
#         self.id_user, self.id_image, self.id_term, self.min_intersection_length)
#
# class ReviewedAnnotationCollection(Collection):
#     def __init__(self, params=None):
#         super(ReviewedAnnotationCollection, self).__init__(Annotation, params)
#
#     def to_url(self):
#         if hasattr(self, "project"):
#             return "project/" + str(self.project) + "/reviewedannotation.json"
#         elif hasattr(self, "user") and hasattr(self, "imageinstance"):
#             return "user/" + str(self.user) + "/imageinstance/" + str(self.imageinstance) + "/reviewedannotation.json"
#         elif hasattr(self, "imageinstance"):
#             return "imageinstance/" + str(self.imageinstance) + "/reviewedannotation.json"
#         else:
#             return "reviewedannotation.json"