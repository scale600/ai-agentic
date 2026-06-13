variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "ai-agentic-2026"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "gemini_model" {
  description = "Gemini model name"
  type        = string
  default     = "gemini-2.5-flash"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}
