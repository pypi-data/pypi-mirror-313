# {py:mod}`ngff_zarr.validate`

```{py:module} ngff_zarr.validate
```

```{autodoc2-docstring} ngff_zarr.validate
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load_schema <ngff_zarr.validate.load_schema>`
  - ```{autodoc2-docstring} ngff_zarr.validate.load_schema
    :summary:
    ```
* - {py:obj}`validate <ngff_zarr.validate.validate>`
  - ```{autodoc2-docstring} ngff_zarr.validate.validate
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`NGFF_URI <ngff_zarr.validate.NGFF_URI>`
  - ```{autodoc2-docstring} ngff_zarr.validate.NGFF_URI
    :summary:
    ```
````

### API

````{py:data} NGFF_URI
:canonical: ngff_zarr.validate.NGFF_URI
:value: >
   'https://ngff.openmicroscopy.org'

```{autodoc2-docstring} ngff_zarr.validate.NGFF_URI
```

````

````{py:function} load_schema(version: str = '0.4', model: str = 'image', strict: bool = False) -> typing.Dict
:canonical: ngff_zarr.validate.load_schema

```{autodoc2-docstring} ngff_zarr.validate.load_schema
```
````

````{py:function} validate(ngff_dict: typing.Dict, version: str = '0.4', model: str = 'image', strict: bool = False)
:canonical: ngff_zarr.validate.validate

```{autodoc2-docstring} ngff_zarr.validate.validate
```
````
