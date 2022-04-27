terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=4.0.0"
    }
  }
}

provider "aws" {
  # Uncomment the below line to specify non-default profile
  # profile = <profile-name>
}
