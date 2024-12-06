__version__ = "2.5.21.5764"

if __package__ or "." in __name__:
    from .core import *
else:
    from core import *

if __package__ or "." in __name__:
    from . import _DynamsoftDocumentNormalizer
else:
    import _DynamsoftDocumentNormalizer
from typing import List, Tuple


from enum import IntEnum


class EnumImageColourMode(IntEnum):
    ICM_COLOUR = _DynamsoftDocumentNormalizer.ICM_COLOUR
    ICM_GRAYSCALE = _DynamsoftDocumentNormalizer.ICM_GRAYSCALE
    ICM_BINARY = _DynamsoftDocumentNormalizer.ICM_BINARY

class SimplifiedDocumentNormalizerSettings:
    """
    The SimplifiedDocumentNormalizerSettings class contains settings for document normalization. It is a sub-parameter of SimplifiedCaptureVisionSettings.

    Attributes:
        grayscale_transformation_modes(List[int]): Specifies how grayscale transformations should be applied, including whether to process inverted grayscale images and the specific transformation mode to use.
        grayscale_enhancement_modes(List[int]): Specifies how to enhance the quality of the grayscale image.
        colour_mode(int): Specifies the colour mode of the output image.
        page_size(List[int]): Specifies the page size (width by height in pixels) of the normalized image.
        brightness(int): Specifies the brightness of the normalized image.
        contrast(int): Specifies the contrast of the normalized image.
        max_threads_in_one_task(int): Specifies the maximum available threads count in one document normalization task.
        scale_down_threshold(int): Specifies the threshold for the image shrinking.
        min_quadrilateral_area_ratio(int): Specifies the minimum ratio between the target quadrilateral area and the total image area. Only those exceeding this value will be output (measured in percentages).
        expected_documents_count(int): Specifies the number of documents expected to be detected.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    # grayscale_transformation_modes: List[int] = property(
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleTransformationModes_get,
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleTransformationModes_set,
    #     doc="""
    #         Specifies how grayscale transformations should be applied, including whether to process inverted grayscale images and the specific transformation mode to use.
    #         It is a list of 8 integers, where each integer represents a mode specified by the EnumGrayscaleTransformationMode enumeration.
    #         """
    # )
    # grayscale_enhancement_modes: List[int] = property(
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleEnhancementModes_get,
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleEnhancementModes_set,
    #     doc="""
    #         Specifies how to enhance the quality of the grayscale image.
    #         It is a list of 8 integers, where each integer represents a mode specified by the EnumGrayscaleEnhancementMode enumeration.
    #         """
    # )
    @property
    def grayscale_transformation_modes(self) -> List[int]:
        if not hasattr(self, '_grayscale_transformation_modes') or self._grayscale_transformation_modes is None:
            self._grayscale_transformation_modes = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleTransformationModes_get(self)
        return self._grayscale_transformation_modes

    @grayscale_transformation_modes.setter
    def grayscale_transformation_modes(self, value: List[int]):
        if not hasattr(self, '_grayscale_transformation_modes') or self._grayscale_transformation_modes is None:
            self._grayscale_transformation_modes = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleTransformationModes_get(self)
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleTransformationModes_set(self, value)
        self._grayscale_transformation_modes = value
    @property
    def grayscale_enhancement_modes(self) -> List[int]:
        if not hasattr(self, '_grayscale_enhancement_modes') or self._grayscale_enhancement_modes is None:
            self._grayscale_enhancement_modes = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleEnhancementModes_get(self)
        return self._grayscale_enhancement_modes

    @grayscale_enhancement_modes.setter
    def grayscale_enhancement_modes(self, value: List[int]):
        if not hasattr(self, '_grayscale_enhancement_modes') or self._grayscale_enhancement_modes is None:
            self._grayscale_enhancement_modes = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleEnhancementModes_get(self)
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_grayscaleEnhancementModes_set(self, value)
        self._grayscale_enhancement_modes = value
    colour_mode: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_colourMode_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_colourMode_set,
        doc="""
            Specifies the colour mode of the output image.
            It is a list of 8 integers, where each integer represents a mode specified by the EnumColourMode enumeration.
            """
    )
    @property
    def page_size(self) -> List[int]:
        if not hasattr(self, '_page_size') or self._page_size is None:
            self._page_size = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_pageSize_get(self)
        return self._page_size

    @page_size.setter
    def page_size(self, value: List[int]):
        if not hasattr(self, '_page_size') or self._page_size is None:
            self._page_size = _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_pageSize_get(self)
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_pageSize_set(self, value)
        self._page_size = value
    # page_size:List[int] = property(
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_pageSize_get,
    #     _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_pageSize_set,
    #     doc="Specifies the page size (width by height in pixels) of the normalized image."
    # )
    brightness: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_brightness_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_brightness_set,
        doc="""
            Specifies the brightness of the normalized image.
            Value Range: [-100,100]
            Default Value: 0
            """
    )
    contrast: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_contrast_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_contrast_set,
        doc="""
            Specifies the contrast of the normalized image.
            Value Range: [-100,100]
            Default Value: 0
            """
    )
    max_threads_in_one_task: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_maxThreadsInOneTask_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_maxThreadsInOneTask_set,
        doc="""
            Specifies the maximum available threads count in one document normalization task.
            Value Range: [1,256]
            Default Value: 4
            """
    )
    scale_down_threshold: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_scaleDownThreshold_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_scaleDownThreshold_set,
        doc="""
            Specifies the threshold for the image shrinking.
            Value Range: [512, 0x7fffffff]
            Default Value: 2300
            """
    )
    min_quadrilateral_area_ratio: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_minQuadrilateralAreaRatio_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_minQuadrilateralAreaRatio_set,
        doc="""
            Specifies the minimum ratio between the target quadrilateral area and the total image area.
            Only those exceeding this value will be output (measured in percentages).
            Value Range: [0, 100]
            Default Value: 0, which means no limitation.
            """
    )
    expected_documents_count: int = property(
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_expectedDocumentsCount_get,
        _DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_expectedDocumentsCount_set,
        doc="""
            Specifies the number of documents expected to be detected.
            Value Range: [0, 0x7fffffff]
            Default Value: 0, which means the count is unknown. The library will try to find at least 1 document.
            """
    )

    def __init__(self):
        _DynamsoftDocumentNormalizer.Class_init(
            self,
            _DynamsoftDocumentNormalizer.new_SimplifiedDocumentNormalizerSettings(),
        )

    __destroy__ = (
        _DynamsoftDocumentNormalizer.delete_SimplifiedDocumentNormalizerSettings
    )


