# {py:mod}`ngff_zarr.detect_cli_io_backend`

```{py:module} ngff_zarr.detect_cli_io_backend
```

```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`detect_cli_io_backend <ngff_zarr.detect_cli_io_backend.detect_cli_io_backend>`
  - ```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.detect_cli_io_backend
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`conversion_backends <ngff_zarr.detect_cli_io_backend.conversion_backends>`
  - ```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.conversion_backends
    :summary:
    ```
* - {py:obj}`conversion_backends_values <ngff_zarr.detect_cli_io_backend.conversion_backends_values>`
  - ```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.conversion_backends_values
    :summary:
    ```
* - {py:obj}`ConversionBackend <ngff_zarr.detect_cli_io_backend.ConversionBackend>`
  - ```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.ConversionBackend
    :summary:
    ```
````

### API

````{py:data} conversion_backends
:canonical: ngff_zarr.detect_cli_io_backend.conversion_backends
:value: >
   [('NGFF_ZARR', 'ngff_zarr'), ('ZARR_ARRAY', 'zarr'), ('ITKWASM', 'itkwasm_image_io'), ('ITK', 'itk')...

```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.conversion_backends
```

````

````{py:data} conversion_backends_values
:canonical: ngff_zarr.detect_cli_io_backend.conversion_backends_values
:value: >
   None

```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.conversion_backends_values
```

````

````{py:data} ConversionBackend
:canonical: ngff_zarr.detect_cli_io_backend.ConversionBackend
:value: >
   'Enum(...)'

```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.ConversionBackend
```

````

````{py:function} detect_cli_io_backend(input: typing.List[str]) -> ngff_zarr.detect_cli_io_backend.ConversionBackend
:canonical: ngff_zarr.detect_cli_io_backend.detect_cli_io_backend

```{autodoc2-docstring} ngff_zarr.detect_cli_io_backend.detect_cli_io_backend
```
````
