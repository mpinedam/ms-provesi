resource "aws_instance" "mongo" {
  ami                         = "ami-0c101f26f147fa7fd" # Ubuntu 22 en us-east-1 (ejemplo)
  instance_type               = "t3.micro"
  vpc_security_group_ids      = [aws_security_group.traffic_mongo.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true

  user_data = file("${path.module}/userdata/mongo.sh")

  tags = {
    Name = "mongo-ec2"
  }
}
