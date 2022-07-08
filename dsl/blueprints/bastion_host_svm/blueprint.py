# THIS FILE IS AUTOMATICALLY GENERATED.
"""
Linux Bastion Host blueprint for deploying Single VM with Cloud Native Management Utilities

"""

import base64
import os
import json

from calm.dsl.builtins import *
from calm.dsl.config import get_context


ContextObj = get_context()
init_data = ContextObj.get_init_config()
  
# Get the values from environment vars

NutanixKeyUser = os.environ['NUTANIX_KEY_USER']
NutanixPublicKey = read_local_file("nutanix_public_key")
NutanixKey = read_local_file("nutanix_key")

NutanixCred = basic_cred(
        NutanixKeyUser,
        name="Nutanix",
        type="KEY",
        password=NutanixKey,
        default=True
    )

NutanixUser = os.environ['NUTANIX_USER']
NutanixPassword = os.environ['NUTANIX_PASS']
NutanixPasswordCred = basic_cred(
        NutanixUser,
        name="Nutanix Password",
        type="PASSWORD",
        password=NutanixPassword,
        default=True
    )

PrismCentralUser = os.environ['PRISM_CENTRAL_USER']
PrismCentralPassword = os.environ['PRISM_CENTRAL_PASS']
PrismCentralCred = basic_cred(
        PrismCentralUser,
        name="Prism Central User",
        type="PASSWORD",
        password=PrismCentralPassword,
        default=False
    )

PrismElementUser = os.environ['PRISM_ELEMENT_USER']
PrismElementPassword = os.environ['PRISM_ELEMENT_PASS']
PrismElementCred = basic_cred(
        PrismElementUser,
        name="Prism Element User",
        type="PASSWORD",
        password=PrismElementPassword,
        default=False
    )

EncrypedPrismCentralCreds = base64.b64encode(bytes(PrismCentralPassword, 'utf-8'))

EncrypedPrismElementCreds = base64.b64encode(bytes(PrismElementPassword, 'utf-8'))

# OS Image details for VM
Centos74_Image = "CentOS7.qcow2"

class Bastion_HostVmResources(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromImageService(Centos74_Image, bootable=True),
    ]

    nics = [
        AhvVmNic.DirectNic.ingress(subnet=os.getenv("IPAM_VLAN")),
    ]

    boot_type = "BIOS"

    guest_customization = AhvVmGC.CloudInit(filename="scripts/guest_customizations/guest_cus.yaml")

class Bastion_HostProfile(VmProfile):

    # Vm Spec for Substrate
    provider_spec = ahv_vm(resources=Bastion_HostVmResources, name="bastion-host-svm-@@{calm_unique}@@")

    # os_type = "Linux"
    # readiness_probe = {
    #     "disabled": False,
    #     "delay_secs": "15",
    #     "connection_type": "SSH",
    #     "connection_port": 22,
    #     "credential": ref(NutanixCred),
    # }

    @action
    def __pre_create__():
        CalmTask.SetVariable.escript(
            name="Set Lowercase App Name",
            filename="../../_common/centos/scripts/set_lower_case_app_name.py",
            variables=["app_name"],
        )

    # Package Actions
    @action
    def __install__():
        CalmTask.Exec.ssh(
            name="Configure User",
            filename="../../_common/centos/scripts/configure_user.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Intall Docker",
            filename="../../_common/centos/scripts/install_docker.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Intall Docker Compose",
            filename="../../_common/centos/scripts/install_docker_compose.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Kube CTL",
            filename="../../_common/centos/scripts/install_kubectl.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Configure Kubectl Aliases",
            filename="../../_common/centos/scripts/configure_kubectl_aliases.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Kubectx and Kubens",
            filename="../../_common/centos/scripts/install_kubectx_kubens.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Kube PS1",
            filename="../../_common/centos/scripts/install_kube-ps1.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Kubectl Krew Package Manager",
            filename="../../_common/centos/scripts/install_kubectl_krew.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Stern",
            filename="../../_common/centos/scripts/install_stern.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install JQ",
            filename="../../_common/centos/scripts/install_jq.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Packages",
            filename="../../_common/centos/scripts/install_required_packages.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Helm",
            filename="../../_common/centos/scripts/install_helm.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Vim",
            filename="../../_common/centos/scripts/install_vim.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Download DSL",
            filename="../../_common/centos/scripts/download_dsl.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Prereqs",
            filename="../../_common/centos/scripts/install_dsl_prereqs.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Setup DSL Environment",
            filename="../../_common/centos/scripts/setup_dsl_environment.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Configure DSL Connectivity",
            filename="../../_common/centos/scripts/configure_dsl_connectivity.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install karbonctl",
            filename="../../_common/karbon/scripts/get_karbonctl.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Azure Cli",
            filename="../../_common/centos/scripts/install_azure_cli.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Terraform",
            filename="../../_common/centos/scripts/install_terraform.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install GoLang",
            filename="../../_common/centos/scripts/install_golang.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install AWS Cli",
            filename="../../_common/centos/scripts/install_aws_cli.sh",
            cred=NutanixCred
        )

        # CalmTask.Exec.ssh(
        #     name="Install AWS IAM Authenticator",
        #     filename="../../_common/centos/scripts/install_aws_iam_authenticator.sh",
        #     cred=NutanixCred
        # )

        CalmTask.Exec.ssh(
            name="Install EKS Ctl",
            filename="../../_common/centos/scripts/install_eksctl.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Gcloud Cli",
            filename="../../_common/centos/scripts/install_gcloud_cli.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install ArgoCD Cli",
            filename="../../_common/centos/scripts/install_argocd_cli.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Vault Cli",
            filename="../../_common/centos/scripts/install_vault_cli.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Istio Cli",
            filename="../../_common/centos/scripts/install_istio_cli.sh",
            cred=NutanixCred
        )

        CalmTask.Exec.ssh(
            name="Install Openshift Cli",
            filename="../../_common/centos/scripts/install_openshift_cli.sh",
            cred=NutanixCred
        )

    nutanix_public_key = CalmVariable.Simple.Secret(
        NutanixPublicKey,
        label="Nutanix Public Key",
        is_hidden=True,
        description="SSH public key for the Nutanix user."
    )
    domain_name = CalmVariable.Simple(
        os.getenv("DOMAIN_NAME"),
        label="Domain Name",
        is_mandatory=True,
        runtime=True,
        description="Domain name used as suffix for FQDN. Entered similar to 'test.lab' or 'lab.local'."
    )
    pc_instance_port = CalmVariable.Simple.string(
        "9440",
        label="Prism Central Port Number",
        is_mandatory=True,
        runtime=True,
        description="IP address of the Prism Central instance that manages this Calm instance."
    )
    pc_instance_ip = CalmVariable.Simple.string(
        os.getenv("PC_IP_ADDRESS"),
        label="Prism Central IP",
        is_mandatory=True,
        runtime=True,
        description="IP address of the Prism Central instance that manages this Calm instance."
    )


class Bastion_Host(VmBlueprint):

    # Credentials for blueprint
    credentials = [
        NutanixCred,
        NutanixPasswordCred,
        PrismCentralCred,
      ]

    profiles = [Bastion_HostProfile]


class Bastion_HostMetadata(Metadata):

    categories = {"TemplateType": "Vm"}
