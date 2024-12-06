__version__ = "1.5.21.5764"

if __package__ or "." in __name__:
    from .cvr import *
else:
    from cvr import *

if __package__ or "." in __name__:
    from .core import *
else:
    from core import *

if __package__ or "." in __name__:
    from . import _DynamsoftUtility
else:
    import _DynamsoftUtility


from abc import ABC, abstractmethod
from typing import List, Tuple


class UtilityModule:
    """
    The UtilityModule class contains utility functions.

    Methods:
        get_version() -> str: Returns the version of the utility module.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    @staticmethod
    def get_version() -> str:
        """
        Returns the version of the utility module.

        Returns:
            A string representing the version of the utility module.
        """
        return __version__ + " (Algotithm " + _DynamsoftUtility.CUtilityModule_GetVersion() + ")"

    def __init__(self):
        _DynamsoftUtility.Class_init(
            self, _DynamsoftUtility.new_CUtilityModule()
        )

    __destroy__ = _DynamsoftUtility.delete_CUtilityModule


_DynamsoftUtility.CUtilityModule_register(UtilityModule)

class MultiFrameResultCrossFilter(CapturedResultFilter):
    """
    The MultiFrameResultCrossFilter class is responsible for filtering captured results. As a default implementation of CapturedResultFilter, it provides results verification and duplicate results filtering features.

    Methods:
        enable_result_cross_verification(self, result_item_types: int, enabled: bool) -> None: Enable result cross verification feature to improve the accuracy of video streaming recognition results.
        is_result_cross_verification_enabled(self, type: int) -> bool: Determines whether the result cross verification feature is enabled for the specific captured result item type.
        enable_result_deduplication(self, result_item_types: int, enabled: bool) -> None: Enable result deduplication feature to filter out the duplicate results in the period of duplicateForgetTime for video streaming recognition.
        is_result_deduplication_enabled(self, type: int) -> bool: Determines whether the result deduplication feature is enabled for the specific result item type.
        set_duplicate_forget_time(self, result_item_types: int, duplicate_forget_time: int) -> None: Sets the duplicate forget time for the specific captured result item types.
        get_duplicate_forget_time(self, type: int) -> int: Gets the duplicate forget time for a specific captured result item type.
        set_max_overlapping_frames(self, result_item_types: int, max_overlapping_frames: int) -> None: Sets the max referencing frames count for the to-the-latest overlapping feature.
        get_max_overlapping_frames(self, type: int) -> int: Gets the max referencing frames count for the to-the-latest overlapping feature.
        enable_latest_overlapping(self, result_item_types: int, enable: bool) -> None: Enable to-the-latest overlapping feature. The output decoded barcode result will become a combination of the recent results if the  latest frame is proved to be similar with the previous.
        is_latest_overlapping_enabled(self, type: int) -> bool: Determines whether the to-the-latest overlapping feature is enabled for the specific result item type.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self, cvr: CaptureVisionRouter = None):
        _DynamsoftUtility.Class_init(
            self, _DynamsoftUtility.new_CMultiFrameResultCrossFilter(cvr)
        )

    __destroy__ = _DynamsoftUtility.delete_CMultiFrameResultCrossFilter

    def enable_result_cross_verification(
        self, result_item_types: int, enabled: bool
    ) -> None:
        """
        Enable result cross verification feature to improve the accuracy of video streaming recognition results.

        Args:
            result_item_types (int): A bitwise OR combination of one or more values from the EnumCapturedResultItemType enumeration.
            enabled (bool): Set whether to enable result verification.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_EnableResultCrossVerification(
            self, result_item_types, enabled
        )

    def is_result_cross_verification_enabled(self, type: int) -> bool:
        """
        Determines whether the result cross verification feature is enabled for the specific captured result item type.

        Args:
            type (int): The specific captured result item type. It is a value from the EnumCapturedResultItemType enumeration.

        Returns:
            A bool value indicating whether result verification is enabled for the specific captured result item type.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_IsResultCrossVerificationEnabled(
            self, type
        )

    def enable_result_deduplication(self, result_item_types: int, enabled: bool) -> None:
        """
        Enable result deduplication feature to filter out the duplicate results in the period of duplicateForgetTime for video streaming recognition.

        Args:
            result_item_types (int): A bitwise OR combination of one or more values from the EnumCapturedResultItemType enumeration.
            enabled (bool): Set whether to enable result result deduplication.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_EnableResultDeduplication(
            self, result_item_types, enabled
        )

    def is_result_deduplication_enabled(self, type: int) -> bool:
        """
        Determines whether the result deduplication feature is enabled for the specific result item type.

        Args:
            type (int): The specific captured result item type. It is a value from the EnumCapturedResultItemType enumeration.

        Returns:
            A bool value indicating whether result deduplication is enabled for the specific result item type.
        """
        return (
            _DynamsoftUtility.CMultiFrameResultCrossFilter_IsResultDeduplicationEnabled(
                self, type
            )
        )

    def set_duplicate_forget_time(self, result_item_types: int, time: int) -> None:
        """
        Sets the duplicate forget time for the specific captured result item types. The same captured result item will be returned only once during the period if deduplication feature is enabled. The default value is 3000ms.

        Args:
            result_item_types (int): A bitwise OR combination of one or more values from the EnumCapturedResultItemType enumeration.
            time (int): The duplicate forget time measured in milliseconds. The value rang is [1, 180000].
        """

        return _DynamsoftUtility.CMultiFrameResultCrossFilter_SetDuplicateForgetTime(
            self, result_item_types, time
        )

    def get_duplicate_forget_time(self, type: int) -> int:
        """
        Gets the duplicate forget time for a specific captured result item type.

        Args:
            type (int): The specific captured result item type. It is a value from the EnumCapturedResultItemType enumeration.

        Returns:
            The duplicate forget time for the specific captured result item type.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_GetDuplicateForgetTime(
            self, type
        )

    def set_max_overlapping_frames(self, result_item_types: int, max_overlapping_frames: int) -> None:
        """
        Sets the max referencing frames count for the to-the-latest overlapping feature.

        Args:
            result_item_types (int): Specifies one or multiple specific result item types, which can be defined using CapturedResultItemType.
            max_overlapping_frames (int): The max referencing frames count for the to-the-latest overlapping feature.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_SetMaxOverlappingFrames(
            self, result_item_types, max_overlapping_frames
        )

    def get_max_overlapping_frames(self, type: int) -> int:
        """
        Gets the max referencing frames count for the to-the-latest overlapping feature.

        Args:
            type (int): Specifies a specific result item type, which can be defined using CapturedResultItemType.

        Returns:
            The max referencing frames count for the to-the-latest overlapping feature.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_GetMaxOverlappingFrames(
            self, type
        )

    def enable_latest_overlapping(self, result_item_types: int, enabled: bool) -> None:
        """
        Enable to-the-latest overlapping feature. The output decoded barcode result will become a combination of the recent results if the  latest frame is proved to be similar with the previous.

        Args:
            result_item_types (int): The or value of the captured result item types.
            enable (bool): Set whether to enable to-the-latest overlapping.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_EnableLatestOverlapping(
            self, result_item_types, enabled
        )

    def is_latest_overlapping_enabled(self, type: int) -> bool:
        """
        Determines whether the to-the-latest overlapping feature is enabled for the specific result item type.

        Args:
            type (int): The specific captured result item type.

        Returns:
            A bool value indicating whether to-the-latest overlapping is enabled for the specific captured result item type.
        """
        return _DynamsoftUtility.CMultiFrameResultCrossFilter_IsLatestOverlappingEnabled(
            self, type
        )
    
_DynamsoftUtility.CMultiFrameResultCrossFilter_register(MultiFrameResultCrossFilter)

class ProactiveImageSourceAdapter(ImageSourceAdapter, ABC):
    """
    The ProactiveImageSourceAdapter class is an abstract class that extends the ImageSourceAdapter class. It provides classs for proactively fetching images in a separate thread.

    Methods:
        _fetch_image(): This method needs to be implemented in the derived class. It is called in a loop in the Fetching thread to obtain images.
        set_image_fetch_interval(self, milliseconds: int) -> None: Sets the time interval for the ImageSource to wait before attempting to fetch another image to put in the buffer.
        get_image_fetch_interval(self) -> int: Gets the time interval for the ImageSource to wait before attempting to fetch another image to put in the buffer.
        has_next_image_to_fetch(self) -> bool: Determines whether there are more images left to fetch.
        start_fetching(self) -> None: Starts fetching images.
        stop_fetching(self) -> None: Stops fetching images.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        _DynamsoftUtility.Class_init(
            self, _DynamsoftUtility.new_CProactiveImageSourceAdapter(self)
        )

    __destroy__ = _DynamsoftUtility.delete_CProactiveImageSourceAdapter

    @abstractmethod
    def _fetch_image():
        """
        This method needs to be implemented in the derived class. It is called in a loop in the Fetching thread to obtain images.
        """
        pass

    def has_next_image_to_fetch(self) -> bool:
        """
        Determines whether there are more images left to fetch.
        
        Returns:
            True if there are more images left to fetch, false otherwise.
        """
        return _DynamsoftUtility.CProactiveImageSourceAdapter_HasNextImageToFetch(self)

    def set_image_fetch_interval(self, milliseconds: int) -> None:
        """
        Sets the time interval for the ImageSource to wait before attempting to fetch another image to put in the buffer.

        Args:
            milliseconds (int): Specifies the wait time in milliseconds. If setting to -1, the ImageSource does not proactively fetch images.
        """
        return _DynamsoftUtility.CProactiveImageSourceAdapter_SetImageFetchInterval(
            self, milliseconds
        )

    def get_image_fetch_interval(self) -> int:
        """
        Gets the time interval for the ImageSource to wait before attempting to fetch another image to put in the buffer.

        Returns:
            The wait time in milliseconds. If the value is -1, the ImageSource does not proactively fetch images.
        """
        return _DynamsoftUtility.CProactiveImageSourceAdapter_GetImageFetchInterval(
            self
        )

    def start_fetching(self) -> None:
        """
        Starts fetching images.
        """
        return _DynamsoftUtility.CProactiveImageSourceAdapter_StartFetching(self)

    def stop_fetching(self) -> None:
        """
        Stops fetching images.
        """
        return _DynamsoftUtility.CProactiveImageSourceAdapter_StopFetching(self)


