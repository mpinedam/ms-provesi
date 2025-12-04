resource "aws_security_group" "traffic_apps" {
    name        = "${var.project_prefix}-traffic-apps"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "${var.project_prefix}-traffic-apps"
    }
}

# Recurso. Define el grupo de seguridad para el tráfico de las bases de datos (5432).
resource "aws_security_group" "traffic_db" {
  name        = "${var.project_prefix}-traffic-db"
  description = "Allow PostgreSQL access"

  ingress {
    description = "Traffic from anywhere to DB"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_prefix}-traffic-db"
  }
}

# Recurso. Define el grupo de seguridad para el tráfico SSH (22) y permite todo el tráfico saliente.
resource "aws_security_group" "traffic_ssh" {
  name        = "${var.project_prefix}-traffic-ssh"
  description = "Allow SSH access"

  ingress {
    description = "SSH access from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_prefix}-traffic-ssh"
  }
}

# Recurso. Define el grupo de seguridad para el tráfico de MongoDB (27017).
resource "aws_security_group" "traffic_mongo" {
  name        = "${var.project_prefix}-traffic-mongo"
  description = "Allow MongoDB access"

  ingress {
    description = "Traffic from anywhere to MongoDB"
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_prefix}-traffic-mongo"
  }
}

resource "aws_security_group" "traffic_api" {
    name        = "${var.project_prefix}-traffic-api"
    description = "Allow application traffic on port 8000"

    ingress {
        description = "HTTP access for gateway layer"
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-api"
    })
}
