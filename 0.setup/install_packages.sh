#!/bin/bash

# Assumes you are running debian/ubuntu and have required sources already setup
# Intended to be used on gLinux or in a GCP VM

sudo apt-get update
sudo apt-get install -y google-cloud-sdk git npm

sudo npm install -g @angular/cli