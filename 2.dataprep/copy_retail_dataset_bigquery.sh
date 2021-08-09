#!/bin/bash

# This script assumes all API and permission requirements are already in place
source ../0.setup/env_vars.sh

SOURCE_PROJECT=css-storeops
SOURCE_DS=css_retail
TARGET_DS=css_retail

echo "Copying source dataset to target dataset"
bq mk --transfer_config --project_id="${RECAI_PROJECT}" \
--data_source=cross_region_copy --target_dataset="${TARGET_DS}" \
--display_name=seed_css_retail \
--params='{"source_project_id":"'"${SOURCE_PROJECT}"'",source_dataset_id":"'"${SOURCE_DS}"'"}'

for TABLE in ['detail_page_view' 'home_page_view' 'purchase_complete' 'add_to_cart'];do
  echo 'Updating date in table ' "${TABLE}"
  YEAR=$(date +%Y)
  QUERY='update `'"${RECAI_PROJECT}"'.'"${TARGET_DS}"'.'"${TABLE}"'` set eventTime = REGEXP_REPLACE(eventTime, "2019", "'"${YEAR}"'") where eventTime is not null'
  bq query "${QUERY}"
  QUERY='update `'"${RECAI_PROJECT}"'.'"${TARGET_DS}"'.'"${TABLE}"'` set eventTime = REGEXP_REPLACE(eventTime, "2020", "'"${YEAR}"'") where eventTime is not null'
  bq query "${QUERY}"
done

# Extract products data to GCS
bq extract --compression=GZIP --destination_format=CSV --field_delimiter=, \
${TARGET_DS}.products gs://bq_exports/${TARGET_DS}_products.csv.gz