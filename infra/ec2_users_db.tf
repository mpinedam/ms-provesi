resource "aws_instance" "users_db" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true

  user_data = file("${path.module}/userdata/users_db.sh")

  tags = {
    Name = "users-db-ec2"
  }
}
