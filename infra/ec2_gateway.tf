resource "aws_instance" "apigateway" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.gateway.id, aws_security_group.internal.id]
  

  user_data = file("${path.module}/userdata/kong.sh")

  tags = {
    Name = "apigateway"
  }
}
