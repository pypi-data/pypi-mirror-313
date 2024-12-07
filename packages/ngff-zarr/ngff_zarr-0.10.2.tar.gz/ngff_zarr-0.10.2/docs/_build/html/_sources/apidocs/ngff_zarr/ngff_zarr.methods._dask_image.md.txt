# {py:mod}`ngff_zarr.methods._dask_image`

```{py:module} ngff_zarr.methods._dask_image
```

```{autodoc2-docstring} ngff_zarr.methods._dask_image
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_compute_next_scale <ngff_zarr.methods._dask_image._compute_next_scale>`
  - ```{autodoc2-docstring} ngff_zarr.methods._dask_image._compute_next_scale
    :summary:
    ```
* - {py:obj}`_compute_next_translation <ngff_zarr.methods._dask_image._compute_next_translation>`
  - ```{autodoc2-docstring} ngff_zarr.methods._dask_image._compute_next_translation
    :summary:
    ```
* - {py:obj}`_get_truncate <ngff_zarr.methods._dask_image._get_truncate>`
  - ```{autodoc2-docstring} ngff_zarr.methods._dask_image._get_truncate
    :summary:
    ```
* - {py:obj}`_downsample_dask_image <ngff_zarr.methods._dask_image._downsample_dask_image>`
  - ```{autodoc2-docstring} ngff_zarr.methods._dask_image._downsample_dask_image
    :summary:
    ```
````

### API

````{py:function} _compute_next_scale(previous_image: ngff_zarr.ngff_image.NgffImage, dim_factors)
:canonical: ngff_zarr.methods._dask_image._compute_next_scale

```{autodoc2-docstring} ngff_zarr.methods._dask_image._compute_next_scale
```
````

````{py:function} _compute_next_translation(previous_image, dim_factors)
:canonical: ngff_zarr.methods._dask_image._compute_next_translation

```{autodoc2-docstring} ngff_zarr.methods._dask_image._compute_next_translation
```
````

````{py:function} _get_truncate(previous_image, sigma_values, truncate_start=4.0) -> float
:canonical: ngff_zarr.methods._dask_image._get_truncate

```{autodoc2-docstring} ngff_zarr.methods._dask_image._get_truncate
```
````

````{py:function} _downsample_dask_image(ngff_image: ngff_zarr.ngff_image.NgffImage, default_chunks, out_chunks, scale_factors, label=False)
:canonical: ngff_zarr.methods._dask_image._downsample_dask_image

```{autodoc2-docstring} ngff_zarr.methods._dask_image._downsample_dask_image
```
````
