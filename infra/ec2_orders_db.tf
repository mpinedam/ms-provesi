resource "aws_instance" "orders_db" {
  ami                         = "ami-0c101f26f147fa7fd"
  instance_type               = "t3.micro"
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = false
  private_ip = "10.0.1.174"

  user_data = file("${path.module}/userdata/orders_db.sh")

  tags = {
    Name = "orders-db-ec2"
  }
}
