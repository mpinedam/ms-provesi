resource "aws_instance" "api-gateway" {
  ami                         = "ami-0c101f26f147fa7fd"
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.gateway.id, aws_security_group.internal.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = file("${path.module}/userdata/kong.sh")
}
