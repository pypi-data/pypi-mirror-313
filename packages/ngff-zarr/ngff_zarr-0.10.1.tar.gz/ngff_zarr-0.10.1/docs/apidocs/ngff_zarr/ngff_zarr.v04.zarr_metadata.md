# {py:mod}`ngff_zarr.v04.zarr_metadata`

```{py:module} ngff_zarr.v04.zarr_metadata
```

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Axis <ngff_zarr.v04.zarr_metadata.Axis>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Axis
    :summary:
    ```
* - {py:obj}`Identity <ngff_zarr.v04.zarr_metadata.Identity>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Identity
    :summary:
    ```
* - {py:obj}`Scale <ngff_zarr.v04.zarr_metadata.Scale>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Scale
    :summary:
    ```
* - {py:obj}`Translation <ngff_zarr.v04.zarr_metadata.Translation>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Translation
    :summary:
    ```
* - {py:obj}`Dataset <ngff_zarr.v04.zarr_metadata.Dataset>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Dataset
    :summary:
    ```
* - {py:obj}`Metadata <ngff_zarr.v04.zarr_metadata.Metadata>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`is_dimension_supported <ngff_zarr.v04.zarr_metadata.is_dimension_supported>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.is_dimension_supported
    :summary:
    ```
* - {py:obj}`is_unit_supported <ngff_zarr.v04.zarr_metadata.is_unit_supported>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.is_unit_supported
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SupportedDims <ngff_zarr.v04.zarr_metadata.SupportedDims>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SupportedDims
    :summary:
    ```
* - {py:obj}`SpatialDims <ngff_zarr.v04.zarr_metadata.SpatialDims>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SpatialDims
    :summary:
    ```
* - {py:obj}`AxesType <ngff_zarr.v04.zarr_metadata.AxesType>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.AxesType
    :summary:
    ```
* - {py:obj}`SpaceUnits <ngff_zarr.v04.zarr_metadata.SpaceUnits>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SpaceUnits
    :summary:
    ```
* - {py:obj}`TimeUnits <ngff_zarr.v04.zarr_metadata.TimeUnits>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.TimeUnits
    :summary:
    ```
* - {py:obj}`Units <ngff_zarr.v04.zarr_metadata.Units>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Units
    :summary:
    ```
* - {py:obj}`supported_dims <ngff_zarr.v04.zarr_metadata.supported_dims>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.supported_dims
    :summary:
    ```
* - {py:obj}`space_units <ngff_zarr.v04.zarr_metadata.space_units>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.space_units
    :summary:
    ```
* - {py:obj}`time_units <ngff_zarr.v04.zarr_metadata.time_units>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.time_units
    :summary:
    ```
* - {py:obj}`Transform <ngff_zarr.v04.zarr_metadata.Transform>`
  - ```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Transform
    :summary:
    ```
````

### API

````{py:data} SupportedDims
:canonical: ngff_zarr.v04.zarr_metadata.SupportedDims
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SupportedDims
```

````

````{py:data} SpatialDims
:canonical: ngff_zarr.v04.zarr_metadata.SpatialDims
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SpatialDims
```

````

````{py:data} AxesType
:canonical: ngff_zarr.v04.zarr_metadata.AxesType
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.AxesType
```

````

````{py:data} SpaceUnits
:canonical: ngff_zarr.v04.zarr_metadata.SpaceUnits
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.SpaceUnits
```

````

````{py:data} TimeUnits
:canonical: ngff_zarr.v04.zarr_metadata.TimeUnits
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.TimeUnits
```

````

````{py:data} Units
:canonical: ngff_zarr.v04.zarr_metadata.Units
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Units
```

````

````{py:data} supported_dims
:canonical: ngff_zarr.v04.zarr_metadata.supported_dims
:value: >
   ['x', 'y', 'z', 'c', 't']

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.supported_dims
```

````

````{py:data} space_units
:canonical: ngff_zarr.v04.zarr_metadata.space_units
:value: >
   ['angstrom', 'attometer', 'centimeter', 'decimeter', 'exameter', 'femtometer', 'foot', 'gigameter', ...

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.space_units
```

````

