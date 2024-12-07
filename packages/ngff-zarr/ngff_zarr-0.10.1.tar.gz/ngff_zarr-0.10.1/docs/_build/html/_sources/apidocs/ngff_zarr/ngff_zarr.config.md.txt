# {py:mod}`ngff_zarr.config`

```{py:module} ngff_zarr.config
```

```{autodoc2-docstring} ngff_zarr.config
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`NgffZarrConfig <ngff_zarr.config.NgffZarrConfig>`
  - ```{autodoc2-docstring} ngff_zarr.config.NgffZarrConfig
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`default_store_factory <ngff_zarr.config.default_store_factory>`
  - ```{autodoc2-docstring} ngff_zarr.config.default_store_factory
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`config <ngff_zarr.config.config>`
  - ```{autodoc2-docstring} ngff_zarr.config.config
    :summary:
    ```
````

### API

````{py:function} default_store_factory()
:canonical: ngff_zarr.config.default_store_factory

```{autodoc2-docstring} ngff_zarr.config.default_store_factory
```
````

`````{py:class} NgffZarrConfig
:canonical: ngff_zarr.config.NgffZarrConfig

```{autodoc2-docstring} ngff_zarr.config.NgffZarrConfig
```

````{py:attribute} memory_target
:canonical: ngff_zarr.config.NgffZarrConfig.memory_target
:type: int
:value: >
   None

```{autodoc2-docstring} ngff_zarr.config.NgffZarrConfig.memory_target
```

````

````{py:attribute} task_target
:canonical: ngff_zarr.config.NgffZarrConfig.task_target
:type: int
:value: >
   50000

```{autodoc2-docstring} ngff_zarr.config.NgffZarrConfig.task_target
```

````

````{py:attribute} cache_store
:canonical: ngff_zarr.config.NgffZarrConfig.cache_store
:type: zarr.storage.StoreLike
:value: >
   'field(...)'

```{autodoc2-docstring} ngff_zarr.config.NgffZarrConfig.cache_store
```

````

`````

````{py:data} config
:canonical: ngff_zarr.config.config
:value: >
   'NgffZarrConfig(...)'

```{autodoc2-docstring} ngff_zarr.config.config
```

````