_DynamsoftDocumentNormalizer.SimplifiedDocumentNormalizerSettings_register(
    SimplifiedDocumentNormalizerSettings
)

class DetectedQuadResultItem(CapturedResultItem):
    """
    The DetectedQuadResultItem class stores a captured result whose type is detected quad.

    Methods:
        get_location(self) -> Quadrilateral: Gets the location of current object.
        get_confidence_as_document_boundary(self) -> int: Gets the confidence of current object as a document boundary.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    def get_location(self) -> Quadrilateral:
        """
        Gets the location of current object.

        Returns:
            The location of current object.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadResultItem_GetLocation(self)

    def get_confidence_as_document_boundary(self) -> int:
        """
        Gets the confidence of current object as a document boundary.

        Returns:
            The confidence as document boundary of the detected quad result.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadResultItem_GetConfidenceAsDocumentBoundary(
            self
        )


_DynamsoftDocumentNormalizer.CDetectedQuadResultItem_register(DetectedQuadResultItem)


class NormalizedImageResultItem(CapturedResultItem):
    """
    The NormalizedImageResultItem class stores a captured result item whose type is normalized image.

    Methods:
        get_image_data(self) -> ImageData: Gets the image data of current object.
        get_location(self) -> Quadrilateral: Gets the location of current object.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    def get_image_data(self) -> ImageData:
        """
        Gets the image data of current object.

        Returns:
            The image data.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImageResultItem_GetImageData(
            self
        )

    def get_location(self) -> Quadrilateral:
        """
        Gets the location of current object.

        Returns:
            The location of current object.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImageResultItem_GetLocation(self)


_DynamsoftDocumentNormalizer.CNormalizedImageResultItem_register(
    NormalizedImageResultItem
)

