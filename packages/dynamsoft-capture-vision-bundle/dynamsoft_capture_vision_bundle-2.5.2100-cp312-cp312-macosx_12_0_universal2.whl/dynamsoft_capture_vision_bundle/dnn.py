__version__ = "1.0.20.5764"

if __package__ or "." in __name__:
    from . import _DynamsoftNeuralNetwork
else:
    import _DynamsoftNeuralNetwork


class DynamsoftNeuralNetworkModule:
    """
    The DynamsoftNeuralNetworkModule class represents the Dynamsoft Neural Network module.

    Methods:
        get_version() -> str: Gets the version of the Dynamsoft Neural Network module.
    """
    @staticmethod
    def get_version() -> str:
        """
        Gets the version of the Dynamsoft Neural Network module.

        Returns:
            A string representing the version of the Dynamsoft Neural Network module.
        """
        return __version__ + " (Algotithm " + _DynamsoftNeuralNetwork.getversion() + ")"
