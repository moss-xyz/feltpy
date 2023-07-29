## FeltPy

_feltpy_ is a lightweight Python package to interact with the [public API](https://feltmaps.notion.site/Felt-Public-API-reference-c01e0e6b0d954a678c608131b894e8e1#bfdcdfabab0b4d9ba4e0b6fbcf04ce04) of [Felt.com](www.felt.com). 

### Installation

This package is available in PyPI, and can be installed like so:
```bash
pip install feltpy
```

Once installed, import the package with
```python
import feltpy
```

This package only requires a few packages, most of which come with a default installation of Python, namely:
- re
- os
- [requests](https://github.com/psf/requests)
- [geopandas](https://github.com/geopandas/geopandas)

I've only tested this on Python 3.10, but it will presumably work with older version of Python 3!

### Set-Up

All functions in this package are only set up, currently, to work with Felt's __Personal Access Tokens__, which must be acquired ahead of time. More information on doing so can be found on [Felt's API documentation](https://feltmaps.notion.site/Felt-Public-API-reference-c01e0e6b0d954a678c608131b894e8e1#065791134e0c4d82b156d97db3f663a5).

### Features

As of 2023-07-28, this package can use the API to:
- Create a new map
- Upload data as a layer to a map, either from a file, a URL, or a Geopandas GeoDataFrame
- Query the current layers, elements, and comments on a map
- Update layer descriptions
- Delete layers and maps

This package works through a collection of __functions__ and __classes__. 
- __functions__, with names such as _getLayers()_ and _deleteMap()_, perform actions, such as those listed above
- __classes__ can be thought of as __objects__, each one representing something that currently exists on Felt, such as a _Map_, a _Layer_, a _Layer Collection_ (i.e. all the layers on a map), and _Datasets_ (i.e. what data "powers" a layer - not so useful at the moment)
  - _Map_ and _Layer_ also have __methods__ within them that allow for easier calling of __functions__ - for example, a layer could be deleted by either calling the function _deleteLayer()_, or by calling _Layer.deleteLayer()_

### Future Work

As of 2023-07-28, this package does __not__ interact with any API functions that deal with the Felt Style Language. This is out of practicality: the API documentation states that these endpoints might change in the future, and I would rather wait for it to be finalized before devoting time to figuring it out

This package could also be extended to be more "helpful" - for instance, confirming that a layer or map is deleted, or enabling more complex functinos, such as creating a new map __and__ loading data to it

Finally, this package is only set up to work with Felt's Personal Access Tokens - I hope at some point to also integrate with OAuth

### Contribution

I welcome comments and pull requests! This is my first Python package, so it is definitely not consistent or pretty or easy to understand - if you have capital-O __Opinions__ on how you'd like to see this change, feel free to let me know here in Github.
