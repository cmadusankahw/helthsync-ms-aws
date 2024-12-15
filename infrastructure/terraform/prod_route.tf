
resource "aws_route_table" "prod-rtb" {
  vpc_id = aws_vpc.prod_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.prod-gw.id
  }

  tags = {
    Name = "HelthSyncRoute-Prod"
  }
}

resource "aws_route_table_association" "prod-a-1" {
  subnet_id      = aws_subnet.prod_public_1.id
  route_table_id = aws_route_table.prod-rtb.id
}

resource "aws_route_table_association" "prod-a-2" {
  subnet_id      = aws_subnet.prod_public_2.id
  route_table_id = aws_route_table.prod-rtb.id
}
