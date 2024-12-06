__version__ = "1.2.30.5764"

if __package__ or "." in __name__:
    from . import _DynamsoftCodeParserDedicator
else:
    import _DynamsoftCodeParserDedicator


class DynamsoftCodeParserDedicatorModule:
    """
    The DynamsoftCodeParserDedicatorModule class represents the Dynamsoft Code Parser Dedicator module.
    """
    @staticmethod
    def get_version() -> str:
        """
        Gets the version of the Dynamsoft Code Parser Dedicator module.

        Returns:
            A string representing the version of the Dynamsoft Code Parser Dedicator module.
        """
        return __version__ + " (Algotithm " + _DynamsoftCodeParserDedicator.getversion() + ")"
