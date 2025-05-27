terraform {
  required_providers {
     aws = {
            source = "hashicorp/aws"
        }
  }
  backend "s3" {
    bucket = "oat-state-bucket"
    key = "oat/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
    region = "eu-west-2"
}

