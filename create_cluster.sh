#!/bin/bash

# Creates a 3-nodes AKS cluster with basic networking.

az aks create \
    --resource-group DogBreeds \
    --name DogBreeds \
    --node-count 3 \
    --kubernetes-version 1.13.5 \
    --service-principal <your_ad_sp_id> \
    --client-secret <your_ad_sp_secret> \
    --generate-ssh-keys \
    --enable-addons monitoring