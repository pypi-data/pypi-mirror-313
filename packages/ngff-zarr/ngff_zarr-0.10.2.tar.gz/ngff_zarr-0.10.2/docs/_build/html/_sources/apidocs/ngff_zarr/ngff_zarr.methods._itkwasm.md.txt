# {py:mod}`ngff_zarr.methods._itkwasm`

```{py:module} ngff_zarr.methods._itkwasm
```

```{autodoc2-docstring} ngff_zarr.methods._itkwasm
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_itkwasm_blur_and_downsample <ngff_zarr.methods._itkwasm._itkwasm_blur_and_downsample>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itkwasm._itkwasm_blur_and_downsample
    :summary:
    ```
* - {py:obj}`_itkwasm_chunk_bin_shrink <ngff_zarr.methods._itkwasm._itkwasm_chunk_bin_shrink>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itkwasm._itkwasm_chunk_bin_shrink
    :summary:
    ```
* - {py:obj}`_downsample_itkwasm_bin_shrink <ngff_zarr.methods._itkwasm._downsample_itkwasm_bin_shrink>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itkwasm._downsample_itkwasm_bin_shrink
    :summary:
    ```
* - {py:obj}`_downsample_itkwasm <ngff_zarr.methods._itkwasm._downsample_itkwasm>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itkwasm._downsample_itkwasm
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_image_dims <ngff_zarr.methods._itkwasm._image_dims>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itkwasm._image_dims
    :summary:
    ```
````

### API

````{py:data} _image_dims
:canonical: ngff_zarr.methods._itkwasm._image_dims
:type: typing.Tuple[str, str, str, str]
:value: >
   ('x', 'y', 'z', 't')

```{autodoc2-docstring} ngff_zarr.methods._itkwasm._image_dims
```

````

````{py:function} _itkwasm_blur_and_downsample(image_data, shrink_factors, kernel_radius, smoothing)
:canonical: ngff_zarr.methods._itkwasm._itkwasm_blur_and_downsample

```{autodoc2-docstring} ngff_zarr.methods._itkwasm._itkwasm_blur_and_downsample
```
````

````{py:function} _itkwasm_chunk_bin_shrink(image_data, shrink_factors)
:canonical: ngff_zarr.methods._itkwasm._itkwasm_chunk_bin_shrink

```{autodoc2-docstring} ngff_zarr.methods._itkwasm._itkwasm_chunk_bin_shrink
```
````

````{py:function} _downsample_itkwasm_bin_shrink(ngff_image: ngff_zarr.ngff_image.NgffImage, default_chunks, out_chunks, scale_factors)
:canonical: ngff_zarr.methods._itkwasm._downsample_itkwasm_bin_shrink

```{autodoc2-docstring} ngff_zarr.methods._itkwasm._downsample_itkwasm_bin_shrink
```
````

````{py:function} _downsample_itkwasm(ngff_image: ngff_zarr.ngff_image.NgffImage, default_chunks, out_chunks, scale_factors, smoothing)
:canonical: ngff_zarr.methods._itkwasm._downsample_itkwasm

```{autodoc2-docstring} ngff_zarr.methods._itkwasm._downsample_itkwasm
```
````
