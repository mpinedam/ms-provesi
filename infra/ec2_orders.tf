resource "aws_instance" "orders" {
  ami            = "ami-0c101f26f147fa7fd"
  instance_type  = "t3.micro"
  subnet_id      = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true
  user_data      = file("${path.module}/userdata/orders.sh")
  private_ip = "10.0.1.60"

  tags = {
    Name = "ms-orders"
  }
}

