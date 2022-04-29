import yaml
import os


def main():
    k8s_configs = os.listdir("k8s/")
    kustomization = {"kind": "Kustomization", "resources": [f"k8s/{config_name}" for config_name in k8s_configs]}
    with open("kustomization.yaml", "w") as kustomization_file:
        yaml.dump(kustomization, kustomization_file)


if __name__ == "__main__":
    main()
