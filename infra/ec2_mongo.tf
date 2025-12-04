resource "aws_instance" "mongo" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  vpc_security_group_ids      = [aws_security_group.traffic_mongo.id, aws_security_group.traffic_ssh.id]
  associate_public_ip_address = true


  tags = {
    Name = "mongo-ec2"
  }
}
