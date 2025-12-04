resource "aws_instance" "products" {
  ami            = "ami-0c101f26f147fa7fd"
  instance_type  = "t3.micro"
  vpc_security_group_ids = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true
  private_ip = "10.0.1.153"
  user_data      = file("${path.module}/userdata/products.sh")
  

  tags = {
    Name = "ms-products"
  }
}