class DetectedQuadsResult:
    """
    The DetectedQuadsResult class stores a captured result whose type is detected quads.

    Methods:
        get_error_code(self) -> int: Gets the error code of the detection operation.
        get_error_string(self) -> str: Gets the error message of the detection operation.
        get_items(self) -> List[DetectedQuadResultItem]: Gets all the detected quadrilateral items.
        get_rotation_transform_matrix(self) -> List[float]: Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.
        get_original_image_hash_id(self) -> str: Gets the hash ID of the original image.
        get_original_image_tag(self) -> ImageTag: Gets the tag of the original image.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftDocumentNormalizer.CDetectedQuadsResult_Release

    def get_original_image_hash_id(self) -> str:
        """
        Gets the hash ID of the original image.
        
        Returns:
            The hash ID of the original image as a string.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetOriginalImageHashId(
            self
        )

    def get_original_image_tag(self) -> ImageTag:
        """
        Gets the tag of the original image.

        Returns:
            An ImageTag object containing the tag of the original image.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetOriginalImageTag(
            self
        )

    def get_rotation_transform_matrix(self) -> List[float]:
        """
        Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.

        Returns:
            A float list of length 9 which represents a 3x3 rotation matrix.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetRotationTransformMatrix(
            self
        )

    def get_items(self) -> List[DetectedQuadResultItem]:
        """
        Gets all the detected quadrilateral items.

        Returns:
            A list of DetectedQuadResultItem objects with all the detected quadrilateral items.
        """
        list = []
        count = _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetItemsCount(self)
        for i in range(count):
            list.append(
                _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetItem(self, i)
            )
        return list

    def get_error_code(self) -> int:
        """
        Gets the error code of the detection operation.

        Returns:
            The error code.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetErrorCode(self)

    def get_error_string(self) -> str:
        """
        Gets the error message of the detection operation.

        Returns:
            A string that represents the error message.
        """
        return _DynamsoftDocumentNormalizer.CDetectedQuadsResult_GetErrorString(self)


_DynamsoftDocumentNormalizer.CDetectedQuadsResult_register(DetectedQuadsResult)

class NormalizedImagesResult:
    """
    The NormalizedImagesResult class stores a collection of captured result items whose type are normalized images.

    Methods:
        get_error_code(self) -> int: Gets the error code of the operation.
        get_error_string(self) -> str: Gets the error message of the operation.
        get_items(self) -> List[NormalizedImageResultItem]: Gets all the normalized images.
        get_rotation_transform_matrix(self) -> List[float]: Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.
        get_original_image_hash_id(self) -> str: Gets the hash ID of the original image that was normalized.
        get_original_image_tag(self) -> ImageTag: Gets the tag of the original image that was normalized.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftDocumentNormalizer.CNormalizedImagesResult_Release

    def get_original_image_hash_id(self) -> str:
        """
        Gets the hash ID of the original image that was normalized.

        Returns:
            The hash ID of the original image that was normalized.
        """
        return (
            _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetOriginalImageHashId(
                self
            )
        )

    def get_original_image_tag(self) -> ImageTag:
        """
        Gets the tag of the original image that was normalized.

        Returns:
            A tag of the original image that was normalized.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetOriginalImageTag(
            self
        )

    def get_rotation_transform_matrix(self) -> List[float]:
        """
        Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.

        Returns:
            A float list of length 9 which represents a 3x3 rotation matrix.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetRotationTransformMatrix(
            self
        )

    def get_items(self) -> List[NormalizedImageResultItem]:
        """
        Gets all the normalized images.

        Returns:
            A NormalizedImageResultItem list.
        """
        list = []
        count = _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetItemsCount(self)
        for i in range(count):
            list.append(
                _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetItem(self, i)
            )
        return list

    def get_error_code(self) -> int:
        """
        Gets the error code of the operation.

        Returns:
            The error code of the operation. A non-zero value indicates an error occurred.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetErrorCode(self)

    def get_error_string(self) -> str:
        """
        Gets the error message of the operation.

        Returns:
            The error message of the operation.
        """
        return _DynamsoftDocumentNormalizer.CNormalizedImagesResult_GetErrorString(self)


_DynamsoftDocumentNormalizer.CNormalizedImagesResult_register(NormalizedImagesResult)


class DocumentNormalizerModule:
    """
    The DocumentNormalizerModule class defines general functions in the document normalizer module.
    
    Methods:
        get_version() -> str: Returns the version of the document normalizer module.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    @staticmethod
    def get_version() -> str:
        """
        Returns the version of the document normalizer module.

        Returns:
            A string representing the version of the document normalizer module.
        """
        return __version__ + " (Algotithm " + _DynamsoftDocumentNormalizer.CDocumentNormalizerModule_GetVersion() + ")"

    def __init__(self):
        _DynamsoftDocumentNormalizer.Class_init(
            self, _DynamsoftDocumentNormalizer.new_CDocumentNormalizerModule()
        )

    __destroy__ = _DynamsoftDocumentNormalizer.delete_CDocumentNormalizerModule


_DynamsoftDocumentNormalizer.CDocumentNormalizerModule_register(
    DocumentNormalizerModule
)


#new 

class DetectedQuadElement(RegionObjectElement):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        _DynamsoftDocumentNormalizer.Class_init(
            self, _DynamsoftDocumentNormalizer.CDocumentNormalizerModule_CreateDetectedQuadElement()
        )

    def get_confidence_as_document_boundary(self) -> int:
        return _DynamsoftDocumentNormalizer.CDetectedQuadElement_GetConfidenceAsDocumentBoundary(self)

