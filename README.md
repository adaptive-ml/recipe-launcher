# recipe-lancher

Tool for launching recipes using Adaptive Engine in kubernetes.

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
