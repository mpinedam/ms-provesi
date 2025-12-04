variable "aws_region" {
  default = "us-east-1"
}

variable "project_prefix" {
  description = "Prefix used for naming AWS resources"
  type        = string
  default     = "provesi"
}


variable "repo_url" {
  default = "https://github.com/mpinedam/ms-provesi.git"
}
