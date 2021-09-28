#!/bin/bash

# Assumes you are running debian/ubuntu and have required sources already setup
# Intended to be used on gLinux, cloud shell, or in a GCP VM

sudo apt-get update
sudo apt-get install -y google-cloud-sdk git npm

sudo npm install -g @angular/cli

sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -