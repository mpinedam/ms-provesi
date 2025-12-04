resource "aws_instance" "orders_db" {
  ami                         = data.aws_ami.ubuntu_2404.id
  instance_type               = "t3.micro"
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = false

  user_data = file("${path.module}/userdata/orders_db.sh")

  tags = {
    Name = "orders-db-ec2"
  }
}
