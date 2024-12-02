resource "aws_efs_mount_target" "efs_mt_public1" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = aws_subnet.public-1.id
  security_groups = [aws_security_group.allow_tls.id]
}

resource "aws_efs_mount_target" "efs_mt_public2" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = aws_subnet.public-2.id
  security_groups = [aws_security_group.allow_tls.id]
}