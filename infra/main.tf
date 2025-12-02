module "vpc" {
  source = "./vpc.tf"
}

module "security" {
  source = "./security.tf"
}

module "gateway" {
  source = "./ec2_gateway.tf"
}

module "users" {
  source = "./ec2_users.tf"
}

module "orders" {
  source = "./ec2_orders.tf"
}

module "products" {
  source = "./ec2_products.tf"
}

module "mongo" {
  source = "./ec2_mongo.tf"
}

module "rds_users" {
  source = "./rds_users.tf"
}

module "rds_orders" {
  source = "./rds_orders.tf"
}
