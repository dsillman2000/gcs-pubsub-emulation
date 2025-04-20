terraform {
  required_providers {
    # Requires GCP
    google = {
      source  = "hashicorp/google"
      version = "~> 3.5"
    }
  }
  required_version = ">= 0.12"
}
