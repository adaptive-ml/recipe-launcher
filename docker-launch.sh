#!/bin/bash

set -e;

GPU_COUNT=$(nvidia-smi --list-gpus | wc -l)

# check that recipe config exists
if [ -z $local_recipe_file_json ]; then
    echo "Recip config file envvar local_recipe_file_json was not set"
    exit 1
fi
if [ -z $local_model_registry_path ]; then
    echo "Model registry path envvar local_model_registry_path was not set"
    exit 1
fi
if [ -z $data_dir ]; then
    echo "Input data directory envvar data_dir was not set"
    exit 1
fi
if [ -z $adaptive_image_repo ]; then
    echo "Image repo envvar adaptive_image_repo was not set"
    exit 1
fi
if [ -z $adaptive_image_tag ]; then
    echo "Image tag envvar adaptive_image_tag was not set"
    exit 1
fi

# Define default flags
DOCKER_RUN_FLAGS=""
# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d)
            DOCKER_RUN_FLAGS+="-d "
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# before pulling make sure you have logged-in to the docker repo
docker pull ${adaptive_image_repo}:${adaptive_image_tag}

# make directories if they do not exist
mkdir -p ${local_model_registry_path} ${data_dir} ./shared
sudo chmod -R 777 ${local_model_registry_path} ${data_dir} ./shared

docker run ${DOCKER_RUN_FLAGS} \
  --rm \
  --gpus all \
  --shm-size=8g \
  -v ${local_recipe_file_json}:/opt/adaptive/lib/adaptive/adaptive/recipe.json \
  -v ${local_model_registry_path}:/model_registry \
  -v ${data_dir}:/data \
  -v ./shared:/opt/adaptive/shared_folder \
  -e GPU_COUNT=${GPU_COUNT} \
  -e WORLD_SIZE=${GPU_COUNT} \
  -e ADAPTIVE_LOGGING_LEVEL=INFO \
  -e HARMONY_SETTING_LOGGING_LEVEL=INFO \
  -e ADAPTIVE_MODE=PROD \
  -e ADAPTIVE_RECIPE_JOB__CONFIG_PATH=/opt/adaptive/lib/adaptive/adaptive/recipe.json \
  -e USE_REPLAY_BUFFER=1 \
  -e JOB_COMPLETION_INDEX=0 \
  -e MASTER_ADDR=localhost \
  -e HARMONY_SETTING_WORKING_DIR=/tmp/workdir \
  -e HARMONY_SETTING_MODEL_REGISTRY_ROOT=/model_registry \
  --entrypoint /opt/adaptive/entrypoint_recipe_k8s_job.sh \
  ${adaptive_image_repo}:${adaptive_image_tag} 

echo "Job was launched, check docker logs"

