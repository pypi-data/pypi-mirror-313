import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _gd_datatable = components.declare_component(
        "gd_datatable",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _gd_datatable = components.declare_component("gd_datatable", path=build_dir)


def gd_datatable(data, id_column, key=None, **kwargs):
    return _gd_datatable(
        data=data,
        default=[],
        key=key,
        id_column=id_column,
        **kwargs
    )
