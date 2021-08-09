# Recommendations AI Demo Project
___
> Refactored code base sourced from
> [go/recommendation-ai-demo-instructions](http://go/recommendation-ai-demo-instructions)



## Instructions

---
> General flow is to step through the directories, update the configurations and execute scripts and process.  
> Most configuration has been pushed into `./0.setup/env_vars.sh` and `./0.setup/install_packages.sh`

### 0.setup
> Install packages and update variables
1. Install cloud sdk, git, npm, and angular cli  
     `bash install_packages.sh`
2. Configure environment variables according to your desires  
    `vi env_vars.sh`
3. Export variables for continued usage in subsequent steps  
    `bash env_vars.sh`

### 1.terraform
> main.tf is configured to build Service Accounts, Networking, AppEngine, Cloud SQL, Storage buckets, and Big Query Datasets
1. Configure terraform.tfvars with required parameters; notably the **project** variable  
   `vi terraform.tfvars`
2. Initialize terraform for the current project  
   `terraform init`
3. Execute the plan step to review the full set of changes to be applied  
   `terraform plan`
4. After review, apply terraform spec to build the environment  
   `terraform apply`

### 2.dataprep
> Create schema in Cloud SQL and copy the css_retail dataset in Big Query
1. Execute Big Query copy and export script  
   `bash copy_retail_dataset_bigquery.sh`
2. Execute the Cloud SQL prep script to build the schema and load the product dataset  
   `bash prep_and_load_cloudsql.sh`

### 3.recommendation_ai
> Two scripts here, one to update RecAI for the newly minted API key for prediction calls
> and another script to delete an api key, which is not likely required but provided for convenience.  
> Consult original demo instructions for Recommendations AI interactions
1. Execute the prediction key script  
   `bash prediction_key.sh`
2. Configure Google Tag Manager
3. Load Product Catalog and User events into Recommendations AI
4. Configure and build Recommendations AI models
   
### 4.backend
> Consult original demo instructions document for various items to be updated
1. Update various configurations and variables in assorted files
2. Execute deploy script
   `bash deploy.sh`

### 5.frontend
> Consult original demo instructions document for various items to be updated
1. Update various configurations and variables in assorted files, including dispatch.yaml
2. Execute deploy script
   `bash deploy_app_engine.sh`