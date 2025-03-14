#!/usr/bin/env python3
import subprocess
import webbrowser

def get_logs_url(k8s_job):
    return f"https://preprod.tech-adaptive-ml.com/monitoring/explore?schemaVersion=1&panes=%7B%22lo2%22:%7B%22datasource%22:%22P8E80F9AEF21F6940%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob_name%3D%5C%22{k8s_job}%5C%22%7D%20%7C%3D%20%60%60%22,%22queryType%22:%22range%22,%22datasource%22:%7B%22type%22:%22loki%22,%22uid%22:%22P8E80F9AEF21F6940%22%7D,%22editorMode%22:%22builder%22,%22direction%22:%22forward%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1"

def delete_helm_release(release_name, namespace="default"):
    command = ["helm", "delete", release_name, "--ignore-not-found"]
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
    
    subprocess.run(command, check=True, capture_output=True, text=True)

    k8s_job = f"{job_name}-recipe-job"
    print(f"🚀 Created k8s job: {k8s_job}")
    print(f"🔧 Models registry: {model_registry_path}")
    webbrowser.open_new_tab(get_logs_url(k8s_job))


if __name__ == "__main__":
    delete_helm_release(release_name="yacine") # cancels any job with same name to avoid conflict
    run_recipe_job(job_name="yacine", harmony_version="sha-e6b5567", user_name="laetitia", recipe_file="test_recipe_2.json", model_registry_path="/mnt/fluidstack/nfs/adaptive/model_registry", nodes_number=2)