_DynamsoftUtility.CProactiveImageSourceAdapter_register(ProactiveImageSourceAdapter)

class DirectoryFetcher(ProactiveImageSourceAdapter):
    """
    The DirectoryFetcher class is a utility class that retrieves a list of files from a specified directory based on certain criteria. It inherits from the ProactiveImageSourceAdapter class.

    Methods:
        set_directory(self, path: str, filter: str) -> Tuple[int, str]: Sets the directory path and filter for the file search.
        set_pdf_reading_parameter(self, para: PDFReadingParameter) -> Tuple[int, str]: Sets the parameters for reading PDF files.
        set_pages(self, pages: List[int]) -> Tuple[int, str]: Sets the 0-based page indexes of a file (.tiff or .pdf) for barcode searching.
        has_next_image_to_fetch(self) -> bool: Determines whether there are more images left to fetch.
    """
    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        _DynamsoftUtility.Class_init(
            self, _DynamsoftUtility.new_CDirectoryFetcher()
        )

    __destroy__ = _DynamsoftUtility.delete_CDirectoryFetcher

    def _fetch_image():
        pass
    def set_directory(self, *args) -> Tuple[int, str]:
        """
        Sets the directory path and filter for the file search.

        Args:
            path (str): The path of the directory to search.
            filter (str, optional): A string that specifies file extensions. For example: "*.BMP;*.JPG;*.GIF", or "*.*", etc. The default value is "*.bmp;*.jpg;*.jpeg;*.tif;*.png;*.tiff;*.gif;*.pdf".
            recursive (bool, optional): Specifies whether to load files recursively. The default value is False.
            
        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CDirectoryFetcher_SetDirectory(self, *args)

    def set_pdf_reading_parameter(self, para: PDFReadingParameter) -> Tuple[int, str]:
        """
        Sets the parameters for reading PDF files.

        Args:
            para (PDFReadingParameter): A PDFReadingParameter object with PDF files reading parameters.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CDirectoryFetcher_SetPDFReadingParameter(self, para)

    def has_next_image_to_fetch(self) -> bool:
        """
        Determines whether there are more images left to fetch.

        Returns:
            True if there are more images left to fetch, false otherwise.
        """
        return _DynamsoftUtility.CDirectoryFetcher_HasNextImageToFetch(self)

    def set_pages(self, pages: List[int]) -> Tuple[int, str]:
        """
        Sets the 0-based page indexes of a file (.tiff or .pdf). By default, there is no restriction on the number of pages that can be processed in a single file.

        Args:
            pages (List[int]): An integer list containing the page information to be set.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CDirectoryFetcher_SetPages(self, pages, len(pages))


_DynamsoftUtility.CDirectoryFetcher_register(DirectoryFetcher)


class FileFetcher(ImageSourceAdapter):
    """
    The FileFetcher class is a utility class that partitions a multi-page image file into multiple independent ImageData objects. It inherits from the ImageSourceAdapter class.

    Methods:
        set_file(self, path: str) -> Tuple[int, str]: Sets the file using a file path.
        set_pdf_reading_parameter(self, para: PDFReadingParameter) -> Tuple[int, str]: Sets the parameters for reading PDF files.
        set_pages(self, pages: List[int]) -> Tuple[int, str]: Sets the 0-based page indexes of a file (.tiff or .pdf) for barcode searching.
        has_next_image_to_fetch(self) -> bool: Determines whether there are more images left to fetch.
        get_image(self) -> ImageData: Gets the next image.
    """

    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def __init__(self):
        _DynamsoftUtility.Class_init(self, _DynamsoftUtility.new_CFileFetcher())

    __destroy__ = _DynamsoftUtility.delete_CFileFetcher

    def set_file(self, *args) -> Tuple[int, str]:
        """
        Sets the file using a file path, file bytes or an ImageData object.

        Args:
            A variable-length argument list. Can be one of the following:
            - file_path (str): Specifies the path of the file to process.
            - file_bytes (bytes): Specifies the image file bytes in memory to process.
            - image_data (ImageData): Specifies the image data to process.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CFileFetcher_SetFile(self, *args)

    def set_pdf_reading_parameter(self, para: PDFReadingParameter) -> Tuple[int, str]:
        """
        Sets the parameters for reading PDF files.

        Args:
            para (PDFReadingParameter): A PDFReadingParameter object with PDF files reading parameters.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CFileFetcher_SetPDFReadingParameter(self, para)

    def has_next_image_to_fetch(self) -> bool:
        """
        Determines whether there are more images left to fetch.

        Returns:
            True if there are more images left to fetch, False otherwise.
        """
        return _DynamsoftUtility.CFileFetcher_HasNextImageToFetch(self)

    def get_image(self) -> ImageData:
        """
        Gets the next image.

        Returns:
            The next image.
        """
        return _DynamsoftUtility.CFileFetcher_GetImage(self)

    def set_pages(self, pages: List[int]) -> Tuple[int, str]:
        """
        Sets the 0-based page indexes of a file (.tiff or .pdf). By default, there is no restriction on the number of pages that can be processed in a single file.

        Args:
            pages (List[int]): An integer list containing the page information to be set.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CFileFetcher_SetPages(self, pages, len(pages))


