resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = true
}

resource "aws_security_group" "rds_sg" {
  name        = "rds-security-group"
  description = "Allow access to RDS"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict this in production!
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  storage_type         = "gp2"
  instance_class       = "db.t3.micro"
  engine               = "postgres"
  engine_version       = "15.4"
  db_name              = "hs"
  username             = "hsuser"
  password             = "hspassword" 
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  multi_az             = false
  publicly_accessible  = false
  skip_final_snapshot  = true
  tags = {
    Name = "HelthSync PostgreSQL DB"
  }

  depends_on = [aws_security_group.rds_sg]
}

# Step 3: Create a Secret in Secrets Manager to store the credentials
resource "aws_secretsmanager_secret" "helthsync-rds" {
  name        = "helthsync-rds"
  description = "Credentials for PostgreSQL RDS instance"
}

resource "aws_secretsmanager_secret_version" "db_secret_version" {
  secret_id     = aws_secretsmanager_secret.helthsync-rds.id
  secret_string = jsonencode({
    username = aws_db_instance.postgres.username
    password = aws_db_instance.postgres.password
    host     = aws_db_instance.postgres.address
    port     = 5432
    dbname   = aws_db_instance.postgres.name
  })
}

# Step 4: Create a DB subnet group (optional but recommended)
resource "aws_db_subnet_group" "main" {
  name       = "hs-db-subnet-group"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]

  tags = {
    Name = "HS DB Subnet Group"
  }
}