# Register CDetectedQuadElement in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CDetectedQuadElement_register(DetectedQuadElement)
class NormalizedImageElement(RegionObjectElement):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        _DynamsoftDocumentNormalizer.Class_init(
            self, _DynamsoftDocumentNormalizer.CDocumentNormalizerModule_CreateNormalizedImageElement()
        )
    

    def get_image_data(self) -> ImageData:
        return _DynamsoftDocumentNormalizer.CNormalizedImageElement_GetImageData(self)

# Register CNormalizedImageElement in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CNormalizedImageElement_register(NormalizedImageElement)
class LongLinesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_GetCount(self)

    def get_long_line(self, index: int) -> LineSegment:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_GetLongLine(self, index)

    def remove_all_long_lines(self) -> None:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_RemoveAllLongLines(self)

    def remove_long_line(self, index: int) -> int:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_RemoveLongLine(self, index)

    def add_long_line(self, line: LineSegment, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_AddLongLine(self, line, matrix_to_original_image)

    def set_long_line(self, index: int, line: LineSegment, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CLongLinesUnit_SetLongLine(self, index, line, matrix_to_original_image)

# Register CLongLinesUnit in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CLongLinesUnit_register(LongLinesUnit)
class CornersUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftDocumentNormalizer.CCornersUnit_GetCount(self)

    def get_corner(self, index: int) -> Tuple[int, Corner]:
        return _DynamsoftDocumentNormalizer.CCornersUnit_GetCorner(self, index)

    def remove_all_corners(self) -> None:
        return _DynamsoftDocumentNormalizer.CCornersUnit_RemoveAllCorners(self)

    def remove_corner(self, index: int) -> int:
        return _DynamsoftDocumentNormalizer.CCornersUnit_RemoveCorner(self, index)

    def add_corner(self, corner: Corner, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CCornersUnit_AddCorner(self, corner, matrix_to_original_image)

    def set_corner(self, index: int, corner: Corner, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CCornersUnit_SetCorner(self, index, corner, matrix_to_original_image)

# Register CCornersUnit in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CCornersUnit_register(CornersUnit)
class CandidateQuadEdgesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_GetCount(self)

    def get_candidate_quad_edge(self, index: int) -> Tuple[int, Edge]:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_GetCandidateQuadEdge(self, index)

    def remove_all_candidate_quad_edges(self) -> None:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_RemoveAllCandidateQuadEdges(self)

    def remove_candidate_quad_edge(self, index: int) -> int:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_RemoveCandidateQuadEdge(self, index)

    def add_candidate_quad_edge(self, edge: Edge, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_AddCandidateQuadEdge(self, edge, matrix_to_original_image)

    def set_candidate_quad_edge(self, index: int, edge: Edge, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_SetCandidateQuadEdge(self, index, edge, matrix_to_original_image)

# Register CCandidateQuadEdgesUnit in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CCandidateQuadEdgesUnit_register(CandidateQuadEdgesUnit)
class DetectedQuadsUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_GetCount(self)

    def get_detected_quad(self, index: int) -> DetectedQuadElement:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_GetDetectedQuad(self, index)

    def remove_all_detected_quads(self) -> None:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_RemoveAllDetectedQuads(self)

    def remove_detected_quad(self, index: int) -> int:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_RemoveDetectedQuad(self, index)

    def add_detected_quad(self, element: DetectedQuadElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_AddDetectedQuad(self, element, matrix_to_original_image)

    def set_detected_quad(self, index: int, element: DetectedQuadElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CDetectedQuadsUnit_SetDetectedQuad(self, index, element, matrix_to_original_image)

# Register CDetectedQuadsUnit in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CDetectedQuadsUnit_register(DetectedQuadsUnit)
class NormalizedImagesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftDocumentNormalizer.CNormalizedImagesUnit_GetCount(self)

    def get_normalized_image(self, index: int) -> NormalizedImageElement:
        return _DynamsoftDocumentNormalizer.CNormalizedImagesUnit_GetNormalizedImage(self, index)

    def remove_all_normalized_images(self) -> None:
        return _DynamsoftDocumentNormalizer.CNormalizedImagesUnit_RemoveAllNormalizedImages(self)

    def set_normalized_image(self, element: NormalizedImageElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftDocumentNormalizer.CNormalizedImagesUnit_SetNormalizedImage(self, element, matrix_to_original_image)

# Register CNormalizedImagesUnit in _DynamsoftDocumentNormalizer:
_DynamsoftDocumentNormalizer.CNormalizedImagesUnit_register(NormalizedImagesUnit)