````{py:data} time_units
:canonical: ngff_zarr.v04.zarr_metadata.time_units
:value: >
   ['attosecond', 'centisecond', 'day', 'decisecond', 'exasecond', 'femtosecond', 'gigasecond', 'hectos...

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.time_units
```

````

````{py:function} is_dimension_supported(dim: str) -> bool
:canonical: ngff_zarr.v04.zarr_metadata.is_dimension_supported

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.is_dimension_supported
```
````

````{py:function} is_unit_supported(unit: str) -> bool
:canonical: ngff_zarr.v04.zarr_metadata.is_unit_supported

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.is_unit_supported
```
````

`````{py:class} Axis
:canonical: ngff_zarr.v04.zarr_metadata.Axis

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Axis
```

````{py:attribute} name
:canonical: ngff_zarr.v04.zarr_metadata.Axis.name
:type: ngff_zarr.v04.zarr_metadata.SupportedDims
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Axis.name
```

````

````{py:attribute} type
:canonical: ngff_zarr.v04.zarr_metadata.Axis.type
:type: ngff_zarr.v04.zarr_metadata.AxesType
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Axis.type
```

````

````{py:attribute} unit
:canonical: ngff_zarr.v04.zarr_metadata.Axis.unit
:type: typing.Optional[ngff_zarr.v04.zarr_metadata.Units]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Axis.unit
```

````

`````

`````{py:class} Identity
:canonical: ngff_zarr.v04.zarr_metadata.Identity

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Identity
```

````{py:attribute} type
:canonical: ngff_zarr.v04.zarr_metadata.Identity.type
:type: str
:value: >
   'identity'

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Identity.type
```

````

`````

`````{py:class} Scale
:canonical: ngff_zarr.v04.zarr_metadata.Scale

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Scale
```

````{py:attribute} scale
:canonical: ngff_zarr.v04.zarr_metadata.Scale.scale
:type: typing.List[float]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Scale.scale
```

````

````{py:attribute} type
:canonical: ngff_zarr.v04.zarr_metadata.Scale.type
:type: str
:value: >
   'scale'

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Scale.type
```

````

`````

`````{py:class} Translation
:canonical: ngff_zarr.v04.zarr_metadata.Translation

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Translation
```

````{py:attribute} translation
:canonical: ngff_zarr.v04.zarr_metadata.Translation.translation
:type: typing.List[float]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Translation.translation
```

````

````{py:attribute} type
:canonical: ngff_zarr.v04.zarr_metadata.Translation.type
:type: str
:value: >
   'translation'

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Translation.type
```

````

`````

````{py:data} Transform
:canonical: ngff_zarr.v04.zarr_metadata.Transform
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Transform
```

````

`````{py:class} Dataset
:canonical: ngff_zarr.v04.zarr_metadata.Dataset

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Dataset
```

````{py:attribute} path
:canonical: ngff_zarr.v04.zarr_metadata.Dataset.path
:type: str
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Dataset.path
```

````

````{py:attribute} coordinateTransformations
:canonical: ngff_zarr.v04.zarr_metadata.Dataset.coordinateTransformations
:type: typing.List[ngff_zarr.v04.zarr_metadata.Transform]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Dataset.coordinateTransformations
```

````

`````

`````{py:class} Metadata
:canonical: ngff_zarr.v04.zarr_metadata.Metadata

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata
```

````{py:attribute} axes
:canonical: ngff_zarr.v04.zarr_metadata.Metadata.axes
:type: typing.List[ngff_zarr.v04.zarr_metadata.Axis]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata.axes
```

````

````{py:attribute} datasets
:canonical: ngff_zarr.v04.zarr_metadata.Metadata.datasets
:type: typing.List[ngff_zarr.v04.zarr_metadata.Dataset]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata.datasets
```

````

````{py:attribute} coordinateTransformations
:canonical: ngff_zarr.v04.zarr_metadata.Metadata.coordinateTransformations
:type: typing.Optional[typing.List[ngff_zarr.v04.zarr_metadata.Transform]]
:value: >
   None

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata.coordinateTransformations
```

````

````{py:attribute} name
:canonical: ngff_zarr.v04.zarr_metadata.Metadata.name
:type: str
:value: >
   'image'

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata.name
```

````

````{py:attribute} version
:canonical: ngff_zarr.v04.zarr_metadata.Metadata.version
:type: str
:value: >
   '0.4'

```{autodoc2-docstring} ngff_zarr.v04.zarr_metadata.Metadata.version
```

````

`````
