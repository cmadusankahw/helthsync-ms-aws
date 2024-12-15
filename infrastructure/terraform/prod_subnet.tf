resource "aws_vpc" "prod_vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "HELTHSYNC-VPC-PROD"
  }
}

resource "aws_subnet" "prod_public_1" {
  vpc_id                  = aws_vpc.prod_vpc.id
  cidr_block              = "10.1.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "prod-public-sub-1"
  }
}

resource "aws_subnet" "prod_public_2" {
  vpc_id                  = aws_vpc.prod_vpc.id
  cidr_block              = "10.1.2.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "prod-public-sub-2"
  }
}

resource "aws_internet_gateway" "prod-gw" {
  vpc_id = aws_vpc.prod_vpc.id

  tags = {
    Name = "prod_vpc"
  }
}
