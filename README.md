# Open ML

This repository provides an overview of a complete machine learning workflow, from data preprocessing to model deployment on Kubernetes via [KServe](https://github.com/kserve/kserve). The diagram illustrates the major steps and technologies used.

# Prerequisites

We use **devbox** to install all required packages listed in `devbox.json`. You also need `pyenv` to manage Python versions—install the version specified in `.python-version` (refer to `pyproject.toml` for details). After activating the devbox shell, run `./setup-env` to set up the Python virtual environment. Finally, launch Jupyter notebooks with the kernel pointing to this newly created environment.   

# Infrastructure

We use **Terraform** to provision a Kubernetes cluster on IONOS Cloud. You may opt for a different cloud provider, but you’ll need to update the Terraform files in the `terraform` directory accordingly. Ensure that your Kubernetes cluster’s `config` file is placed under `~/.kube` in `/home/user`.

If you’re using a *managed* Kubernetes cluster on IONOS Cloud, you can retrieve the cluster’s config file with the `helper/get_k8s_config.py` script. This requires the cluster ID—found in `terraform.tfstate` once provisioning is complete—passed in via the `--id` argument.

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
