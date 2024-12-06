__version__ = "3.5.21.5764"

if __package__ or "." in __name__:
    from .core import *
else:
    from core import *

if __package__ or "." in __name__:
    from . import _DynamsoftLabelRecognizer
else:
    import _DynamsoftLabelRecognizer

from typing import List,Tuple

from enum import IntEnum

class EnumRawTextLineStatus(IntEnum):
    RTLS_LOCALIZED = _DynamsoftLabelRecognizer.RTLS_LOCALIZED
    RTLS_RECOGNITION_FAILED = _DynamsoftLabelRecognizer.RTLS_RECOGNITION_FAILED
    RTLS_RECOGNITION_SUCCEEDED = _DynamsoftLabelRecognizer.RTLS_RECOGNITION_SUCCEEDED

class SimplifiedLabelRecognizerSettings:
    """
    The SimplifiedLabelRecognizerSettings class contains settings for label recognition.
    It is a sub-parameter of SimplifiedCaptureVisionSettings.

    Attributes:
        grayscale_transformation_modes(List[int]): Specifies how grayscale transformations should be applied, including whether to process inverted grayscale images and the specific transformation mode to use.
        grayscale_enhancement_modes(List[int]): Specifies how to enhance the quality of the grayscale image.
        character_model_name(str): Specifies a character model by its name.
        line_string_regex_pattern(str): Specifies the RegEx pattern of the text line string to filter out the unqualified results.
        max_threads_in_one_task(int): Specifies the maximum available threads count in one label recognition task.
        scale_down_threshold(int): Specifies the threshold for the image shrinking.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    # grayscale_transformation_modes: List[int] = property(
    #     _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleTransformationModes_get,
    #     _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleTransformationModes_set,
    #     doc="""
    #         Specifies how grayscale transformations should be applied, including whether to process inverted grayscale images and the specific transformation mode to use.
    #         It is a list of 8 integers, where each integer represents a mode specified by the EnumGrayscaleTransformationMode enumeration.
    #         """
    # )
    # grayscale_enhancement_modes: List[int] = property(
    #     _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleEnhancementModes_get,
    #     _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleEnhancementModes_set,
    #     doc="""
    #         Specifies how to enhance the quality of the grayscale image.
    #         It is a list of 8 integers, where each integer represents a mode specified by the EnumGrayscaleEnhancementMode enumeration.
    #         """,
    # )
    @property
    def grayscale_transformation_modes(self) -> List[int]:
        if not hasattr(self, "_grayscale_transformation_modes") or self._grayscale_transformation_modes is None:
            self._grayscale_transformation_modes = _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleTransformationModes_get(self)
        return self._grayscale_transformation_modes
    @grayscale_transformation_modes.setter
    def grayscale_transformation_modes(self, value):
        if not hasattr(self, "_grayscale_transformation_modes") or self._grayscale_transformation_modes is None:
            self._grayscale_transformation_modes = _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleTransformationModes_get(self)
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleTransformationModes_set(self, value)
        self._grayscale_transformation_modes = value

    @property
    def grayscale_enhancement_modes(self) -> List[int]:
        if not hasattr(self, "_grayscale_enhancement_modes") or self._grayscale_enhancement_modes is None:
            self._grayscale_enhancement_modes = _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleEnhancementModes_get(self)
        return self._grayscale_enhancement_modes
    @grayscale_enhancement_modes.setter
    def grayscale_enhancement_modes(self, value):
        if not hasattr(self, "_grayscale_enhancement_modes") or self._grayscale_enhancement_modes is None:
            self._grayscale_enhancement_modes = _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleEnhancementModes_get(self)
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_grayscaleEnhancementModes_set(self, value)
        self._grayscale_enhancement_modes = value

    character_model_name: str = property(
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_characterModelName_get,
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_characterModelName_set,
        doc="Specifies a character model by its name.",
    )
    line_string_regex_pattern: str = property(
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_lineStringRegExPattern_get,
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_lineStringRegExPattern_set,
        doc="Specifies the RegEx pattern of the text line string to filter out the unqualified results.",
    )
    max_threads_in_one_task: int = property(
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_maxThreadsInOneTask_get,
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_maxThreadsInOneTask_set,
        doc="""
            Specifies the maximum available threads count in one label recognition task.
            Value Range: [1, 256]
            Default value: 4
            """,
    )
    scale_down_threshold: int = property(
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_scaleDownThreshold_get,
        _DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_scaleDownThreshold_set,
        doc="""
            Specifies the threshold for the image shrinking.
            Value Range: [512, 0x7fffffff]
            Default Value: 2300
            """,
    )

    def __init__(self):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.new_SimplifiedLabelRecognizerSettings()
        )

    __destroy__ = _DynamsoftLabelRecognizer.delete_SimplifiedLabelRecognizerSettings


