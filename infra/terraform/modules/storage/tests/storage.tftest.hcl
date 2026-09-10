mock_provider "aws" {}

variables {
  name_prefix = "podium-foundation-test"
  kms_key_arn = "arn:aws:kms:eu-west-1:123456789012:key/00000000-0000-0000-0000-000000000000"
}

run "storage_contract" {
  command = apply

  assert {
    condition     = length(aws_s3_bucket.store) == 2
    error_message = "Provision separate dataset and artifact stores."
  }
  assert {
    condition     = alltrue([for store in aws_s3_bucket_versioning.store : store.versioning_configuration[0].status == "Enabled"])
    error_message = "Every store must preserve object revisions."
  }
  assert {
    condition     = alltrue([for store in aws_s3_bucket_public_access_block.store : store.block_public_acls && store.block_public_policy && store.ignore_public_acls && store.restrict_public_buckets])
    error_message = "Every store must block every public-access path."
  }
  assert {
    condition     = alltrue([for store in aws_s3_bucket.store : !store.force_destroy])
    error_message = "Removing infrastructure must not silently destroy stored evidence."
  }
  assert {
    condition = alltrue([for store in aws_s3_bucket_server_side_encryption_configuration.store :
      one(store.rule).apply_server_side_encryption_by_default[0].sse_algorithm == "aws:kms" &&
      one(store.rule).apply_server_side_encryption_by_default[0].kms_master_key_id == var.kms_key_arn
    ])
    error_message = "Every store must encrypt using the environment-owned KMS key."
  }
  assert {
    condition = alltrue([for store in aws_s3_bucket_policy.store :
      jsondecode(store.policy).Statement[0].Effect == "Deny" &&
      jsondecode(store.policy).Statement[0].Condition.Bool["aws:SecureTransport"] == "false"
    ])
    error_message = "Every store must deny insecure transport."
  }

}

run "reject_invalid_name" {
  command = plan
  variables {
    name_prefix = "INVALID PREFIX"
  }
  expect_failures = [var.name_prefix]
}

run "reject_non_kms_key" {
  command = plan
  variables {
    kms_key_arn = "alias/local-development"
  }
  expect_failures = [var.kms_key_arn]
}
