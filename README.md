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

Requires a node with GPS with docker installed, x86_64 arch.

`docker-launch.sh` script is a simpler version for runner training on a gpu host.

you'll need to set environment variables below:

- `adaptive_image_repo`: the harmony image repository
- `adaptive_image_tag`: harmony image tag
- `local_model_registry_path`: the adaptive model registry path.
- `local_recipe_file_json`: the serialized recipe configuration


For additional options/overrides on harmony settings, you can get in touch with adaptive support.