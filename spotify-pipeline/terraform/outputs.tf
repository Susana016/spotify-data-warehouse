# What Terraform returns

output "database_name" {
  value = snowflake_database.spotify.name
}

output "warehouse_name" {
  value = snowflake_warehouse.spotify_wh.name
}

output "role_name" {
  value = snowflake_account_role.pipeline_role.name
}