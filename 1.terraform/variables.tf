variable "myaccount" {
  type        = string
  description = "Your user account for role membership"
}

variable "location" {
  type        = string
  description = "GCP location"
}

variable "region" {
  type        = string
  description = "GCP region used in deployment configuration"
}

variable "zone" {
  type        = string
  description = "GCP zone used in deployment configuration"
}

variable "beta-location" {
  type        = string
  description = "GCP location"
}

variable "beta-region" {
  type        = string
  description = "GCP region used in deployment configuration"
}

variable "beta-zone" {
  type        = string
  description = "GCP zone used in deployment configuration"
}

variable "project" {
  type        = string
  description = "GCP project used in deployment configuration"
}
