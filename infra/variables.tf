variable "aws_region" {
  default = "us-east-1"
}

variable "key_name" {
  description = "EC2 SSH key (you must create it in AWS first)"
  type        = string
}

variable "repo_url" {
  default = "https://github.com/mpinedam/ms-provesi.git"
}
