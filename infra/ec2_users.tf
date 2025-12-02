resource "aws_instance" "users" {
  ami            = "ami-0c101f26f147fa7fd"
  instance_type  = "t3.micro"
  subnet_id      = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.internal.id]
  user_data      = file("${path.module}/userdata/users.sh")
}
