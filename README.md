# recipe-lancher

Tool for launching training recipes using Adaptive Engine in kubernetes on multiple nodes.

## Launch a recipe on FS

First make the script executable for convenience: `chmod +x k8s_launcher.py`

**Usage**: `./k8s_launcher.py --help`

**Example**:

```python
./k8s_launcher.py --job-name=fancyjob --user-name=laetitia --recipe-file=test_recipe_2.json --wandb-api-key wand_api_key --nodes-number 4
```

## Cancel a job

`./k8s_launcher.py --cancel --job-name your_job_name`

## Current limitations

- No advanced queue features, no guarantee of fairness.
- Requires building a new image if dependencies (either pip, or binaries) need to be changed.


## Run using docker (single node)

Requires a GPU node with docker installed, x86_64 architecture.

`docker-launch.sh` script is a simpler version to launch training jobs on a gpu host.

You'll need to set environment variables below:

- `adaptive_image_repo`: harmony image repository
- `adaptive_image_tag`: harmony image tag
- `local_model_registry_path`: local adaptive model registry path
- `local_recipe_file_json`: the local JSON-serialized recipe configuration
- `data_dir`: the local directory where you save training/evaluation data files


For additional options/overrides on harmony settings, you can get in touch with adaptive support.
