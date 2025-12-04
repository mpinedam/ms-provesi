resource "aws_db_instance" "ordersdb" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  db_name              = "usersdb"
  username             = "admin"
  password             = "admin1234"
  skip_final_snapshot  = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.internal.id]
  db_subnet_group_name = null
}
