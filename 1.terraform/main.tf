# Base configurations and setup
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.48.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.79.0"
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
  region  = var.beta_region
  zone    = var.beta_zone
}

# Service Accounts
/*
resource "google_service_account" "recai-demo-sa" {
  provider     = google
  project      = var.project
  account_id   = "recai-demo-sa"
  display_name = "RecAI Demo"
}
data "google_iam_policy" "ml_admin" {
  binding {
    members = ["serviceAccount:${google_service_account.recai-demo-sa.name}"]
    role = "roles/automl.admin"
  }
  binding {
    members = ["serviceAccount:${google_service_account.recai-demo-sa.name}"]
    role = "roles/automlrecommendations.admin"
  }
}
*/
#resource "google_service_account_iam_policy" "recai-demo-sa-ml-admin" {
#  service_account_id = google_service_account.recai-demo-sa.name
#  policy_data = data.google_iam_policy.ml_admin.policy_data
#}
/*
resource "google_service_account_iam_binding" "recai-demo-sa-automl-admin" {
  provider           = google
  depends_on = [google_service_account.recai-demo-sa]
  service_account_id = google_service_account.recai-demo-sa.name
  role               = "roles/automl.admin"
  #member             = "serviceAccount:${google_service_account.recai-demo-sa.email}}"
  members             = ["user:${var.myaccount}"]
}
resource "google_service_account_iam_binding" "recai-demo-sa-recai-admin" {
  provider           = google
  depends_on = [google_service_account.recai-demo-sa]
  service_account_id = google_service_account.recai-demo-sa.name
  role               = "roles/automlrecommendations.admin"
  #member             = "serviceAccount:${google_service_account.recai-demo-sa.email}}"
  members             = ["user:${var.myaccount}"]
}
*/


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
  role = "roles/storage.legacyObjectOwner"
  member = "serviceAccount:${google_sql_database_instance.retail.service_account_email_address}"
}

resource "google_dataproc_cluster" "tensor_cluster" {
  name    = "tf-clus"
  region  = var.region
  provider = google-beta

  cluster_config {
    gce_cluster_config {
      zone        = var.zone
      network     = google_compute_network.private_network.id
      subnetwork  = google_compute_subnetwork.css-retail1.id
      metadata    = {
        include-gpus        = true
        gpu-driver-provider = "NVIDIA"
        init-actions-repo   = "gs://goog-dataproc-initialization-actions-${var.region}"
      }
    }
    software_config {
      image_version       = "preview-ubuntu18"
      optional_components = ["JUPYTER"]
    }
    master_config {
      num_instances = 1
      machine_type  = "n1-standard-16"
      accelerators {
        accelerator_count = 1
        accelerator_type  = "nvidia-tesla-t4"
      }
    }
    worker_config {
      num_instances = 3
      machine_type  = "n1-highmem-16"
      accelerators {
        accelerator_count = 1
        accelerator_type  = "nvidia-tesla-t4"
      }
    }
    preemptible_worker_config {
      num_instances = 0
    }
    initialization_action {
      script      = "gs://goog-dataproc-initialization-actions-${var.region}/mlvm/mlvm.sh"
      timeout_sec = 45 * 60
    }
    endpoint_config {
      enable_http_port_access = true
    }
  }

}
/*
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
  bucket      = google_storage_bucket.recai_demo_data_transfers.name
  policy_data = data.google_iam_policy.cloud_sql_admin.policy_data
}*/
