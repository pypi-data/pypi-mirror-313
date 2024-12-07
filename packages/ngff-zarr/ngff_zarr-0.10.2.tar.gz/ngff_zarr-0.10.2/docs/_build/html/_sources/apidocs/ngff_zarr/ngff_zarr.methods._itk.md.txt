# {py:mod}`ngff_zarr.methods._itk`

```{py:module} ngff_zarr.methods._itk
```

```{autodoc2-docstring} ngff_zarr.methods._itk
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_compute_itk_gaussian_kernel_radius <ngff_zarr.methods._itk._compute_itk_gaussian_kernel_radius>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itk._compute_itk_gaussian_kernel_radius
    :summary:
    ```
* - {py:obj}`_itk_blur_and_downsample <ngff_zarr.methods._itk._itk_blur_and_downsample>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itk._itk_blur_and_downsample
    :summary:
    ```
* - {py:obj}`_downsample_itk_bin_shrink <ngff_zarr.methods._itk._downsample_itk_bin_shrink>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itk._downsample_itk_bin_shrink
    :summary:
    ```
* - {py:obj}`_downsample_itk_gaussian <ngff_zarr.methods._itk._downsample_itk_gaussian>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itk._downsample_itk_gaussian
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_image_dims <ngff_zarr.methods._itk._image_dims>`
  - ```{autodoc2-docstring} ngff_zarr.methods._itk._image_dims
    :summary:
    ```
````

### API

````{py:data} _image_dims
:canonical: ngff_zarr.methods._itk._image_dims
:type: typing.Tuple[str, str, str, str]
:value: >
   ('x', 'y', 'z', 't')

```{autodoc2-docstring} ngff_zarr.methods._itk._image_dims
```

````

````{py:function} _compute_itk_gaussian_kernel_radius(input_size, sigma_values) -> list
:canonical: ngff_zarr.methods._itk._compute_itk_gaussian_kernel_radius

```{autodoc2-docstring} ngff_zarr.methods._itk._compute_itk_gaussian_kernel_radius
```
````

````{py:function} _itk_blur_and_downsample(image_data, gaussian_filter_name, interpolator_name, shrink_factors, sigma_values, kernel_radius)
:canonical: ngff_zarr.methods._itk._itk_blur_and_downsample

```{autodoc2-docstring} ngff_zarr.methods._itk._itk_blur_and_downsample
```
````

````{py:function} _downsample_itk_bin_shrink(ngff_image: ngff_zarr.ngff_image.NgffImage, default_chunks, out_chunks, scale_factors)
:canonical: ngff_zarr.methods._itk._downsample_itk_bin_shrink

```{autodoc2-docstring} ngff_zarr.methods._itk._downsample_itk_bin_shrink
```
````

````{py:function} _downsample_itk_gaussian(ngff_image: ngff_zarr.ngff_image.NgffImage, default_chunks, out_chunks, scale_factors)
:canonical: ngff_zarr.methods._itk._downsample_itk_gaussian

```{autodoc2-docstring} ngff_zarr.methods._itk._downsample_itk_gaussian
```
````
