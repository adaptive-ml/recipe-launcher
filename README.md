# recipe-lancher

Tool for launching recipes using Adaptive Engine in kubernetes.

## Launch a recipe on FS

First make the script executable for convenience: `chmod +x run_recipe.py`

**Usage**: `./run_recipe.py --help`

**Example**:

```python
./run_recipe.py --job-name=fancyjob --user-name=laetitia --recipe-file=test_recipe_2.json --wandb-api-key wand_api_key --nodes-number 4
```

## Cancel a job

`./run_recipe.py --cancel --job-name your_job_name`
