#!/usr/bin/env python3
import subprocess
import webbrowser
import argparse
import re

def get_logs_url(k8s_job):
    return f"https://preprod.tech-adaptive-ml.com/monitoring/explore?schemaVersion=1&panes=%7B%22lo2%22:%7B%22datasource%22:%22P8E80F9AEF21F6940%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob_name%3D%5C%22{k8s_job}%5C%22%7D%20%7C%3D%20%60%60%22,%22queryType%22:%22range%22,%22datasource%22:%7B%22type%22:%22loki%22,%22uid%22:%22P8E80F9AEF21F6940%22%7D,%22editorMode%22:%22builder%22,%22direction%22:%22forward%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1"

def cancel_job(job_name, namespace="default"):
    command = ["helm", "delete", job_name, "--ignore-not-found"]
    if namespace:
        command.extend(["--namespace", namespace])
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error deleting Helm release:", e.stderr)

def run_recipe_job(job_name, harmony_version, user_name, recipe_file, model_registry_path, nodes_number, namespace="default"):
    command = ["helm", "install", job_name, "./charts/recipe-job"]

    # overrides
    command.extend(["--set", f"image.tag={harmony_version},userName={user_name},recipeFile={recipe_file},modelRegistryPath={model_registry_path},replicasCount={nodes_number}"])

    if namespace:
        command.extend(["--namespace", namespace])
    
    k8s_job = f"{job_name}-recipe-job"

    print(f"🚀 Creating job '{job_name}'")
    subprocess.run(command, check=True, capture_output=True, text=True)

    logs_url= get_logs_url(k8s_job)

    print(f"🚧 Queued recipe job '{job_name}'")
    print(f"🔧 Models registry: {model_registry_path}")

    print(f"Job logs at: {logs_url}")

    webbrowser.open_new_tab(logs_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe k8s launcher")
    parser.add_argument("--cancel", action="store_true", default=False, help="Cancel a job")
    parser.add_argument("--job-name", type=str, required=True, help="Name of the job to run")

    optional_args = parser.add_argument_group("Optional arguments (required only if --cancel is not set)")
    optional_args.add_argument("--harmony-version", type=str, default="sha-e6b5567", help="Harmony image version to use. see (https://github.com/adaptive-ml/adaptive/releases)")
    optional_args.add_argument("--user-name", type=str, required=False, help="User initiating the job (a directory per username under /mnt/fluidstack/nfs/home/)")
    optional_args.add_argument("--recipe-file", type=str, required=False, help="Recipe file name in /mnt/fluidstack/nfs/home/(--user-name)/adaptive/src/adaptive")
    optional_args.add_argument("--model-registry-path", type=str, default="/mnt/fluidstack/nfs/adaptive/model_registry", help="Path to the model registry")
    optional_args.add_argument("--nodes-number", type=int, default=2, help="Number of nodes to use (assumes 8 gpus per node)")
    optional_args.add_argument("--wandb-api-key", type=str, required=False, help="Wandb api key")

    args = parser.parse_args()

    if not re.match(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", args.job_name):
        raise argparse.ArgumentTypeError(
            "Invalid job name. It must consist of lowercase alphanumeric characters or '-', "
            "start and end with an alphanumeric character."
        )
        
    cancel_job(job_name=args.job_name)
    if args.cancel:
        print(f"Job '{args.job_name}' cancelled")

    if not args.cancel:
        if not args.user_name or not args.recipe_file:
            parser.error("At least --user-name, --recipe-file are required for running the recipe")
        
        if args.nodes_number <= 0:
            parser.error("The number of nodes must be a strict positive integer")

        run_recipe_job(
            job_name=args.job_name,
            harmony_version=args.harmony_version,
            user_name=args.user_name,
            recipe_file=args.recipe_file,
            model_registry_path=args.model_registry_path,
            nodes_number=args.nodes_number
        )