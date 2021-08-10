#!/bin/bash

source ../0.setup/env_vars.sh

# Upload schema script to GCS Bucket and import to create schema in Cloud SQL
gsutil cp ./cloudsql_schema-ddl.sql gs://${RECAI_PROJECT}_data_transfers/
gcloud sql import sql pso-css-retail gs://${RECAI_PROJECT}_data_transfers/cloudsql_schema-ddl.sql \
--database=Retail

# Import product data into Cloud SQL table
gcloud sql import csv pso-css-retail gs://${RECAI_PROJECT}_data_transfers/css_retail_products.csv.gz \
--database=Retail --table=products