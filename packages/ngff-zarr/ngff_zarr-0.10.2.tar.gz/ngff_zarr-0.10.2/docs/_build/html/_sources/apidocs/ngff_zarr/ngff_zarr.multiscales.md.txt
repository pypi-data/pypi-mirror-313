# {py:mod}`ngff_zarr.multiscales`

```{py:module} ngff_zarr.multiscales
```

```{autodoc2-docstring} ngff_zarr.multiscales
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Multiscales <ngff_zarr.multiscales.Multiscales>`
  - ```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales
    :summary:
    ```
````

### API

`````{py:class} Multiscales
:canonical: ngff_zarr.multiscales.Multiscales

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales
```

````{py:attribute} images
:canonical: ngff_zarr.multiscales.Multiscales.images
:type: typing.List[ngff_zarr.ngff_image.NgffImage]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales.images
```

````

````{py:attribute} metadata
:canonical: ngff_zarr.multiscales.Multiscales.metadata
:type: ngff_zarr.zarr_metadata.Metadata
:value: >
   None

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales.metadata
```

````

````{py:attribute} scale_factors
:canonical: ngff_zarr.multiscales.Multiscales.scale_factors
:type: typing.Optional[typing.Sequence[typing.Union[typing.Dict[str, int], int]]]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales.scale_factors
```

````

````{py:attribute} method
:canonical: ngff_zarr.multiscales.Multiscales.method
:type: typing.Optional[ngff_zarr.methods.Methods]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales.method
```

````

````{py:attribute} chunks
:canonical: ngff_zarr.multiscales.Multiscales.chunks
:type: typing.Optional[typing.Union[int, typing.Tuple[int, ...], typing.Tuple[typing.Tuple[int, ...], ...], typing.Mapping[typing.Any, typing.Union[None, int, typing.Tuple[int, ...]]]]]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.multiscales.Multiscales.chunks
```

````

`````
