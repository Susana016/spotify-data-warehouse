# Provider/auth/security

terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 1.0"
    }
  }
}

provider "snowflake" {
  organization_name = var.snowflake_organization
  account_name      = var.snowflake_account
  user              = var.snowflake_user
  password          = var.snowflake_password
}

resource "snowflake_account_role" "pipeline_role" {
  name    = "PIPELINE_ROLE"
  comment = "Role for data pipeline automation"
}