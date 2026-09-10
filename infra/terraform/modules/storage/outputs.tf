output "bucket_names" {
  description = "Dataset and artifact bucket names for workload configuration."
  value       = { for name, bucket in aws_s3_bucket.store : name => bucket.id }
}
