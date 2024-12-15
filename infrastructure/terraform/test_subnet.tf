resource "aws_vpc" "test_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "HELTHSYNC-VPC-TEST"
  }
}

resource "aws_subnet" "test_public_1" {
  vpc_id                  = aws_vpc.test_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "test-public-sub-1"
  }
}

resource "aws_subnet" "test_public_2" {
  vpc_id                  = aws_vpc.test_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "test-public-sub-2"
  }
}

resource "aws_internet_gateway" "test-gw" {
  vpc_id = aws_vpc.test_vpc.id

  tags = {
    Name = "test_vpc"
  }
}