_DynamsoftLabelRecognizer.SimplifiedLabelRecognizerSettings_register(
    SimplifiedLabelRecognizerSettings
)

class CharacterResult:
    """
    The CharacterResult class represents the result of a character recognition process.
    It contains the characters recognized (high, medium, and low confidence), their respective confidences, and the location of the character in a quadrilateral shape.

    Attributes:
        character_h(str): The character with high confidence.
        character_m(str): The character with medium confidence.
        character_l(str): The character with low confidence.
        location(Quadrilateral): The location of the character in a quadrilateral shape.
        character_h_confidence(int): The confidence of the character with high confidence.
        character_m_confidence(int): The confidence of the character with medium confidence.
        character_l_confidence(int): The confidence of the character with low confidence.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    character_h: str = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterH_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterH_set,
        doc="The character with high confidence."
    )
    character_m: str = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterM_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterM_set,
        doc="The character with medium confidence."
    )
    character_l: str = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterL_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterL_set,
        doc="The character with low confidence."
    )
    location: Quadrilateral = property(
        _DynamsoftLabelRecognizer.CCharacterResult_location_get,
        _DynamsoftLabelRecognizer.CCharacterResult_location_set,
        doc="The location of the character in a quadrilateral shape."
    )
    character_h_confidence: int = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterHConfidence_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterHConfidence_set,
        doc="The confidence of the character with high confidence."
    )
    character_m_confidence: int = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterMConfidence_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterMConfidence_set,
        doc="The confidence of the character with medium confidence."
    )
    character_l_confidence: int = property(
        _DynamsoftLabelRecognizer.CCharacterResult_characterLConfidence_get,
        _DynamsoftLabelRecognizer.CCharacterResult_characterLConfidence_set,
        doc="The confidence of the character with low confidence."
    )

    def __init__(self):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.new_CCharacterResult()
        )

    __destroy__ = _DynamsoftLabelRecognizer.delete_CCharacterResult


_DynamsoftLabelRecognizer.CCharacterResult_register(CharacterResult)

class TextLineResultItem(CapturedResultItem):
    """
    The TextLineResultItem class represents a text line result item recognized by the library. It is derived from CapturedResultItem.

    Methods:
        get_text(self) -> str: Gets the text content of the text line.
        get_location(self) -> Quadrilateral: Gets the location of the text line in the form of a quadrilateral.
        get_confidence(self) -> int: Gets the confidence of the text line recognition result.
        get_character_results(self) -> List[CharacterResult]: Gets all the character results.
        get_specification_name(self) -> str: Gets the name of the text line specification that generated this item.
        get_raw_text(self) -> str: Gets the recognized raw text, excluding any concatenation separators.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    def get_text(self) -> str:
        """
        Gets the text content of the text line.

        Returns:
            The text content of the text line.
        """
        return _DynamsoftLabelRecognizer.CTextLineResultItem_GetText(self)

    def get_location(self) -> Quadrilateral:
        """
        Gets the location of the text line in the form of a quadrilateral.

        Returns:
            The location of the text line in the form of a quadrilateral.
        """
        return _DynamsoftLabelRecognizer.CTextLineResultItem_GetLocation(self)

    def get_confidence(self) -> int:
        """
        Gets the confidence of the text line recognition result.

        Returns:
            The confidence of the text line recognition result.
        """
        return _DynamsoftLabelRecognizer.CTextLineResultItem_GetConfidence(self)

    def get_character_results(self) -> List[CharacterResult]:
        """
        Gets all the character results.

        Returns:
            All the character results as a CharacterResult list.
        """
        list = []
        count = _DynamsoftLabelRecognizer.CTextLineResultItem_GetCharacterResultsCount(
            self
        )
        for i in range(count):
            list.append(
                _DynamsoftLabelRecognizer.CTextLineResultItem_GetCharacterResult(
                    self, i
                )
            )
        return list

    def get_specification_name(self) -> str:
        """
        Gets the name of the text line specification that generated this item.

        Returns:
            The name of the text line specification that generated this item.
        """
        return _DynamsoftLabelRecognizer.CTextLineResultItem_GetSpecificationName(self)

    def get_raw_text(self) -> str:
        """
        Gets the recognized raw text, excluding any concatenation separators.

        Returns:
            The recognized raw text.
        """
        return _DynamsoftLabelRecognizer.CTextLineResultItem_GetRawText(self)


