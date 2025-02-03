# Open ML

This repository provides an overview of a complete machine learning workflow, from data preprocessing to model deployment on Kubernetes via [KServe](https://github.com/kserve/kserve). The diagram illustrates the major steps and technologies used.

# Prerequisites

We use `devbox` to install necessary packages for the project. All the packages are available in `devbox.json`. Apart from that, you need to have `pyenv` installed and install the Python version suggested in `.python-version` (see also `pyproject.toml`). Once the `devbox` shell is activated, you can run `./setup-env` to install the python virtual env. You can then run the jupyter notebooks with its kernel set to the virtual env just created.    

# Infrastructure

We use terraform to provision a Kubernetes cluster on IONOS cloud. You can choose another provider. In this case, you need to modify the `tf` files in `terraform` directory. Make sure the Kebernetes cluster's `config` file is located in `~/.kube` directory of `/home/user`. If you use a managed Kubernetes cluster on IONOS cloud, you can use the python script in `helper` directory (`helper/get_k8s_config.py`) to get the `config` file of your cluster. For this to work, you need to have the cluster id (you can find it in `terraform.tfstate` after a successful provision) and pass it to `--id`.

The Kubernetes cluster is where our Spark ETL job will be executed and our inference service (`Kserve`) will be located. 

# Repo Structure

Each step has its own directory:

* `data_platform`: Pyspark script (sample ETL job), job CRD and installaton of Stackable operators.
* `ml_platform`: Jupyter notebook where a data scientist runs Ray training and hyperparameter optimization (`ray_tune.ipynb`), installation of serverless Kserve into the Kubernetes cluster, and a special directory called `best_model_artifacts` with the best mlflow run's artifacts (e.g., `conda.yaml` and `.env.best_run`) as well as supplimentary files (e.g., `s3_config` and `.s3cfg`) to be used in CI/CD later on. 
* `.github/workflows`: Workflow for the CI/CD. 

# Workload

![platforms](./pictures/stack.png "Workload")


# Contributing

We welcome feedback and contributions. Please open an issue or submit a pull request for any improvements or bug fixes.
