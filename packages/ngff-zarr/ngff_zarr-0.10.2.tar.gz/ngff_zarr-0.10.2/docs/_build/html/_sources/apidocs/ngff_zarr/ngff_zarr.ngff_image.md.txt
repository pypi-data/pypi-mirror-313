# {py:mod}`ngff_zarr.ngff_image`

```{py:module} ngff_zarr.ngff_image
```

```{autodoc2-docstring} ngff_zarr.ngff_image
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`NgffImage <ngff_zarr.ngff_image.NgffImage>`
  - ```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ComputedCallback <ngff_zarr.ngff_image.ComputedCallback>`
  - ```{autodoc2-docstring} ngff_zarr.ngff_image.ComputedCallback
    :summary:
    ```
````

### API

````{py:data} ComputedCallback
:canonical: ngff_zarr.ngff_image.ComputedCallback
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.ComputedCallback
```

````

`````{py:class} NgffImage
:canonical: ngff_zarr.ngff_image.NgffImage

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage
```

````{py:attribute} data
:canonical: ngff_zarr.ngff_image.NgffImage.data
:type: dask.array.core.Array
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.data
```

````

````{py:attribute} dims
:canonical: ngff_zarr.ngff_image.NgffImage.dims
:type: typing.Sequence[str]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.dims
```

````

````{py:attribute} scale
:canonical: ngff_zarr.ngff_image.NgffImage.scale
:type: typing.Dict[str, float]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.scale
```

````

````{py:attribute} translation
:canonical: ngff_zarr.ngff_image.NgffImage.translation
:type: typing.Dict[str, float]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.translation
```

````

````{py:attribute} name
:canonical: ngff_zarr.ngff_image.NgffImage.name
:type: str
:value: >
   'image'

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.name
```

````

````{py:attribute} axes_units
:canonical: ngff_zarr.ngff_image.NgffImage.axes_units
:type: typing.Optional[typing.Mapping[str, ngff_zarr.zarr_metadata.Units]]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.axes_units
```

````

````{py:attribute} computed_callbacks
:canonical: ngff_zarr.ngff_image.NgffImage.computed_callbacks
:type: typing.List[ngff_zarr.ngff_image.ComputedCallback]
:value: >
   'field(...)'

```{autodoc2-docstring} ngff_zarr.ngff_image.NgffImage.computed_callbacks
```

````

`````
