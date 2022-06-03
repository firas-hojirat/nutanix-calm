# THIS FILE IS AUTOMATICALLY GENERATED.
"""
Calm DSL for Karbon_Admin_Workstation blueprint

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
#PrismElementPassword = read_local_file("prism_element_password")
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
Centos74_Image = vm_disk_package(
        name="centos7_generic",
        config_file="image_configs/centos74_disk.yaml"
    )

class Adm_WorkstationService(Service):
    """Workstation Service"""

    @action
    def ConfigureUser(name="Configure User"):
        CalmTask.Exec.ssh(
            name="Configure User",
            filename="../../_common/centos/scripts/configure_user.sh",
            cred=NutanixCred
        )

    @action
    def InstallDocker(name="Install Docker"):
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

    @action
    def InstallKubeCTL(name="Install kubectl"):
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

    @action
    def InstallPackages(name="Install Packages"):
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

    @action
    def InstallVim(name="Install Vim"):
        CalmTask.Exec.ssh(
            name="Install Vim",
            filename="../../_common/centos/scripts/install_vim.sh",
            cred=NutanixCred
        )

    @action
    def InstallDSL(name="Install Calm DSL"):
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


    @action
    def InstallKarbonCtl(name="Install Karbonctl"):
        CalmTask.Exec.ssh(
            name="Install karbonctl",
            filename="../../_common/karbon/scripts/get_karbonctl.sh",
            cred=NutanixCred
        )

    @action
    def InstallAzureCloudUtils(name="Install Azure Cloud Utilities"):
        CalmTask.Exec.ssh(
            name="Install Azure Cli",
            filename="../../_common/centos/scripts/install_azure_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallTerraform(name="Install Terraform"):
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

    @action
    def InstallAwsCloudUtils(name="Install AWS Cloud Utilities"):
        CalmTask.Exec.ssh(
            name="Install AWS Cli",
            filename="../../_common/centos/scripts/install_aws_cli.sh",
            cred=NutanixCred
        )
        CalmTask.Exec.ssh(
            name="Install AWS IAM Authenticator",
            filename="../../_common/centos/scripts/install_aws_iam_authenticator.sh",
            cred=NutanixCred
        )
        CalmTask.Exec.ssh(
            name="Install EKS Ctl",
            filename="../../_common/centos/scripts/install_eksctl.sh",
            cred=NutanixCred
        )

    @action
    def InstallGoogleCloudUtils(name="Install Google Cloud Utilities"):
        CalmTask.Exec.ssh(
            name="Install Gcloud Cli",
            filename="../../_common/centos/scripts/install_gcloud_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallArgoCdCli(name="Install ArgoCD CLI"):
        CalmTask.Exec.ssh(
            name="Install ArgoCD Cli",
            filename="../../_common/centos/scripts/install_argocd_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallRancherCli(name="Install Rancher CLI"):
        CalmTask.Exec.ssh(
            name="Install Rancher Cli",
            filename="../../_common/centos/scripts/install_rancher_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallVaultCli(name="Install Hashi Vault CLI"):
        CalmTask.Exec.ssh(
            name="Install Vault Cli",
            filename="../../_common/centos/scripts/install_vault_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallIstioCli(name="Install Istio CLI"):
        CalmTask.Exec.ssh(
            name="Install Istio Cli",
            filename="../../_common/centos/scripts/install_vault_cli.sh",
            cred=NutanixCred
        )

    @action
    def InstallOpenshiftCli(name="Install Openshift CLI"):
        CalmTask.Exec.ssh(
            name="Install Openshift Cli",
            filename="../../_common/centos/scripts/install_openshift_cli.sh",
            cred=NutanixCred
        )

class Adm_WorkstationPackage(Package):
    """Workstation Package"""

    # Services created by installing this Package
    services = [ref(Adm_WorkstationService)]

    @action
    def __install__():
        Adm_WorkstationService.ConfigureUser(name="Configure User")
        Adm_WorkstationService.InstallDocker(name="Install Docker")
        Adm_WorkstationService.InstallKubeCTL(name="Install KubeCTL")
        Adm_WorkstationService.InstallPackages(name="Install Required Packages")
        Adm_WorkstationService.InstallVim(name="Install Vim")
        Adm_WorkstationService.InstallDSL(name="Install Calm DSL")
        Adm_WorkstationService.InstallKarbonCtl(name="Install Karbonctl")
        Adm_WorkstationService.InstallTerraform(name="Install Terraform")
        Adm_WorkstationService.InstallAzureCloudUtils(name="Install Azure Cloud Utilities")
        Adm_WorkstationService.InstallAwsCloudUtils(name="Install AWS Cloud Utilities")
        Adm_WorkstationService.InstallGoogleCloudUtils(name="Install Google Cloud Utilities")
        Adm_WorkstationService.InstallArgoCdCli(name="Install ArgoCD CLI")
        #Adm_WorkstationService.InstallRancherCli(name="Install Rancher CLI")
        Adm_WorkstationService.InstallRancherCli(name="Install Vault CLI")
        Adm_WorkstationService.InstallIstioCli(name="Install Istio CLI")
        Adm_WorkstationService.InstallOpenshiftCli(name="Install Openshift CLI")

class Adm_WorkstationVmResources(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromVMDiskPackage(Centos74_Image, bootable=True)
    ]
    nics = [
        AhvVmNic.NormalNic(os.getenv("IPAM_VLAN")),
    ]

    boot_type = "BIOS"

    guest_customization = AhvVmGC.CloudInit(filename="scripts/guest_customizations/guest_cus.yaml")

class Adm_WorkstationVm(AhvVm):

    resources = Adm_WorkstationVmResources
    categories = {"AppFamily": "Demo", "AppType": "Default"}


class Adm_WorkstationSubstrate(Substrate):
    name = "Admin Workstation VM"

    provider_spec = Adm_WorkstationVm
    provider_spec.name = "admin-workstation-@@{calm_unique}@@"

    os_type = "Linux"
    readiness_probe = {
        "disabled": False,
        "delay_secs": "15",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(NutanixCred),
    }

    @action
    def __pre_create__():
        CalmTask.SetVariable.escript(
            name="Set Lowercase App Name",
            filename="../../_common/centos/scripts/set_lower_case_app_name.py",
            variables=["app_name"],
        )


class Adm_WorkstationDeployment(Deployment):
    """Workstation Deployment"""

    packages = [ref(Adm_WorkstationPackage)]
    substrate = ref(Adm_WorkstationSubstrate)


class Adm_WorkstationProfile(Profile):

    # Deployments under this profile
    deployments = [Adm_WorkstationDeployment]

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


class Adm_Workstation(Blueprint):
    """ Blueprint for Adm_Workstation app using AHV VM"""

    credentials = [
            NutanixCred,
            NutanixPasswordCred,
            PrismCentralCred,
            ]
    services = [Adm_WorkstationService]
    packages = [Adm_WorkstationPackage, Centos74_Image]
    substrates = [Adm_WorkstationSubstrate]
    profiles = [Adm_WorkstationProfile]
