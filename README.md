# ML from Development to Deployment

This repository provides an overview of a complete machine learning workflow, from data preprocessing to model deployment on Kubernetes via [KServe](https://github.com/kserve/kserve). The diagram illustrates the major steps and technologies used.

# Prerequisites

We use [devbox](https://www.jetify.com/devbox) to install all required packages listed in `devbox.json`. You also need `pyenv` to manage Python versions—install the version specified in `.python-version` (refer to `pyproject.toml` for details). After activating the devbox shell, run `./setup-env` to set up the Python virtual environment. Finally, launch Jupyter notebooks with the kernel pointing to this newly created environment.   

You can track your ML experiments using either a local or a remote [Mlflow](https://mlflow.org/) server (see `ml_platform/start-local-mlflow-server`). In either case, the server must be backed by an S3 artifactory store. Remember to update the tracking server URI in your Jupyter notebook by calling `mlflow.set_tracking_uri(<remote_server_uri>)`.

To enable CI/CD, configure your Git repository with the necessary S3 credentials as secrets (the credentials used to log the metdata and artifacts for each trial into Mlflow server and its S3 artifactory storage), and ensure that the artifact paths in the S3 bucket are set correctly.

# Infrastructure

We use [Terraform](https://www.terraform.io/) to provision a Kubernetes cluster on [IONOS Cloud](https://cloud.ionos.de). For this, you need a `token` to authorize Terraform. You may opt for a different cloud provider, but you’ll need to update the Terraform files in the `terraform` directory accordingly. Ensure that your Kubernetes cluster’s `config` file is placed under `~/.kube` in `/home/user`.

If you’re using a *managed* Kubernetes cluster on IONOS Cloud, you can retrieve the cluster’s config file with the `helper/get_k8s_config.py` script. This requires the cluster ID—found in `terraform.tfstate` once provisioning is complete—passed in via the `--id` argument.

The Kubernetes cluster is where our [Spark](https://spark.apache.org/) ETL job will be executed and our inference service `Kserve` will be located. 

# Repository Structure

Each major step of the workflow has its own directory:

* `data_platform`: Contains the PySpark script (sample ETL job), the Kubernetes job CRD object, and the installation assets for [Stackable](https://stackable.tech/en/) operators.

* `ml_platform`: Includes a Jupyter notebook (`ray_tune.ipynb`) for [Ray-based training and hyperparameter optimization](https://docs.ray.io/en/latest/tune/index.html), and a folder (`best_model_artifacts`) where we keep the best Mlflow run's attributes (`.env.best_run`). This is necessary for our CI/CD pipeline.

* `inference_service`: Includes the installation assets for serverless Kserve, a Jupyter notebook (`serve.ipynb`) to make predictions using  Kserve, and a CRD object to deploy our Mlflow model using Kserve on K8s.  

* `data`: Sample data to be used for Pyspark ETL job and Hyperparameter tunning.

* `.github/workflows`: CI/CD workflow and a custom Docker action (located in `.github/actions/s3cmd-docker`) that simplifies interacting with S3-compatible services. At the time of writing, none of the available s3cmd actions supported S3-compatible services other than `s3.amazonaws.com`.

> [!Note]
>  Using the bash files in `install` directory of `data_platform` and `inference_service`, you can install 
> Stackable K8s Spark operator and serverless Kserve into your Kubernetes cluster. 

# Workload

![platforms](./pictures/comp.png "Workload")

# Task Automation

We suggest using [go-task](https://github.com/go-task/task) for task automation. You can find an example in `data_platform/Taskfile.yml`. Once you activate the `devbox` shell, the `task` command is available. In the same directory, run `tl` to list all tasks along with their descriptions.

# Querying the Inference Service

Use the bash script at `ml_platform/best_model_artifacts/inference_service/prediction` to send a prediction request to the inference service. The `input.json` file in that same folder provides the feature set (`protocolVersion: v2`) for the instance you want the **XGBoost** model to predict. You can also use `ml_platform/serve.ipynb` for this purpose. 

> [!Note]
>  Before using the inference service, modify the configmap called `config-domain` in the `knative-serving`
> namespace of your Kubernetes cluster. Use `kubectl edit` to remove `_example` from the `data` key, and
> then adjust the indentation for the rest of the content in that key.

If you modify the `InferenceService` to introduce a canary model (see `ml_platform/best_model_artifacts/inference_service/mlflow.yml`), the `iris-classifier` will have two active revisions. Viewing the running pods, you’ll notice one pod serving the old model and another serving the new model, with 10% of traffic routed to the canary version.

```bash
kubectl get pods -l serving.kserve.io/inferenceservice=iris-classifier
```

You can promote the canary model by removing the `canaryTrafficPercent` field in the manifest file.

# Contributing

We welcome feedback and contributions. Please open an issue or submit a pull request for any improvements or bug fixes.
