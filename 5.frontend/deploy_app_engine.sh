#!/bin/bash

source ../0.setup/env_vars.sh

ng build

gcloud app deploy --project="${RECAI_PROJECT}"

gcloud app deploy --project="${RECAI_PROJECT}" dispatch.yaml
