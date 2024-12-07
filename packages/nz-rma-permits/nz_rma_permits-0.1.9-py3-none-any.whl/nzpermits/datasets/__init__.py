import os


__all__ = ['available', 'get_path']

_module_path = os.path.dirname(__file__)
_available_dir = [p for p in next(os.walk(_module_path))[1]
                  if not p.startswith('__')]
_shp_dir_files = os.listdir(os.path.join(_module_path, 'shapefiles'))
_available_shp = {p.split('.')[0]: p for p in _shp_dir_files if p.endswith('.shp')}
available = list(_available_shp.keys())


def get_path(dataset):
    """
    Get the path to the data file.
    Parameters
    ----------
    dataset : str
        The name of the dataset. See ``geopandas.datasets.available`` for
        all options.
    """
    if dataset in _available_shp:
        return os.path.abspath(
            os.path.join(_module_path, 'shapefiles', _available_shp[dataset]))
    else:
        msg = "The dataset '{data}' is not available. ".format(data=dataset)
        msg += "Available datasets are {}".format(", ".join(available))
        raise ValueError(msg)
