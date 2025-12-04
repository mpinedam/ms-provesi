output "kong_public_ip" {
  value = aws_instance.apigateway.public_ip
}

output "users_service_private_ip" {
  value = aws_instance.users.private_ip
}

output "orders_service_private_ip" {
  value = aws_instance.orders.private_ip
}

output "products_service_private_ip" {
  value = aws_instance.products.private_ip
}

output "mongo_private_ip" {
  value = aws_instance.mongo.private_ip
}

output "users_rds_endpoint" {
  value = aws_db_instance.usersdb.address
}

output "orders_rds_endpoint" {
  value = aws_db_instance.ordersdb.address
}
