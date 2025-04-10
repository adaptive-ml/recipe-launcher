GPU_COUNT=$(nvidia-smi --list-gpus | wc -l)

# before pulling make sure you have logged-in to the docker repo
docker pull ${adaptive_image_repo}:${adaptive_image_tag}

docker run --rm \
  -d \
  --gpus all \
  --shm-size=8g \
  -v ${local_recipe_file_json}:/opt/adaptive/lib/adaptive/adaptive/recipe.json \
  -v ${local_model_registry_path}:/model_registry \
  -e GPU_COUNT=${GPU_COUNT} \
  -e WORLD_SIZE=1 \
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




