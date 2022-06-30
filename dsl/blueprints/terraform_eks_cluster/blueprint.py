# THIS FILE IS AUTOMATICALLY GENERATED.
"""
Calm DSL for Terraform Cluster blueprint

"""

k8s_distro_name = "Eks"
terrafom_repo_name = "eks_cluster"

import base64
import os
import json
from calm.dsl.builtins import *
from calm.dsl.config import get_context

ContextObj = get_context()
init_data = ContextObj.get_init_config()

if file_exists(os.path.join(init_data["LOCAL_DIR"]["location"], "nutanix_key_user")):
    NutanixKeyUser = read_local_file("nutanix_key_user")
else:
    NutanixKeyUser = "nutanix"

if file_exists(os.path.join(init_data["LOCAL_DIR"]["location"], "nutanix_user")):
    NutanixUser = read_local_file("nutanix_user")
else:
    NutanixUser = "nutanix"

if file_exists(os.path.join(init_data["LOCAL_DIR"]["location"], "prism_central_user")):
    PrismCentralUser = read_local_file("prism_central_user")
else:
    PrismCentralUser = "admin"

if file_exists(os.path.join(init_data["LOCAL_DIR"]["location"], "prism_element_user")):
    PrismElementUser = read_local_file("prism_element_user")
else:
    PrismElementUser = "admin"

NutanixPublicKey = read_local_file("nutanix_public_key")
NutanixKey = read_local_file("nutanix_key")

NutanixCred = basic_cred(
        NutanixKeyUser,
        name="Nutanix",
        type="KEY",
        password=NutanixKey,
        default=True
    )

NutanixPassword = read_local_file("nutanix_password")
NutanixPasswordCred = basic_cred(
        NutanixUser,
        name="Nutanix Password",
        type="PASSWORD",
        password=NutanixPassword,
        default=True
    )

PrismCentralPassword = read_local_file("prism_central_password")
PrismCentralCred = basic_cred(
        PrismCentralUser,
        name="Prism Central User",
        type="PASSWORD",
        password=PrismCentralPassword,
        default=False
    )

EncrypedPrismCentralCreds = base64.b64encode(bytes(PrismCentralPassword, 'utf-8'))

# PrismElementPassword = read_local_file("prism_element_password")
# PrismElementCred = basic_cred(
#         PrismElementUser,
#         name="Prism Element User",
#         type="PASSWORD",
#         password=PrismElementPassword,
#         default=False
#     )

# EncrypedPrismElementCreds = base64.b64encode(bytes(PrismElementPassword, 'utf-8'))

TerraformServiceAccountUser = read_local_file("aws_access_key_id")
TerraformServiceAccountPassword = read_local_file("aws_secret_access_key")
TerraformServiceAccountCred = basic_cred(
        TerraformServiceAccountUser,
        name="Terraform Service Account User",
        type="PASSWORD",
        password=TerraformServiceAccountPassword,
        default=False
    )

KarbonctlEnpoint = os.getenv("KARBONCTL_WS_ENDPOINT")

