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
* - {py:obj}`_numpy_to_zarr_dtype <ngff_zarr.to_ngff_zarr._numpy_to_zarr_dtype>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._numpy_to_zarr_dtype
    :summary:
    ```
* - {py:obj}`_write_with_tensorstore <ngff_zarr.to_ngff_zarr._write_with_tensorstore>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._write_with_tensorstore
    :summary:
    ```
* - {py:obj}`to_ngff_zarr <ngff_zarr.to_ngff_zarr.to_ngff_zarr>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.to_ngff_zarr
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`zarr_version <ngff_zarr.to_ngff_zarr.zarr_version>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.zarr_version
    :summary:
    ```
* - {py:obj}`zarr_version_major <ngff_zarr.to_ngff_zarr.zarr_version_major>`
  - ```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.zarr_version_major
    :summary:
    ```
````

### API

````{py:data} zarr_version
:canonical: ngff_zarr.to_ngff_zarr.zarr_version
:value: >
   'parse(...)'

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.zarr_version
```

````

````{py:data} zarr_version_major
:canonical: ngff_zarr.to_ngff_zarr.zarr_version_major
:value: >
   None

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.zarr_version_major
```

````

````{py:function} _pop_metadata_optionals(metadata_dict)
:canonical: ngff_zarr.to_ngff_zarr._pop_metadata_optionals

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._pop_metadata_optionals
```
````

````{py:function} _prep_for_to_zarr(store: ngff_zarr.to_ngff_zarr.StoreLike, arr: dask.array.Array) -> dask.array.Array
:canonical: ngff_zarr.to_ngff_zarr._prep_for_to_zarr

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._prep_for_to_zarr
```
````

````{py:function} _numpy_to_zarr_dtype(dtype)
:canonical: ngff_zarr.to_ngff_zarr._numpy_to_zarr_dtype

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._numpy_to_zarr_dtype
```
````

````{py:function} _write_with_tensorstore(store_path: str, array, region, chunks, zarr_format) -> None
:canonical: ngff_zarr.to_ngff_zarr._write_with_tensorstore

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr._write_with_tensorstore
```
````

````{py:function} to_ngff_zarr(store: ngff_zarr.to_ngff_zarr.StoreLike, multiscales: ngff_zarr.multiscales.Multiscales, version: str = '0.4', overwrite: bool = True, use_tensorstore: bool = False, chunk_store: typing.Optional[ngff_zarr.to_ngff_zarr.StoreLike] = None, progress: typing.Optional[typing.Union[ngff_zarr.rich_dask_progress.NgffProgress, ngff_zarr.rich_dask_progress.NgffProgressCallback]] = None, **kwargs) -> None
:canonical: ngff_zarr.to_ngff_zarr.to_ngff_zarr

```{autodoc2-docstring} ngff_zarr.to_ngff_zarr.to_ngff_zarr
```
````