_DynamsoftUtility.CFileFetcher_register(FileFetcher)


class ImageManager:
    """
    The ImageManager class is a utility class for managing and manipulating images. It provides functionality for saving images to files and drawing various shapes on images.

    Methods:
        save_to_file(self, image_data: ImageData, path: str, overwrite: bool = True) -> Tuple[int, str]: Saves an image to a file.
        draw_on_image(self, *args) -> Tuple[int, str]: Draws an image on an image.
    """

    _thisown = property(
        lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag"
    )

    def save_to_file(
        self, image_data: ImageData, path: str, overwrite: bool = True
    ) -> Tuple[int, str]:
        """
        Saves an image to a file.

        Args:
            image_data (ImageData): The image data to be saved.
            path (str): The targeting file path with the file name and extension name.
            overwrite (bool, optional): A flag indicating whether to overwrite the file if it already exists. Defaults to true.

        Returns:
            A tuple containing following elements:
            - error_code <int>: The error code indicating the status of the operation.
            - error_message <str>: A descriptive message explaining the error.
        """
        return _DynamsoftUtility.CImageManager_SaveToFile(
            self, image_data, path, overwrite
        )

    def draw_on_image(self, *args):
        """
        Draws an image on an image.
        """
        return _DynamsoftUtility.CImageManager_DrawOnImage(self, *args)

    def __init__(self):
        _DynamsoftUtility.Class_init(
            self, _DynamsoftUtility.new_CImageManager()
        )

    __destroy__ = _DynamsoftUtility.delete_CImageManager


_DynamsoftUtility.CImageManager_register(ImageManager)
