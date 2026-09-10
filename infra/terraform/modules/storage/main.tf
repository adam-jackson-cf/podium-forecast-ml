locals {
  stores = toset(["datasets", "artifacts"])
}

resource "aws_s3_bucket" "store" {
  for_each      = local.stores
  bucket        = "${var.name_prefix}-${each.key}"
  force_destroy = false
  tags = {
    Project = "podium-forecastin-ml"
    Purpose = each.key
  }
}

resource "aws_s3_bucket_public_access_block" "store" {
  for_each                = local.stores
  bucket                  = aws_s3_bucket.store[each.key].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "store" {
  for_each = local.stores
  bucket   = aws_s3_bucket.store[each.key].id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_versioning" "store" {
  for_each = local.stores
  bucket   = aws_s3_bucket.store[each.key].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "store" {
  for_each = local.stores
  bucket   = aws_s3_bucket.store[each.key].id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
  }
}

resource "aws_s3_bucket_policy" "store" {
  for_each = local.stores
  bucket   = aws_s3_bucket.store[each.key].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.store[each.key].arn, "${aws_s3_bucket.store[each.key].arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}
