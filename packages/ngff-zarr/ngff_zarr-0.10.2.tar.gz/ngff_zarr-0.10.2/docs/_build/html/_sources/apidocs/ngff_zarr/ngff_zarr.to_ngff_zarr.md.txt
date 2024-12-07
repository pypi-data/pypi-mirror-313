# {py:mod}`ngff_zarr.to_ngff_zarr`

```{py:module} ngff_zarr.to_ngff_zarr
```

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_pop_metadata_optionals <ngff_zarr.to_ngff_zarr._pop_metadata_optionals>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._pop_metadata_optionals
    :summary:
    ```
* - {py:obj}`_prep_for_to_zarr <ngff_zarr.to_ngff_zarr._prep_for_to_zarr>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._prep_for_to_zarr
    :summary:
    ```
* - {py:obj}`to_ngff_zarr <ngff_zarr.to_ngff_zarr.to_ngff_zarr>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.to_ngff_zarr
    :summary:
    ```
````

### API

````{py:function} _pop_metadata_optionals(metadata_dict)
:canonical: ngff_zarr.to_ngff_zarr._pop_metadata_optionals

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._pop_metadata_optionals
```
````

````{py:function} _prep_for_to_zarr(store: typing.Union[collections.abc.MutableMapping, str, pathlib.Path, zarr.storage.BaseStore], arr: dask.array.Array) -> dask.array.Array
:canonical: ngff_zarr.to_ngff_zarr._prep_for_to_zarr

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._prep_for_to_zarr
```
````

````{py:function} to_ngff_zarr(store: typing.Union[collections.abc.MutableMapping, str, pathlib.Path, zarr.storage.BaseStore], multiscales: ngff_zarr.multiscales.Multiscales, overwrite: bool = True, chunk_store: typing.Optional[typing.Union[collections.abc.MutableMapping, str, pathlib.Path, zarr.storage.BaseStore]] = None, progress: typing.Optional[typing.Union[ngff_zarr.rich_dask_progress.NgffProgress, ngff_zarr.rich_dask_progress.NgffProgressCallback]] = None, **kwargs) -> None
:canonical: ngff_zarr.to_ngff_zarr.to_ngff_zarr

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.to_ngff_zarr
```
````