_DynamsoftLabelRecognizer.CTextLineResultItem_register(TextLineResultItem)


class RecognizedTextLinesResult:
    """
    The RecognizedTextLinesResult class represents the result of a text recognition process.
    It provides access to information about the recognized text lines, the original image, and any errors that occurred during the recognition process.

    Methods:
        get_original_image_hash_id(self) -> str: Gets the hash ID of the original image.
        get_original_image_tag(self) -> ImageTag: Gets the tag of the original image.
        get_rotation_transform_matrix(self) -> List[float]: Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.
        get_items(self) -> List[TextLineResultItem]: Gets all the text line result items.
        get_error_code(self) -> int: Gets the error code of the recognition result, if an error occurred.
        get_error_string(self) -> str: Gets the error message of the recognition result, if an error occurred.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_Release

    def get_original_image_hash_id(self) -> str:
        """
        Gets the hash ID of the original image.

        Returns:
            A string containing the hash ID of the original image.
        """
        return (
            _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetOriginalImageHashId(
                self
            )
        )

    def get_original_image_tag(self) -> ImageTag:
        """
        Gets the tag of the original image.

        Returns:
            An ImageTag object containing the tag of the original image.
        """
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetOriginalImageTag(
            self
        )

    def get_rotation_transform_matrix(self) -> List[float]:
        """
        Gets the 3x3 rotation transformation matrix of the original image relative to the rotated image.

        Returns:
            A float list of length 9 which represents a 3x3 rotation matrix.
        """
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetRotationTransformMatrix(
            self
        )

    def get_items(self) -> List[TextLineResultItem]:
        """
        Gets all the text line result items.

        Returns:
            A TextLineResultItem list.
        """
        list = []
        count = _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetItemsCount(self)
        for i in range(count):
            list.append(
                _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetItem(self, i)
            )
        return list

    def get_error_code(self) -> int:
        """
        Gets the error code of the recognition result, if an error occurred.

        Returns:
            The error code.
        """
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetErrorCode(self)

    def get_error_string(self) -> str:
        """
        Gets the error message of the recognition result, if an error occurred.

        Returns:
            A string that represents the error message.
        """
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesResult_GetErrorString(self)


_DynamsoftLabelRecognizer.CRecognizedTextLinesResult_register(RecognizedTextLinesResult)


class LabelRecognizerModule:
    """
    The LabelRecognizerModule class represents a label recognizer module.

    Methods:
        get_version() -> str: Gets the version of the label recognizer module.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    @staticmethod
    def get_version() -> str:
        """
        Gets the version of the label recognizer module.

        Returns:
            A string representing the version of the label recognizer module.
        """
        return __version__ + " (Algotithm " + _DynamsoftLabelRecognizer.CLabelRecognizerModule_GetVersion() + ")"

    def __init__(self):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.new_CLabelRecognizerModule()
        )

    __destroy__ = _DynamsoftLabelRecognizer.delete_CLabelRecognizerModule


_DynamsoftLabelRecognizer.CLabelRecognizerModule_register(LabelRecognizerModule)


