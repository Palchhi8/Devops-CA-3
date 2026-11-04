variable "aws_secret_key" {
  type        = string
  description = "AWS secret access key supplied securely via vault/env"
  sensitive   = true
}

variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "production"
}

variable "app_version" {
  type        = string
  description = "Application release version tag"
  default     = "v2.3.0"
}
