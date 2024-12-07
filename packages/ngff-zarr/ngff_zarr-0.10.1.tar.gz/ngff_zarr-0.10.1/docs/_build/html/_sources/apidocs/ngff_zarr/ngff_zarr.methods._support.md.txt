# {py:mod}`ngff_zarr.methods._support`

```{py:module} ngff_zarr.methods._support
```

```{autodoc2-docstring} ngff_zarr.methods._support
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_dim_scale_factors <ngff_zarr.methods._support._dim_scale_factors>`
  - ```{autodoc2-docstring} ngff_zarr.methods._support._dim_scale_factors
    :summary:
    ```
* - {py:obj}`_align_chunks <ngff_zarr.methods._support._align_chunks>`
  - ```{autodoc2-docstring} ngff_zarr.methods._support._align_chunks
    :summary:
    ```
* - {py:obj}`_compute_sigma <ngff_zarr.methods._support._compute_sigma>`
  - ```{autodoc2-docstring} ngff_zarr.methods._support._compute_sigma
    :summary:
    ```
* - {py:obj}`_get_block <ngff_zarr.methods._support._get_block>`
  - ```{autodoc2-docstring} ngff_zarr.methods._support._get_block
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_spatial_dims <ngff_zarr.methods._support._spatial_dims>`
  - ```{autodoc2-docstring} ngff_zarr.methods._support._spatial_dims
    :summary:
    ```
````

### API

````{py:data} _spatial_dims
:canonical: ngff_zarr.methods._support._spatial_dims
:value: >
   None

```{autodoc2-docstring} ngff_zarr.methods._support._spatial_dims
```

````

````{py:function} _dim_scale_factors(dims, scale_factor, previous_dim_factors)
:canonical: ngff_zarr.methods._support._dim_scale_factors

```{autodoc2-docstring} ngff_zarr.methods._support._dim_scale_factors
```
````

````{py:function} _align_chunks(previous_image, default_chunks, dim_factors)
:canonical: ngff_zarr.methods._support._align_chunks

```{autodoc2-docstring} ngff_zarr.methods._support._align_chunks
```
````

````{py:function} _compute_sigma(shrink_factors: typing.List[int]) -> typing.List[float]
:canonical: ngff_zarr.methods._support._compute_sigma

```{autodoc2-docstring} ngff_zarr.methods._support._compute_sigma
```
````

````{py:function} _get_block(previous_image: ngff_zarr.ngff_image.NgffImage, block_index: int)
:canonical: ngff_zarr.methods._support._get_block

```{autodoc2-docstring} ngff_zarr.methods._support._get_block
```
````
