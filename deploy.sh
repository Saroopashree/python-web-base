#!/usr/bin/env bash
set -xe

HOST="$1"
ACTION="$2"
PROFILE="$3"

if [ -z "$HOST" ] || [[ ! "$HOST" =~ ^(local-k8s|cloud-k8s)$ ]]; then
  echo "Invalid HOST specified"
  exit 1
fi

if [ -z "$ACTION" ] || [[ ! "$ACTION" =~ ^(up|down)$ ]]; then
  echo "Invalid ACTION specified"
  exit 1
fi

refresh_k8s_config() {
  python3 -m pip install pyyaml

  rm -rf k8s/
  kompose convert -o k8s/
  python3 create_customization.py
}

if [[ "$HOST" == local-k8s ]] && [[ "$ACTION" == up ]]; then
  refresh_k8s_config

  kubectl config use-context minikube
  kubectl apply -k .
fi

if [[ "$HOST" == local-k8s ]] && [[ "$ACTION" == down ]]; then
  kubectl config use-context minikube
  kubectl delete -k .
fi

if [[ "$HOST" == cloud-k8s ]] && [[ "$ACTION" == up ]]; then
  refresh_k8s_config

  # Apply terraform script
  cd terraform/
  terraform init
  terraform plan
  terraform apply -auto-approve

  # Update the Kube Config to change the context to the deployed Cluster in cloud
  update_kubeconfig="aws eks --region us-east-1 update-kubeconfig --name todo-application"
  if [ -z "$PROFILE" ]; then
    echo "Using Default AWS profile"
  else 
    update_kubeconfig="$update_kubeconfig --profile $PROFILE"
  fi
  eval $update_kubeconfig
  
  # Deploy the k8s resources to cloud cluster
  cd ../
  kubectl apply -k .
fi

if [[ "$HOST" == cloud-k8s ]] && [[ "$ACTION" == down ]]; then
  refresh_k8s_config
  
  # Delete the k8s resources in the cloud cluster
  kubectl delete -k .

  # Destroy the resources created by terraform
  cd terraform/
  terraform destroy -auto-approve
fi
