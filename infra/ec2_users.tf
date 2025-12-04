resource "aws_instance" "users" {
  ami            = "ami-051685736c7b35f95"
  instance_type  = "t3.micro"
  vpc_security_group_ids = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true
  user_data      = file("${path.module}/userdata/users.sh")
  
  tags = {
    Name = "ms-users"
  }
}
