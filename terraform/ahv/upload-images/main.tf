terraform{
  required_providers{
    nutanix = {
      source = "nutanix/nutanix"
      version = "1.3.0"
    }
  }
}

provider "nutanix" {
  username  = var.nutanix_username
  password  = var.nutanix_password
  endpoint  = var.nutanix_endpoint
  insecure  = var.nutanix_insecure
  port      = var.nutanix_port
}

data "nutanix_cluster" "cluster" {
  name = var.nutanix_cluster
}

data "nutanix_subnet" "net" {
  subnet_name = var.nutanix_subnet
}

resource "nutanix_image" "centos7" {
  name        = var.centos7_iso_name
  source_uri  = var.centos7_iso_uri
}

resource "nutanix_image" "centos8" {
  name        = var.centos8_iso_name
  source_uri  = var.centos8_iso_uri
}

resource "nutanix_image" "windows2016" {
  name        = var.windows_2016_iso_name
  source_uri  = var.windows_2016_iso_uri
}

resource "nutanix_image" "virtio" {
  name        = var.virtio_iso_name
  source_uri  = var.virtio_iso_uri
}

resource "nutanix_image" "ubuntu1804" {
  name        = var.ubuntu1804_iso_name
  source_uri  = var.ubuntu1804_iso_uri
}

resource "nutanix_image" "windowsPE" {
  name        = var.windows_pe_iso_name
  source_uri  = var.windows_pe_iso_uri
}

resource "nutanix_image" "windows10" {
  name        = var.windows_10_iso_name
  source_uri  = var.windows_10_iso_uri
}

output "cluster_uuid" {
  value = data.nutanix_cluster.cluster.cluster_id
}

output "subnet_uuid" {
  value = data.nutanix_subnet.net.id
}

output "centos7_uuid" {
  value = resource.nutanix_image.centos7.id
}

output "centos8_uuid" {
  value = resource.nutanix_image.centos8.id
}

output "win2016_uuid" {
  value = resource.nutanix_image.windows2016.id
}

output "virtio_uuid" {
  value = resource.nutanix_image.virtio.id
}

output "ubuntu1804_uuid" {
  value = resource.nutanix_image.ubuntu1804.id
}

output "windows_pe_uuid" {
  value = resource.nutanix_image.windowsPE.id
}

output "windows_10_uuid" {
  value = resource.nutanix_image.windows10.id
}