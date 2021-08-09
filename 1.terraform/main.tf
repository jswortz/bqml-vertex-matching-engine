# Base configurations and setup
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.48.0"
    }
  }
}
# Primary provider
provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
# Use this provider only if app engine and VPC,Cloud SQL are in separate region
provider "google-beta" {
  project = var.project
  region  = var.beta-region
  zone    = var.beta-zone
}

# Service Accounts
resource "google_service_account" "recai-demo-sa" {
  provider = google
  account_id = "recai-demo-sa"
  display_name = "RecAI Demo"
}
resource "google_service_account_iam_member" "recai-demo-sa-automl-admin" {
  provider = google
  service_account_id = google_service_account.recai-demo-sa.name
  role               = "roles/automl.admin"
  member             = "serviceAccount:${google_service_account.recai-demo-sa.email}}"
}
resource "google_service_account_iam_member" "recai-demo-sa-recai-admin" {
  provider = google
  service_account_id = google_service_account.recai-demo-sa.name
  role               = "roles/automlrecommendations.admin"
  member             = "serviceAccount:${google_service_account.recai-demo-sa.email}}"
}


# Networking configurations
resource "google_compute_network" "private_network" {
  provider                = google-beta                #provider to be set as per region and zone
  name                    = "css-retail"                   #name of VPC
  auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "css-retail" {
  provider      = google-beta
  name          = "css-retail-uc"    #name of the first subnet
  ip_cidr_range = "10.1.0.0/24"        #IP_CIDR range of the first subnet
  #region        = var.beta-region
  network       = google_compute_network.private_network.id
}
resource "google_compute_subnetwork" "css-retail1" {
  provider      = google
  name          = "css-retail-sub"  #name of the second subnet
  ip_cidr_range = "10.0.0.0/16"         #IP_CIDR range of the second subnet
  #region        = var.region
  network       = google_compute_network.private_network.id
}
resource "google_compute_firewall" "default" {
  provider = google
  name    = "ssh-into-vm-instance"                       #name of the firewall can be specified over here
  network = google_compute_network.private_network.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
resource "google_compute_global_address" "private_ip_address" {
  provider      = google-beta
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
}
resource "google_service_networking_connection" "private_vpc_connection" {
  provider                = google-beta
  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}
resource "google_vpc_access_connector" "connector" {
  provider = google
  region = var.region
  name = "recai-demo-serverless-vpc"
  ip_cidr_range = "10.1.1.0/28"
  network = google_compute_network.private_network.id
}

# Application resource configuration
resource "google_app_engine_application" "retail-site" {
  provider    = google
  location_id = var.location
}
resource "google_sql_database_instance" "retail" {
  provider         = google-beta
  name             = "pso-css-retail"       #name of the MySQl cloud instance. Can be changed as per the requirements.
  database_version = "MySQL_8_0"
  #region           = var.region
  depends_on = [google_service_networking_connection.private_vpc_connection]
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.private_network.id
    }
  }
}
resource "google_sql_database" "retail" {
  name = "Retail"
  instance = google_sql_database_instance.retail.id
}
resource "google_sql_user" "recai-demo" {
  name = "recai-demo"
  instance = google_sql_database_instance.retail.name
  host = "%"
  password = "demopass"
}
# Data resource configuration
resource "google_bigquery_dataset" "css_retail" {
  provider   = google
  dataset_id = "css_retail"
}
resource "google_storage_bucket" "recai_demo_data_bq_exports" {
  provider = google
  name     = "bq_exports"
  location = "US"
}
data "google_iam_policy" "cloud_sql_admin" {
  binding {
    members = [
      "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
    ]
    role = "roles/cloudsql.owner"
  }
  binding {
    members = [
      "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
    ]
    role = "roles/storage.objectAdmin"
  }
  binding {
    members = [
      "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
    ]
    role = "roles/storage.legacyObjectOwner"
  }
  binding {
    members = [
      "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
    ]
    role = "roles/storage.legacyBucketOwner"
  }
}
resource "google_storage_bucket_iam_policy" "bq_exports" {
  bucket = google_storage_bucket.recai_demo_data_bq_exports.name
  policy_data = data.google_iam_policy.cloud_sql_admin.policy_data
}
resource "google_storage_bucket" "model_export" {
  provider = google
  name     = "model_exports"
  location = "US"
}