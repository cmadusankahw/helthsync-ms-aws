
resource "aws_route_table" "test-rtb" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.test-gw.id
  }

  tags = {
    Name = "HelthSyncRoute-Test"
  }
}

resource "aws_route_table_association" "test-a-1" {
  subnet_id      = aws_subnet.test_public_1.id
  route_table_id = aws_route_table.test-rtb.id
}

resource "aws_route_table_association" "test-a-2" {
  subnet_id      = aws_subnet.test_public_2.id
  route_table_id = aws_route_table.test-rtb.id
}
