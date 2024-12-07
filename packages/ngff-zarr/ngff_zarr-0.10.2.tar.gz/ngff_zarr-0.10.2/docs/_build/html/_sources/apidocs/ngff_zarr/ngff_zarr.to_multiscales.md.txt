# {py:mod}`ngff_zarr.to_multiscales`

```{py:module} ngff_zarr.to_multiscales
```

```{autodoc2-docstring} ngff_zarr.to_multiscales
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_ngff_image_scale_factors <ngff_zarr.to_multiscales._ngff_image_scale_factors>`
  - ```{autodoc2-docstring} ngff_zarr.to_multiscales._ngff_image_scale_factors
    :summary:
    ```
* - {py:obj}`_large_image_serialization <ngff_zarr.to_multiscales._large_image_serialization>`
  - ```{autodoc2-docstring} ngff_zarr.to_multiscales._large_image_serialization
    :summary:
    ```
* - {py:obj}`to_multiscales <ngff_zarr.to_multiscales.to_multiscales>`
  - ```{autodoc2-docstring} ngff_zarr.to_multiscales.to_multiscales
    :summary:
    ```
````

### API

````{py:function} _ngff_image_scale_factors(ngff_image, min_length, out_chunks)
:canonical: ngff_zarr.to_multiscales._ngff_image_scale_factors

```{autodoc2-docstring} ngff_zarr.to_multiscales._ngff_image_scale_factors
```
````

````{py:function} _large_image_serialization(image: ngff_zarr.ngff_image.NgffImage, progress: typing.Optional[typing.Union[ngff_zarr.rich_dask_progress.NgffProgress, ngff_zarr.rich_dask_progress.NgffProgressCallback]])
:canonical: ngff_zarr.to_multiscales._large_image_serialization

```{autodoc2-docstring} ngff_zarr.to_multiscales._large_image_serialization
```
````

````{py:function} to_multiscales(data: typing.Union[ngff_zarr.ngff_image.NgffImage, numpy.typing.ArrayLike, collections.abc.MutableMapping, str, zarr.core.Array], scale_factors: typing.Union[int, typing.Sequence[typing.Union[typing.Dict[str, int], int]]] = 128, method: typing.Optional[ngff_zarr.methods.Methods] = None, chunks: typing.Optional[typing.Union[int, typing.Tuple[int, ...], typing.Tuple[typing.Tuple[int, ...], ...], typing.Mapping[typing.Any, typing.Union[None, int, typing.Tuple[int, ...]]]]] = None, progress: typing.Optional[typing.Union[ngff_zarr.rich_dask_progress.NgffProgress, ngff_zarr.rich_dask_progress.NgffProgressCallback]] = None, cache: typing.Optional[bool] = None) -> ngff_zarr.multiscales.Multiscales
:canonical: ngff_zarr.to_multiscales.to_multiscales

```{autodoc2-docstring} ngff_zarr.to_multiscales.to_multiscales
```
````