class Terraform_WorkstationService(Service):
    """Workstation Service"""

    @action
    def DeployTerraformCluster(name="Deploy " + terraform_name):
        CalmTask.Exec.ssh(
            name="Clone Terraform Repo",
            filename="scripts/terraform_deploy/clone_repo.sh",
            cred=NutanixCred
        )
        CalmTask.Exec.ssh(
            name="Initialize Terraform",
            filename="scripts/terraform_deploy/initialize_terraform.sh",
            cred=NutanixCred
        )
        CalmTask.Exec.ssh(
            name="Apply Terraform",
            filename="scripts/terraform_deploy/terraform_apply.sh",
            cred=NutanixCred
        )
        CalmTask.Exec.ssh(
            name="Validate " + terraform_name",
            filename="scripts/terraform_deploy/validate_k8s_cluster.sh",
            cred=NutanixCred
        )


    @action
    def Terraform_Scale_In_Cluster():
        ScaleIn = CalmVariable.Simple.int(
            "1",
            label="",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.ssh(
            name="Scale_In_Cluster",
            filename="scripts/day_two_actions/terraform_scale_in.sh",
            cred=NutanixCred
        )

    @action
    def Terraform_Scale_Out_Cluster():
        ScaleOut = CalmVariable.Simple.int(
            "1",
            label="",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.ssh(
            name="Scale_Out_Cluster",
            filename="scripts/day_two_actions/terraform_scale_out.sh",
            cred=NutanixCred
        )


    @action
    def Terraform_Destroy_Cluster():

        CalmTask.Exec.ssh(
            name="Terraform_Destroy_Cluster",
            filename="scripts/day_two_actions/terraform_destroy.sh",
            cred=NutanixCred
        )

    @action
    def __delete__():
        """System action for deleting an application. Deletes created VMs as well"""

        Terraform_WorkstationService.Terraform_Destroy_Cluster(name="Terraform_Destroy_Cluster")


class Terraform_WorkstationPackage(Package):
    """Workstation Package"""

    # Services created by installing this Package
    services = [ref(Terraform_WorkstationService)]

    @action
    def __install__():
        Terraform_WorkstationService.DeployTerraformCluster(name="Deploy " + terrafom_repo_name + " Cluster")


class Terraform_WorkstationSubstrate(Substrate):
    name = "Admin Workstation VM"

    os_type = "Linux"
    provider_type = "EXISTING_VM"
    provider_spec = read_provider_spec(os.path.join("image_configs", "karbonctl_workstation_provider_spec.yaml"))

    provider_spec.spec["address"] = KarbonctlEnpoint

    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=False,
        retries="5",
        connection_port=22,
        address=KarbonctlEnpoint,
        delay_secs="60",
        credential=ref(NutanixCred),
    )


class Terraform_WorkstationDeployment(Deployment):
    """Workstation Deployment"""

    packages = [ref(Terraform_WorkstationPackage)]
    substrate = ref(Terraform_WorkstationSubstrate)


class Terraform_WorkstationProfile(Profile):

    # Deployments under this profile
    deployments = [Terraform_WorkstationDeployment]

    nutanix_public_key = CalmVariable.Simple.Secret(
        NutanixPublicKey,
        label="Nutanix Public Key",
        is_hidden=True,
        description="SSH public key for the Nutanix user."
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

    @action
    def ScaleOut():
        """This action will scale out worker nodes by given scale out count"""

        ScaleOut = CalmVariable.Simple.int(
            "1",
            label="",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        Terraform_WorkstationService.Terraform_Scale_Out_Cluster(name="Terraform_Scale_Out_Cluster")

    @action
    def ScaleIn():
        """This action will scale in workder nodes by given scale in count"""

        ScaleIn = CalmVariable.Simple.int(
            "1",
            label="",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        Terraform_WorkstationService.Terraform_Scale_In_Cluster(name="Terraform_Scale_In_Cluster")

    # @action
    # def UpgradeRke():
    #     """This action will upgrade the Rke cluster to a new version"""

    #     ANTHOS_VERSION = CalmVariable.Simple(
    #         "",
    #         label="Rke cluster version",
    #         regex="^(\d+\.)?(\d+\.)?(\*|\d+)$",
    #         validate_regex=True,
    #         is_mandatory=True,
    #         is_hidden=False,
    #         runtime=True,
    #         description="The only supported version is 1.6.1, but 1.6.2 or 1.7.0 can be tested.",
    #     )
    #     AdminVM.Terraform_Upgrade_Cluster(name="Terraform_Upgrade_Cluster")


class Terraform_Workstation(Blueprint):
    """ Blueprint for Terraform_Workstation app using AHV VM"""

    credentials = [
            NutanixCred,
            NutanixPasswordCred,
            PrismCentralCred,
            TerraformServiceAccountCred,
    ]
    services = [Terraform_WorkstationService]
    packages = [Terraform_WorkstationPackage]
    substrates = [Terraform_WorkstationSubstrate]
    profiles = [Terraform_WorkstationProfile]
