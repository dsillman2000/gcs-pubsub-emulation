terraform {
  required_providers {
    # Requires GCP
    google = {
      source  = "hashicorp/google"
      version = "~> 3.5"
    }
    # Requires Docker
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }
  required_version = ">= 0.12"
}
