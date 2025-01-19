# Kubernetes microservices 

Here's an example of deploying various services on a Kubernetes cluster, such as a FastAPI web service and a Streamlit dashboard. This setup utilizes an Nginx controller as an ingress resource to route traffic to the appropriate service based on the originating endpoint. You can refer to `/deploy/k8s/common/ingress.yml` for more details.


# Prerequisites

To get started, you'll need access to a Kubernetes cluster. For this project, I used a managed Kubernetes cluster on IONOS Cloud, provisioned using Terraform (refer to `/terraform` for more information). Additionally, you should install `devbox` and activate its shell to access the necessary software packages for this project (see `devbox.json`). Lastly, ensure that you have both the `Docker Engine` and `pyenv` installed. Using `pyenv`, install a Python version that is compatible with `pyproject.toml` file, such as Python 3.9.1, used in this project.

### Provision a Kubernetes cluster
Activate the `devbox` shell (run `devbox shell`), navigate to `/terraform` directory and run

```bash
terraform plan -out="tfplan"
terraform apply 
```

It will take some time to create the resources. 

### Setup the python virtual env
In the project root directory, run

```
./setup-env
```

You can now acquire the provisioned Kubernetes cluster's config file by running

```bash
poetry run python helper/get_k8s_config.py 
```

This will save `config` file in `~/.kube/` (note that existing `config` file will be replaced). You can modify the python module to suit your needs (e.g., put the `config` file in an arbitrary location).

## Usage 

[1] Navigate to the following directories one by one and use `task build-container-image-multi-arch` to build a multi arch image and push it to `docker.io` registery.

> [!Note]
> Make sure you have a builder instance with driver of type docker-container. Otherwise, `docker buildx` fails. 

* `deploy/k8s/postgres`
* `deploy/k8s/apps/python-api`
* `deploy/k8s/apps/streamlit`

[2] Navigate to `deploy/k8s` directory and create the Kubernetes resources by running

```bash
task apply-all
``` 
> [!Note]
> You can also navigate to the directories listed above and execute tasks manually. To get the list of tasks, run `tl` (an alias for `task --list`) . You can then execute a task by `task <task-name>`

# System 

![Diagram of components](./pictures/diagram.png "Status of K8s deployment (success)")