from mltraq.utils.base_options import BaseOptions


class Options(BaseOptions):
    """
    Package options.
    """

    default_values = {
        "reproducibility": {"random_seed": 123},
    }


def options() -> BaseOptions:
    """
    Returns singleton object of options.
    """

    return Options.instance()
