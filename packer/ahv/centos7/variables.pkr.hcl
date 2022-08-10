variable "nutanix_username" {
  type = string
}

variable "nutanix_password" {
  type = string
}

variable "nutanix_insecure" {
  type = string
  default = false
}

variable "nutanix_endpoint" {
  type = string
}

variable "nutanix_port" {
  type = string
}

variable "nutanix_subnet" {
  type = string
}

variable "nutanix_cluster" {
  type = string
}

variable "centos7_iso_uuid" {
  type = string
}
