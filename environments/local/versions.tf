terraform {
  required_providers {
    # Requires Docker
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }
  required_version = ">= 0.12"
}
