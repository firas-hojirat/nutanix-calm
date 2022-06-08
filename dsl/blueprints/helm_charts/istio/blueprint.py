
"""
Blueprint to Deploy Helm Chart onto Target Karbon Cluster
"""

## Update at minimum these vars
helm_chart_name = "Istio"
helm_chart_namespace = "istio-system"
helm_chart_instance_name = "istio"

import base64
import json
import os
from calm.dsl.builtins import *
from calm.dsl.config import get_context

ContextObj = get_context()
init_data = ContextObj.get_init_config()

PrismCentralUser = os.environ['PRISM_CENTRAL_USER']
PrismCentralPassword = os.environ['PRISM_CENTRAL_PASS']
PrismCentralCred = basic_cred(
                    PrismCentralUser,
                    name="Prism Central User",
                    type="PASSWORD",
                    password=PrismCentralPassword,
                    default=False
                )

EncrypedPrismCreds = base64.b64encode(bytes(PrismCentralPassword, 'utf-8'))

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

BastionHostEndpoint = os.getenv("BASTION_WS_ENDPOINT")

class HelmService(Service):

    name = "Helm_"+helm_chart_name

    @action
    def InstallHelmChart(name="Install "+helm_chart_name):
        CalmTask.Exec.ssh(
            name="Get Kubeconfig",
            filename="../../../_common/karbon/scripts/get_kubeconfig.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )
        CalmTask.Exec.ssh(
            name="Install "+helm_chart_name+" Helm Chart",
            filename="scripts/deploy_helm_chart/install_helm_chart.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )

    @action
    def UninstallHelmChart(name="Uninstall "+helm_chart_name):
        CalmTask.Exec.ssh(
            name="Get Kubeconfig",
            filename="../../../_common/karbon/scripts/get_kubeconfig.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )
        CalmTask.Exec.ssh(
            name="Uninstall "+helm_chart_name+" Helm Chart",
            filename="scripts/deploy_helm_chart/uninstall_helm_chart.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )

    @action
    def DeployDemoApp(name="Deploy "+helm_chart_name+" Demo App"):
        CalmTask.Exec.ssh(
            name="Get Kubeconfig",
            filename="../../../_common/karbon/scripts/get_kubeconfig.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )
        CalmTask.Exec.ssh(
            name="Deploy "+helm_chart_name+" Demo App",
            filename="scripts/day_two_actions/install_bookinfo_sample_app.sh",
            target=ref(HelmService),
            cred=ref(NutanixCred)
        )

class BastionHostWorkstation(Substrate):

    os_type = "Linux"
    provider_type = "EXISTING_VM"
    provider_spec = read_provider_spec(os.path.join("image_configs", "bastionctl_workstation_provider_spec.yaml"))

    provider_spec.spec["address"] = BastionHostEndpoint

    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=False,
        retries="5",
        connection_port=22,
        address=BastionHostEndpoint,
        delay_secs="60",
        credential=ref(NutanixCred),
    )


class HelmPackage(Package):

    services = [ref(HelmService)]

    @action
    def __install__():
        HelmService.InstallHelmChart(name="Install "+helm_chart_name)

    @action
    def __uninstall__():
        HelmService.UninstallHelmChart(name="Uninstall "+helm_chart_name)


class HelmDeployment(Deployment):

    name = "Helm Deployment"
    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(HelmPackage)]
    substrate = ref(BastionHostWorkstation)


class Default(Profile):

    deployments = [HelmDeployment]

    pc_instance_ip = CalmVariable.Simple(
        os.getenv("PC_IP_ADDRESS"),
        label="",
        is_mandatory=False,
        is_hidden=True,
        runtime=False,
        description="",
    )

    pc_instance_port = CalmVariable.Simple(
        "9440",
        label="",
        is_mandatory=False,
        is_hidden=True,
        runtime=False,
        description="",
    )

    instance_name = CalmVariable.Simple(
        helm_chart_instance_name,
        label=helm_chart_name+" Instance Name",
        is_mandatory=False,
        is_hidden=False,
        runtime=True,
        description="Helm Instance Release Name",
    )

    k8s_cluster_name = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename="../../../_common/karbon/scripts/get_karbon_cluster_list.py",
        ),
        label="Kubernetes Cluster Name",
        is_mandatory=True,
        is_hidden=False,
        description="Target Karbon Cluster Name",
    )

    namespace = CalmVariable.Simple(
        helm_chart_namespace,
        label=helm_chart_name+" Namespace",
        is_mandatory=False,
        is_hidden=False,
        runtime=True,
        description="Kubernetes Namespace to deploy helm chart",
    )

    enc_pc_creds = CalmVariable.Simple(
        EncrypedPrismCreds.decode("utf-8"),
        is_mandatory=True,
        is_hidden=True,
        runtime=False,
    )

    @action
    def DeployDemoApp(name="Deploy "+helm_chart_name+" Demo App"):
        """
    Deploy Bookinfo Demo Application
        """

        HelmService.DeployDemoApp(name="Deploy "+helm_chart_name+" Demo App")


class HelmBlueprint(Blueprint):

    services = [HelmService]
    packages = [HelmPackage]
    substrates = [BastionHostWorkstation]
    profiles = [Default]
    credentials = [PrismCentralCred, NutanixCred]
