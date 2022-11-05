terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


provider "aws" {
  region                  = "us-west-2"
  profile                 = "default"
}

resource "aws_s3_bucket" "bucket" {
    bucket = "josue-verzel-app"
}

