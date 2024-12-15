resource "aws_efs_mount_target" "efs_mt_test_public1" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = aws_subnet.test_public_1.id
  security_groups = [aws_security_group.test_allow_tls.id]
}

resource "aws_efs_mount_target" "efs_mt_test_public2" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = aws_subnet.test_public_2.id
  security_groups = [aws_security_group.test_allow_tls.id]
}