class BufferedCharacterItem:
    """
    The BufferedCharacterItem class represents a text line result item recognized by the library. It is derived from CapturedResultItem.

    Methods:
        get_character(self) -> str: Gets the buffered character value.
        get_image(self) -> ImageData: Gets the image data of the buffered character.
        get_features(self) -> List[Tuple[int, float]]: Gets all the features formatted with id and value of the buffered character.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftLabelRecognizer.delete_CBufferedCharacterItem

    def get_character(self) -> str:
        """
        Gets the buffered character value.

        Returns:
            The buffered character value.
        """
        return _DynamsoftLabelRecognizer.CBufferedCharacterItem_GetCharacter(self)

    def get_image(self) -> ImageData:
        """
        Gets the image data of the buffered character.

        Returns:
            The image data of the buffered character.
        """
        return _DynamsoftLabelRecognizer.CBufferedCharacterItem_GetImage(self)

    def get_features(self) -> List[Tuple[int, float]]:
        """
        Gets all the features formatted with id and value of the buffered character.
        
        Returns:
            A tuple list while each item contains following elements.
            - feature_id <int>: The feature id.
            - feature_value <float>: The feature value.
        """
        list = []
        count = _DynamsoftLabelRecognizer.CBufferedCharacterItem_GetFeaturesCount(self)
        for i in range(count):
            err,id,feature = _DynamsoftLabelRecognizer.CBufferedCharacterItem_GetFeature(self, i)
            list.append([id,feature])
        return list


_DynamsoftLabelRecognizer.CBufferedCharacterItem_register(BufferedCharacterItem)


class CharacterCluster:
    """
    The CharacterCluster class represents a character cluster generated from the buffered character items. These buffered items will be clustered based on feature similarity to obtain cluster centers.

    Methods:
        get_character(self) -> str: Gets the character value of the cluster.
        get_mean(self) -> BufferedCharacterItem: Gets the mean of the cluster.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftLabelRecognizer.delete_CCharacterCluster

    def get_character(self) -> str:
        """
        Gets the character value of the cluster.

        Returns:
            The character value of the cluster.
        """
        return _DynamsoftLabelRecognizer.CCharacterCluster_GetCharacter(self)

    def get_mean(self) -> BufferedCharacterItem:
        """
        Gets the mean of the cluster.

        Returns:
            The mean of the cluster which is a BufferedCharacterItem object.
        """
        return _DynamsoftLabelRecognizer.CCharacterCluster_GetMean(self)


_DynamsoftLabelRecognizer.CCharacterCluster_register(CharacterCluster)


