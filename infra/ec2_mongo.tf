resource "aws_instance" "mongo" {
  ami                         = "ami-0c101f26f147fa7fd" # Ubuntu 22 en us-east-1 (ejemplo)
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.internal.id]
  associate_public_ip_address = true 

  user_data = file("${path.module}/userdata/mongo.sh")

  tags = {
    Name = "mongo-ec2"
  }
}
