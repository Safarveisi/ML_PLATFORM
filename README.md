# ML from Development to Deployment

This repository provides an overview of a complete machine learning workflow, from data preprocessing to model deployment on Kubernetes via [KServe](https://github.com/kserve/kserve). The diagram illustrates the major steps and technologies used.

# Prerequisites

We use [devbox](https://www.jetify.com/devbox) to install all required packages listed in `devbox.json`. You also need `pyenv` to manage Python versions—install the version specified in `.python-version` (refer to `pyproject.toml` for details). After activating the devbox shell, run `./setup-env` to set up the Python virtual environment. Finally, launch Jupyter notebooks with the kernel pointing to this newly created environment.   

# Infrastructure

We use [Terraform](https://www.terraform.io/) to provision a Kubernetes cluster on [IONOS Cloud](https://cloud.ionos.de). You may opt for a different cloud provider, but you’ll need to update the Terraform files in the `terraform` directory accordingly. Ensure that your Kubernetes cluster’s `config` file is placed under `~/.kube` in `/home/user`.

If you’re using a *managed* Kubernetes cluster on IONOS Cloud, you can retrieve the cluster’s config file with the `helper/get_k8s_config.py` script. This requires the cluster ID—found in `terraform.tfstate` once provisioning is complete—passed in via the `--id` argument.

The Kubernetes cluster is where our [Spark](https://spark.apache.org/) ETL job will be executed and our inference service (`Kserve`) will be located. 

# Repository Structure

Each major step of the workflow has its own directory:

* `data_platform`: Contains the PySpark script (sample ETL job), the Kubernetes job CRD, and the installation assets for [Stackable](https://stackable.tech/en/) operators.
* `ml_platform`: Includes a Jupyter notebook (`ray_tune.ipynb`) for [Ray-based training and hyperparameter optimization](https://docs.ray.io/en/latest/tune/index.html), the KServe installation configuration, and a `best_model_artifacts` folder with MLflow artifacts (e.g., `conda.yaml`, `.env.best_run`) for the best mlflow run alongside supplementary files (`s3_config`, `.s3cfg`) used later in CI/CD.

* `.github/workflows`: Workflow for the CI/CD. 

# Workload

![platforms](./pictures/stack.png "Workload")

# Task Automation

We suggest using [go-task](https://github.com/go-task/task) for task automation. You can find an example in `data_platform/Taskfile.yml`. Once you activate the `devbox` shell, the `task` command is available. In the same directory, run `tl` to list all tasks along with their descriptions.

# Querying the Inference Service

Use the bash script at `ml_platform/best_model_artifacts/inference_service/prediction` to send a prediction request to the inference service. The `input.json` file in that same folder provides the feature set (`protocolVersion: v2`) for the instance you want the **XGBoost** model to predict.

> [!Note]
> Reasoned about Kubernetes configuration editing for a few seconds Before running the inference, modify the configmap
> called config-domain in the knative-serving namespace of your Kubernetes cluster. Use kubectl edit to remove _example
> from the data key, and then adjust the indentation for the rest of > the content in that key.

# Contributing

We welcome feedback and contributions. Please open an issue or submit a pull request for any improvements or bug fixes.
