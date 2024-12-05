"""General utils"""

from functools import partial
import re

from dol import (
    TextFiles,
    wrap_kvs,
    filt_iter,
    invertible_maps,
    add_ipython_key_completions,
)

try:
    import importlib.resources

    _files = importlib.resources.files  # only valid in 3.9+
except AttributeError:
    import importlib_resources  # needs pip install

    _files = importlib_resources.files

files = _files("jy")
# data_dir = files / 'data'
# data_dir_path = str(data_dir)
js_dir = files / "js"
js_dir_path = str(js_dir)


@add_ipython_key_completions
@wrap_kvs(key_of_id=lambda x: x[: -len(".js")], id_of_key=lambda x: x + ".js")
@filt_iter(filt=lambda x: x.endswith(".js"))
class JsFiles(TextFiles):
    """A store of js files"""


_replace_non_alphanumerics_by_underscore = partial(re.compile(r"\W").sub, "_")


# Note: js_files_as_attrs is not used in the module, but can be useful when working
# in a notebook, or console, where we might want the convenience of tab-completion of
# attributes
def js_files_as_attrs(rootdir):
    """
    Will make a JsFiles, but where the keys are available as attributes.
    To do so, any non alphanumerics of file name are replaced with underscore,
    and there can be no two files that collide with that key transformation!
    """
    from dol.sources import AttrContainer

    s = JsFiles(rootdir)
    key_for_id = {id_: _replace_non_alphanumerics_by_underscore(id_) for id_ in s}
    key_for_id, id_for_key = invertible_maps(key_for_id)
    return AttrContainer(
        **wrap_kvs(s, key_of_id=key_for_id.get, id_of_key=id_for_key.get)
    )


# Note: Could replace with js_files_as_attrs, but not sure if it's worth it
mk_js_files = JsFiles

js_files = mk_js_files(str(js_dir_path))
