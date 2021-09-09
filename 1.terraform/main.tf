# Base configurations and setup
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.82.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.82.0"
    }
  }
}
# Primary provider
provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
# Use this provider only if app engine and VPC, Cloud SQL are in separate region
provider "google-beta" {
  project = var.project
  region  = var.beta_region
  zone    = var.beta_zone
}
# Networking configurations
resource "google_compute_network" "private_network" {
  provider                = google-beta                #provider to be set as per region and zone
  project                 = var.project
  name                    = "css-retail"                   #name of VPC
  auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "css-retail" {
  provider      = google-beta
  project       = var.project
  name          = "css-retail-uc"    #name of the first subnet
  ip_cidr_range = "10.1.0.0/24"        #IP_CIDR range of the first subnet
  #region        = var.beta-region
  network       = google_compute_network.private_network.id
}
resource "google_compute_subnetwork" "css-retail1" {
  provider      = google
  project       = var.project
  name          = "css-retail-sub"  #name of the second subnet
  ip_cidr_range = "10.0.0.0/16"         #IP_CIDR range of the second subnet
  network       = google_compute_network.private_network.id
}
resource "google_compute_firewall" "default" {
  provider = google
  project  = var.project
  name     = "ssh-into-vm-instance"                       #name of the firewall can be specified over here
  network  = google_compute_network.private_network.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
resource "google_compute_global_address" "private_ip_address" {
  provider      = google-beta
  project       = var.project
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
  provider      = google
  project       = var.project
  region        = var.region
  name          = "recai-demo-vpc"
  ip_cidr_range = "10.1.1.0/28"
  network       = google_compute_network.private_network.name
}
# Application resource configuration
resource "google_app_engine_application" "retail-site" {
  provider    = google
  project     = var.project
  location_id = var.location
}
resource "google_sql_database_instance" "retail" {
  provider         = google-beta
  project          = var.project
  name             = "pso-css-retail"       #name of the MySQl cloud instance. Can be changed as per the requirements.
  database_version = "MYSQL_8_0"
  deletion_protection = false
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
  name     = "Retail"
  instance = google_sql_database_instance.retail.id
}
resource "google_sql_user" "recai-demo" {
  name     = "recai-demo"
  instance = google_sql_database_instance.retail.name
  host     = "%"
  password = "demopass"
}
# Data resource configuration
resource "google_bigquery_dataset" "css_retail" {
  provider   = google
  project    = var.project
  dataset_id = "css_retail"
}
resource "google_storage_bucket" "recai_demo_data_transfers" {
  provider                    = google
  project                     = var.project
  name                        = "${var.project}_data_transfers"
  location                    = "US"
  uniform_bucket_level_access = true
}
resource "google_storage_bucket" "model_export" {
  provider                    = google
  project                     = var.project
  name                        = "${var.project}_model_exports"
  location                    = "US"
  uniform_bucket_level_access = true
}
resource "google_storage_bucket" "vertex_training" {
  provider                    = google
  project                     = var.project
  name                        = "${var.project}_vertex_training"
  location                    = "US"
  uniform_bucket_level_access = true
}
resource "google_storage_bucket_object" "notebook_post_startup_script" {
  bucket = google_storage_bucket.vertex_training.name
  name = "notebook_install.sh"
  source = "../7.tf_two_tower/notebook_install.sh"
}
resource "google_storage_bucket_object" "notebook_requirements" {
  bucket = google_storage_bucket.vertex_training.name
  name = "notebook_requirements.txt"
  source = "../7.tf_two_tower/notebook_requirements.txt"
}
# Data permissions configuration
resource "google_storage_bucket_iam_member" "bq_exports_storage_admin" {
  bucket = google_storage_bucket.recai_demo_data_transfers.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
}
resource "google_storage_bucket_iam_member" "bq_exports_storage_legacy_bucket_owner" {
  bucket = google_storage_bucket.recai_demo_data_transfers.name
  role   = "roles/storage.legacyBucketOwner"
  member = "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
}
resource "google_storage_bucket_iam_member" "bq_exports_storage_legacy_object_owner" {
  bucket = google_storage_bucket.recai_demo_data_transfers.name
  role   = "roles/storage.legacyObjectOwner"
  member = "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
}
# Custom model building configuration
resource "google_notebooks_instance" "tf_two_tower" {
  provider            = google
  name                = "tf-two-tower"
  location            = var.zone
  subnet              = google_compute_subnetwork.css-retail1.id
  machine_type        = "n1-standard-4"
  install_gpu_driver  = true
  accelerator_config {
    core_count  = 1
    type        = "NVIDIA_TESLA_T4"
  }
  vm_image {
    project       = "deeplearning-platform-release"
    image_family  = "tf-latest-gpu"
  }

  #post_startup_script = "${google_storage_bucket_object.notebook_post_startup_script.media_link}"
}
