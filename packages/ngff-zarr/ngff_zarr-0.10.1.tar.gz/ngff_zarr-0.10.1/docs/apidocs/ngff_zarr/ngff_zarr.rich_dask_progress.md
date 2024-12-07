# {py:mod}`ngff_zarr.rich_dask_progress`

```{py:module} ngff_zarr.rich_dask_progress
```

```{autodoc2-docstring} ngff_zarr.rich_dask_progress
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`NgffProgress <ngff_zarr.rich_dask_progress.NgffProgress>`
  - ```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress
    :summary:
    ```
* - {py:obj}`NgffProgressCallback <ngff_zarr.rich_dask_progress.NgffProgressCallback>`
  - ```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback
    :summary:
    ```
````

### API

`````{py:class} NgffProgress(rich_progress)
:canonical: ngff_zarr.rich_dask_progress.NgffProgress

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress
```

```{rubric} Initialization
```

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress.__init__
```

````{py:method} add_multiscales_task(description: str, scales: int)
:canonical: ngff_zarr.rich_dask_progress.NgffProgress.add_multiscales_task

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress.add_multiscales_task
```

````

````{py:method} update_multiscales_task_completed(completed: int)
:canonical: ngff_zarr.rich_dask_progress.NgffProgress.update_multiscales_task_completed

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress.update_multiscales_task_completed
```

````

````{py:method} add_cache_task(description: str, total: int)
:canonical: ngff_zarr.rich_dask_progress.NgffProgress.add_cache_task

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress.add_cache_task
```

````

````{py:method} update_cache_task_completed(completed: int)
:canonical: ngff_zarr.rich_dask_progress.NgffProgress.update_cache_task_completed

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgress.update_cache_task_completed
```

````

`````

`````{py:class} NgffProgressCallback(rich_progress)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback

Bases: {py:obj}`dask.callbacks.Callback`, {py:obj}`ngff_zarr.rich_dask_progress.NgffProgress`

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback
```

```{rubric} Initialization
```

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback.__init__
```

````{py:method} add_callback_task(description: str)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback.add_callback_task

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback.add_callback_task
```

````

````{py:method} _start(dsk)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback._start

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback._start
```

````

````{py:method} _start_state(dsk, state)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback._start_state

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback._start_state
```

````

````{py:method} _pretask(key, dsk, state)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback._pretask

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback._pretask
```

````

````{py:method} _posttask(key, result, dsk, state, worker_id)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback._posttask

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback._posttask
```

````

````{py:method} _finish(dsk, state, errored)
:canonical: ngff_zarr.rich_dask_progress.NgffProgressCallback._finish

```{autodoc2-docstring} ngff_zarr.rich_dask_progress.NgffProgressCallback._finish
```

````

`````