class BufferedCharacterItemSet:
    """
    The BufferedCharacterItemSet class represents a collection of buffered character items and associated character clusters.

    Methods:
        get_items(self) -> List[BufferedCharacterItem]: Gets all the buffered items.
        get_character_clusters(self) -> List[CharacterCluster]: Gets all the character clusters.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        raise AttributeError("No constructor defined - class is abstract")

    __destroy__ = _DynamsoftLabelRecognizer.CBufferedCharacterItemSet_Release

    def get_items(self) -> List[BufferedCharacterItem]:
        """
        Gets all the buffered items.

        Returns:
            A BufferedCharacterItem list.
        """
        list = []
        count = _DynamsoftLabelRecognizer.CBufferedCharacterItemSet_GetItemsCount(self)
        for i in range(count):
            list.append(
                _DynamsoftLabelRecognizer.CBufferedCharacterItemSet_GetItem(self, i)
            )
        return list

    def get_character_clusters(self) -> List[CharacterCluster]:
        """
        Gets all the character clusters.

        Returns:
            A CharacterCluster list.
        """
        list = []
        count = _DynamsoftLabelRecognizer.CBufferedCharacterItemSet_GetCharacterClustersCount(
            self
        )
        for i in range(count):
            list.append(
                _DynamsoftLabelRecognizer.CBufferedCharacterItemSet_GetCharacterCluster(
                    self, i
                )
            )
        return list


_DynamsoftLabelRecognizer.CBufferedCharacterItemSet_register(BufferedCharacterItemSet)


#new 

class LocalizedTextLineElement(RegionObjectElement):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.CLabelRecognizerModule_CreateLocalizedTextLineElement()
        )

    def get_character_quads_count(self) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLineElement_GetCharacterQuadsCount(self)
    
    def get_character_quad(self, index: int) -> Tuple[int, Quadrilateral]:
        return _DynamsoftLabelRecognizer.CLocalizedTextLineElement_GetCharacterQuad(self, index)

    def get_row_number(self) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLineElement_GetRowNumber(self)

# Register CLocalizedTextLineElement in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CLocalizedTextLineElement_register(LocalizedTextLineElement)
class RecognizedTextLineElement(RegionObjectElement):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.CLabelRecognizerModule_CreateRecognizedTextLineElement()
        )
    

    def get_text(self) -> str:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetText(self)

    def get_confidence(self) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetConfidence(self)

    def get_character_results_count(self) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetCharacterResultsCount(self)

    def get_row_number(self) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetRowNumber(self)

    def get_character_result(self, index: int) -> CharacterResult:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetCharacterResult(self, index)

    def set_text(self, text: str) -> None:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_SetText(self, text)

    def get_specification_name(self) -> str:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetSpecificationName(self)

    def get_raw_text(self) -> str:
        return _DynamsoftLabelRecognizer.CRecognizedTextLineElement_GetRawText(self)

# Register CRecognizedTextLineElement in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CRecognizedTextLineElement_register(RecognizedTextLineElement)
class LocalizedTextLinesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_GetCount(self)

    def get_localized_text_line(self, index: int) -> LocalizedTextLineElement:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_GetLocalizedTextLine(self, index)

    def remove_all_localized_text_lines(self) -> None:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_RemoveAllLocalizedTextLines(self)

    def remove_localized_text_line(self, index: int) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_RemoveLocalizedTextLine(self, index)

    def add_localized_text_line(self, element: LocalizedTextLineElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_AddLocalizedTextLine(self, element, matrix_to_original_image)

    def set_localized_text_line(self, index: int, element: LocalizedTextLineElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_SetLocalizedTextLine(self, index, element, matrix_to_original_image)

# Register CLocalizedTextLinesUnit in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CLocalizedTextLinesUnit_register(LocalizedTextLinesUnit)
class RecognizedTextLinesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_GetCount(self)

    def get_recognized_text_line(self, index: int) -> RecognizedTextLineElement:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_GetRecognizedTextLine(self, index)

    def remove_all_recognized_text_lines(self) -> None:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_RemoveAllRecognizedTextLines(self)

    def remove_recognized_text_line(self, index: int) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_RemoveRecognizedTextLine(self, index)

    def add_recognized_text_line(self, element: RecognizedTextLineElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_AddRecognizedTextLine(self, element, matrix_to_original_image)

    def set_recognized_text_line(self, index: int, element: RecognizedTextLineElement, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_SetRecognizedTextLine(self, index, element, matrix_to_original_image)

# Register CRecognizedTextLinesUnit in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CRecognizedTextLinesUnit_register(RecognizedTextLinesUnit)
class RawTextLine:
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        _DynamsoftLabelRecognizer.Class_init(
            self, _DynamsoftLabelRecognizer.CLabelRecognizerModule_CreateRawTextLine()
        )
    __destroy__ = _DynamsoftLabelRecognizer.CRawTextLine_Release

    def get_text(self) -> str:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetText(self)

    def get_confidence(self) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetConfidence(self)

    def get_character_results_count(self) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetCharacterResultsCount(self)

    def get_row_number(self) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetRowNumber(self)

    def get_character_result(self, index: int) -> CharacterResult:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetCharacterResult(self, index)

    def set_text(self, text: str) -> None:
        return _DynamsoftLabelRecognizer.CRawTextLine_SetText(self, text)

    def get_specification_name(self) -> str:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetSpecificationName(self)

    def get_location(self) -> Quadrilateral:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetLocation(self)

    def set_location(self, location: Quadrilateral) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_SetLocation(self, location)

    def get_status(self) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_GetStatus(self)

    def clone(self) -> "RawTextLine":
        return _DynamsoftLabelRecognizer.CRawTextLine_Clone(self)

    def set_row_number(self, row_number: int) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_SetRowNumber(self, row_number)

    def set_specification_name(self, specification_name: str) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLine_SetSpecificationName(self, specification_name)

# Register CRawTextLine in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CRawTextLine_register(RawTextLine)
class RawTextLinesUnit(IntermediateResultUnit):
    _thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    

    def get_count(self) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_GetCount(self)

    def get_raw_text_line(self, index: int) -> RawTextLine:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_GetRawTextLine(self, index)

    def remove_all_raw_text_lines(self) -> None:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_RemoveAllRawTextLines(self)

    def remove_raw_text_line(self, index: int) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_RemoveRawTextLine(self, index)

    def add_raw_text_line(self, text_line: RawTextLine, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_AddRawTextLine(self, text_line, matrix_to_original_image)

    def set_raw_text_line(self, index: int, text_line: RawTextLine, matrix_to_original_image: List[float] = IDENTITY_MATRIX) -> int:
        return _DynamsoftLabelRecognizer.CRawTextLinesUnit_SetRawTextLine(self, index, text_line, matrix_to_original_image)

# Register CRawTextLinesUnit in _DynamsoftLabelRecognizer:
_DynamsoftLabelRecognizer.CRawTextLinesUnit_register(RawTextLinesUnit)