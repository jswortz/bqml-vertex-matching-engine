#!/bin/bash

USERNAME=babrams

mysql -h 127.0.0.1 -u ${USERNAME} --port 3308 < schema.sql

gcloud sql import csv pso-css-retail gs://bq_exports/products.csv.gz \
--database=Retail --table=products