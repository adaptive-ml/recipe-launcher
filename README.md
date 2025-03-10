# recipe-lancher
Tool for launching recipes in kubernetes



### Launch a recipe

```

(helm delete yacine || true) &&  helm install yacine ./recipe-job --values image.tag="reference_harmony_image_tag"  --namespace recipe-jobs

```
``