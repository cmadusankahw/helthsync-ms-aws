resource "aws_efs_file_system" "efs" {
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS" # Move files to Infrequent Access after 30 days
  }

  tags = {
    Name = "my-efs-filesystem"
  }
}