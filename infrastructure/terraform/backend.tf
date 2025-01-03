resource "aws_s3_bucket" "terraform_state" {
  bucket = "hs-terraform-state-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }


  tags = {
    Name        = "Terraform State"
    Environment = "dev"
  }
}
