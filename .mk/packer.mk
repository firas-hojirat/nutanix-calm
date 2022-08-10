REQUIRED_TOOLS_LIST += packer

PKR_PATH ?= ahv/centos7

packer-ahv-validate packer-ahv-build: packer-ahv-init

.PHONY: packer-ahv-print-uuids
packer-ahv-print-uuids: #### Print ahv image uuids from existing terraform output / state file
	@echo PKR_VAR_centos7_iso_uuid=${PKR_VAR_centos7_iso_uuid}
	@echo PKR_VAR_centos8_iso_uuid=${PKR_VAR_centos8_iso_uuid}
	@echo PKR_VAR_windows_2016_iso_uuid=${PKR_VAR_windows_2016_iso_uuid}
	@echo PKR_VAR_virtio_iso_uuid=${PKR_VAR_virtio_iso_uuid}
	@echo PKR_VAR_ubuntu1804_iso_uuid=${PKR_VAR_ubuntu1804_iso_uuid}
	@echo PKR_VAR_windows_pe_iso_uuid=${PKR_VAR_windows_pe_iso_uuid}
	@echo PKR_VAR_windows_10_iso_uuid=${PKR_VAR_windows_10_iso_uuid}

.PHONY: packer-ahv-init
packer-ahv-init: #### Init packer ahv configs
	[ -f $(TF_AHV_IMAGE_STATE_PATH) ] || make terraform-apply TF_PATH=ahv/upload-images ENVIRONMENT=${ENVIRONMENT}
	@make packer-ahv-print-uuids ENVIRONMENT=${ENVIRONMENT}; \
	cd packer/${PKR_PATH}; \
	packer init .

.PHONY: packer-ahv-validate
packer-ahv-validate: #### Validates Packer Build Files
	@cd packer/${PKR_PATH}; \
	packer validate .

.PHONY: packer-ahv-build
packer-ahv-build: #### Builds Target Packer Image. i.e., make packer-ahv-build PKR_PATH=ahv/windows2016 ENVIRONMENT=${ENVIRONMENT}
	@cd packer/${PKR_PATH}; \
	packer build -force -on-error=cleanup .

.PHONY: packer-vsphere-build
packer-vsphere-build: #### Builds Packer Images in vSphere if they are not already available
	cd packer/vsphere; \
	packer init builds/windows/desktop/10; \
	packer build -force -on-error=ask \
		--only vsphere-iso.windows-desktop \
		-var-file="builds/common.pkrvars.hcl" \
		-var-file="builds/vsphere.pkrvars.hcl" \
		builds/windows/desktop/10