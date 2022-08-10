build {
  sources = [
    "source.nutanix.windows"
  ]

  provisioner "windows-shell" {
    only = ["nutanix.windows"]
    inline = ["dir d:\\"]
  }

  ## diskpart /s drive:\CreatePartitions-UEFI.txt
  provisioner "windows-shell" {
    only = ["nutanix.windows"]
    inline = ["diskpart /s F:\\scripts\\CreatePartitions-UEFI.txt"]
    pause_before = "60s"
  }

  ## drive:\ApplyImage.bat drive:\win10.wim
  provisioner "windows-shell" {
    only = ["nutanix.windows"]
    inline = ["F:\\scripts\\ApplyImage.bat E:\\wim-files\\win10.wim"]
    pause_before = "60s"
  }

}