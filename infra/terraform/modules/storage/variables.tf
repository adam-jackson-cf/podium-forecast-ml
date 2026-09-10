variable "name_prefix" {
  description = "Globally unique, approved environment prefix for storage buckets."
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,40}$", var.name_prefix))
    error_message = "Use 3–41 lowercase letters, digits or hyphens starting with a letter."
  }
}

variable "kms_key_arn" {
  description = "Environment-owned KMS key ARN; key policy must grant intended workload access."
  type        = string
  validation {
    condition     = can(regex("^arn:aws:kms:[a-z0-9-]+:[0-9]{12}:key/", var.kms_key_arn))
    error_message = "Supply a customer-managed AWS KMS key ARN."
  }
}
