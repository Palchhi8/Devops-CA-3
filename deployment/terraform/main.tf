# Infrastructure Decision Note:
# Standalone EC2 instance infrastructure has been deprecated for OrderFlow production deployments.
# Containerized Kubernetes orchestration (deployment/kubernetes/) is selected for OrderFlow v2.3.0
# to ensure high availability, automatic scaling, health probing, and zero-downtime rolling updates.

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Legacy single-node EC2 instance (Retained for reference/staging fallback only)
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name        = "OrderFlow-LegacyInstance"
    Environment = var.environment
    Version     = var.app_version
    ManagedBy   = "Terraform"
  }
}
