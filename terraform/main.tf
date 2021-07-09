
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.48.0"
    }
  }
}

provider "google" {
  
  region      = "us-central1"            #region goes here
  project = "babrams-recai-demo"                   #project ID goes here
}



resource "google_app_engine_application" "app" {
 project     = "babrams-recai-demo"   # PROJECT ID goes here
  location_id = "us-central"             #location id goes here
}


#use this provider only if app engine and VPC,Cloud SQL are in separate region
provider "google-beta" {
 region = "us-west1"
  zone   = "us-west1-a"
project = "babrams-recai-demo"   # project id goes here
}


  resource "google_compute_network" "private_network" {
  provider = google-beta                #provider to be set as per region and zone
  

  name = "css-retail"                   #name of VPC
auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "css-retail" {
  name          = "css-retail-uc"    #name of the first subnet
  ip_cidr_range = "10.1.0.0/24"        #IP_CIDR range of the first subnet
  region        = "us-west1"
  network       = google_compute_network.private_network.id
 
}
resource "google_compute_subnetwork" "css-retail1" {
  name          = "css-retail-sub"  #name of the second subnet
  ip_cidr_range = "10.0.0.0/16"         #IP_CIDR range of the second subnet
  region        = "us-central1"
  network       = google_compute_network.private_network.id
 
}
#Cloud SQL configuration
resource "google_compute_global_address" "private_ip_address" {
  provider = google-beta

  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  provider = google-beta

  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}



resource "google_sql_database_instance" "instance" {
  provider = google-beta

  name   = "pso-css-retail"       #name of the MySQl cloud instance. Can be changed as per the requirements.
  database_version = "MySQL_8_0"
  region = "us-central1"

  depends_on = [google_service_networking_connection.private_vpc_connection]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.private_network.id
    }
  }
}

#firewall setup
resource "google_compute_firewall" "default" {
  name    = "ssh-into-vm-instance"                       #name of the firewall can be specified over here
  network = google_compute_network.private_network.name

  

  allow {
    protocol = "tcp"
    ports    = ["22"]                                      	
  }

  
}


