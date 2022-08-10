
## Calico Instructions Walkthrough

Below is a step by step breakdown review of the Calico Configs provided

### Applying 01_calico.yaml

In comparing 01_calico.yaml - this setting was configured on Karbon, but set to `none` in version:

  `typha_service_name: calico-typha`

Looks like we enable for scaling / performance reasons: https://docs.projectcalico.org/reference/typha/overview

Listing of calico crds found within Karbon Cluster. An `x` was placed next to each one found in corresponding `01_calico.yaml`  Looks like we're running later version of calico (3.10.0 vs. 3.14.0)

```bash
❯ kubectl get crds | grep calico                                                                                                                                             ─╯
bgpconfigurations.crd.projectcalico.org               2022-07-27T22:05:25Z
bgppeers.crd.projectcalico.org                        2022-07-27T22:05:25Z
blockaffinities.crd.projectcalico.org                 2022-07-27T22:05:24Z
clusterinformations.crd.projectcalico.org             2022-07-27T22:05:25Z
felixconfigurations.crd.projectcalico.org             2022-07-27T22:05:24Z
globalnetworkpolicies.crd.projectcalico.org           2022-07-27T22:05:25Z
globalnetworksets.crd.projectcalico.org               2022-07-27T22:05:25Z
hostendpoints.crd.projectcalico.org                   2022-07-27T22:05:25Z
ipamblocks.crd.projectcalico.org                      2022-07-27T22:05:24Z
ipamconfigs.crd.projectcalico.org                     2022-07-27T22:05:24Z
ipamhandles.crd.projectcalico.org                     2022-07-27T22:05:24Z
ippools.crd.projectcalico.org                         2022-07-27T22:05:25Z
kubecontrollersconfigurations.crd.projectcalico.org   2022-07-27T22:05:25Z
networkpolicies.crd.projectcalico.org                 2022-07-27T22:05:25Z
networksets.crd.projectcalico.org                     2022-07-27T22:05:25Z
```

RBAC Access Matrix

```bash
$ kubectl-access_matrix --sa kube-system:calico-node
NAME                                                          LIST  CREATE  UPDATE  DELETE
alertmanagers.monitoring.coreos.com                           ✖     ✖       ✖       ✖
apiservices.apiregistration.k8s.io                            ✖     ✖       ✖       ✖
bgpconfigurations.crd.projectcalico.org                       ✔     ✔       ✔       ✖
bgppeers.crd.projectcalico.org                                ✔     ✔       ✔       ✖
bindings                                                            ✖
blockaffinities.crd.projectcalico.org                         ✔     ✔       ✔       ✔
certificaterequests.cert-manager.io                           ✖     ✖       ✖       ✖
certificates.cert-manager.io                                  ✖     ✖       ✖       ✖
certificatesigningrequests.certificates.k8s.io                ✖     ✖       ✖       ✖
challenges.acme.cert-manager.io                               ✖     ✖       ✖       ✖
clusterinformations.crd.projectcalico.org                     ✔     ✔       ✔       ✖
clusterissuers.cert-manager.io                                ✖     ✖       ✖       ✖
clusterrolebindings.rbac.authorization.k8s.io                 ✖     ✖       ✖       ✖
clusterroles.rbac.authorization.k8s.io                        ✖     ✖       ✖       ✖
componentstatuses                                             ✖
configmaps                                                    ✖     ✖       ✖       ✖
controllerrevisions.apps                                      ✖     ✖       ✖       ✖
cronjobs.batch                                                ✖     ✖       ✖       ✖
csidrivers.storage.k8s.io                                     ✖     ✖       ✖       ✖
csinodes.storage.k8s.io                                       ✖     ✖       ✖       ✖
customresourcedefinitions.apiextensions.k8s.io                ✖     ✖       ✖       ✖
daemonsets.apps                                               ✖     ✖       ✖       ✖
deployments.apps                                              ✖     ✖       ✖       ✖
endpoints                                                     ✔     ✖       ✖       ✖
endpointslices.discovery.k8s.io                               ✖     ✖       ✖       ✖
events                                                        ✖     ✖       ✖       ✖
events.events.k8s.io                                          ✖     ✖       ✖       ✖
felixconfigurations.crd.projectcalico.org                     ✔     ✔       ✔       ✖
globalnetworkpolicies.crd.projectcalico.org                   ✔     ✖       ✖       ✖
globalnetworksets.crd.projectcalico.org                       ✔     ✖       ✖       ✖
horizontalpodautoscalers.autoscaling                          ✖     ✖       ✖       ✖
hostendpoints.crd.projectcalico.org                           ✔     ✖       ✖       ✖
ingressclasses.networking.k8s.io                              ✖     ✖       ✖       ✖
ingresses.extensions                                          ✖     ✖       ✖       ✖
ingresses.networking.k8s.io                                   ✖     ✖       ✖       ✖
ipamblocks.crd.projectcalico.org                              ✔     ✔       ✔       ✔
ipamconfigs.crd.projectcalico.org                             ✖     ✖       ✖       ✖
ipamhandles.crd.projectcalico.org                             ✔     ✔       ✔       ✔
ippools.crd.projectcalico.org                                 ✔     ✔       ✔       ✖
issuers.cert-manager.io                                       ✖     ✖       ✖       ✖
jobs.batch                                                    ✖     ✖       ✖       ✖
kubecontrollersconfigurations.crd.projectcalico.org           ✖     ✖       ✖       ✖
leases.coordination.k8s.io                                    ✖     ✖       ✖       ✖
limitranges                                                   ✖     ✖       ✖       ✖
localsubjectaccessreviews.authorization.k8s.io                      ✖
mutatingwebhookconfigurations.admissionregistration.k8s.io    ✖     ✖       ✖       ✖
namespaces                                                    ✔     ✖       ✖       ✖
networkpolicies.crd.projectcalico.org                         ✔     ✖       ✖       ✖
networkpolicies.networking.k8s.io                             ✔     ✖       ✖       ✖
networksets.crd.projectcalico.org                             ✔     ✖       ✖       ✖
nodes                                                         ✔     ✖       ✖       ✖
nodes.metrics.k8s.io                                          ✖
orders.acme.cert-manager.io                                   ✖     ✖       ✖       ✖
persistentvolumeclaims                                        ✖     ✖       ✖       ✖
persistentvolumes                                             ✖     ✖       ✖       ✖
poddisruptionbudgets.policy                                   ✖     ✖       ✖       ✖
podmonitors.monitoring.coreos.com                             ✖     ✖       ✖       ✖
pods                                                          ✔     ✖       ✖       ✖
pods.metrics.k8s.io                                           ✖
podsecuritypolicies.policy                                    ✖     ✖       ✖       ✖
podtemplates                                                  ✖     ✖       ✖       ✖
priorityclasses.scheduling.k8s.io                             ✖     ✖       ✖       ✖
prometheuses.monitoring.coreos.com                            ✖     ✖       ✖       ✖
prometheusrules.monitoring.coreos.com                         ✖     ✖       ✖       ✖
replicasets.apps                                              ✖     ✖       ✖       ✖
replicationcontrollers                                        ✖     ✖       ✖       ✖
resourcequotas                                                ✖     ✖       ✖       ✖
rolebindings.rbac.authorization.k8s.io                        ✖     ✖       ✖       ✖
roles.rbac.authorization.k8s.io                               ✖     ✖       ✖       ✖
runtimeclasses.node.k8s.io                                    ✖     ✖       ✖       ✖
secrets                                                       ✖     ✖       ✖       ✖
selfsubjectaccessreviews.authorization.k8s.io                       ✔
selfsubjectrulesreviews.authorization.k8s.io                        ✔
serviceaccounts                                               ✔     ✖       ✖       ✖
servicemonitors.monitoring.coreos.com                         ✖     ✖       ✖       ✖
services                                                      ✔     ✖       ✖       ✖
statefulsets.apps                                             ✖     ✖       ✖       ✖
storageclasses.storage.k8s.io                                 ✖     ✖       ✖       ✖
subjectaccessreviews.authorization.k8s.io                           ✖
tokenreviews.authentication.k8s.io                                  ✖
validatingwebhookconfigurations.admissionregistration.k8s.io  ✖     ✖       ✖       ✖
volumeattachments.storage.k8s.io                              ✖     ✖       ✖       ✖
```

> calico daemonset/deployment comparison between karbon and provided

Screenshots of parameters below - nothing critical that stands out, imho

![](typha_service_name.png)

![](ipv4pool_cidr.png)

![](ip_auth_method.png)

### Label Nodes

> Node labels will be fine, just need to be cognizant of new worker nodes that will not have by default...Could include in Calm Workflow when adding nodes

```
$ kubectl get nodes -o name | cut -d/ -f2 | xargs -I {} kubectl exec -i -n kube-system calicoctl -- /calicoctl label nodes {} inside-node='' --overwrite
Successfully set label inside-node on nodes karbon-kalm-main-0d721d-k8s-master-0
Successfully set label inside-node on nodes karbon-kalm-main-0d721d-k8s-master-1
Successfully set label inside-node on nodes karbon-kalm-main-0d721d-k8s-worker-0
Successfully set label inside-node on nodes karbon-kalm-main-0d721d-k8s-worker-1
Successfully set label inside-node on nodes karbon-kalm-main-0d721d-k8s-worker-2
```

k8s-app=calico-node

kubectl get nodes -o name | cut -d/ -f2 | xargs -I {} kubectl exec -i -n kube-system calicoctl -- /calicoctl get nodes {} --export -o yaml | grep -B 3 -A 2 inside-node

```
$ kubectl get nodes -o name | cut -d/ -f2 | xargs -I {} kubectl exec -i -n kube-system calicoctl -- /calicoctl get nodes {} --export -o yaml | grep -B 3 -A 2 inside-node
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    inside-node: ""
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-0d721d-k8s-master-0
--
--
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    inside-node: ""
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-0d721d-k8s-master-1
--
--
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    inside-node: ""
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-0d721d-k8s-worker-0
--
--
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    inside-node: ""
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-0d721d-k8s-worker-1
--
--
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    inside-node: ""
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-0d721d-k8s-worker-2
```

### 02-04 Node Configurations

$ kubectl get nodes -o name | cut -d/ -f2 | xargs -I {} kubectl exec -i -n kube-system calicoctl -- /calicoctl get nodes {} --export -o yaml > calicoctl-karbon-get-all-nodes.yaml

> In reviewing calicoctl-karbon-get-all-nodes.yaml, the only difference was AS Number for BGP specs.

![](bgp_specs_as_num.png)

### 05 BGP Peer Configurations

Karbon doesn't have any default related configs and should not conflict / impact any of these configs.

![](bgp_peers_config.png)

### 06 Network Pool Configurations

Below is Karbon Default Config IPAM Pool.

Having separate subnets for Control Plane vs. Worker Nodes would not be configured during initial install / config and may be overwritten on upgrade.  Would need further validation if required.

$ kubectl get ippool default-ipv4-ippool -o yaml

![](default_ipam_pool.png)

vs.

![](inside-vs-master-ipv4.png)

### 07 Disable Node to Node ServiceMesh

Default config for Karbon is Node to Node Service Mesh.

![](bgp_config.png)

### 08-12 Master Configs

Same as 02-04 Node Configs listed above.

### 13 Master BGP Peers config

No concerns with following config

![](master_bgp_peers_config.png)

### 14-18 Worker Configs

Same as 02-04 Node Configs listed above.

### 19 Calico Upgrade

Karbon is running at 3.14.0, and upgrades are handled accordingly via Karbon automation.


## Setup Calico BGP Peering

https://github.com/osrg/gobgp/blob/master/docs/sources/cli-operations.md

GoBGP is an open source Border Gateway Protocol (BGP) implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

https://osrg.github.io/gobgp/
  - https://github.com/osrg/gobgp

rr.conf
```bash
[global.config]
  as = 64496
  router-id = "192.0.2.1"

[[dynamic-neighbors]]
  [dynamic-neighbors.config]
    prefix = "0.0.0.0/0"
    peer-group = "k8s-group"

[[peer-groups]]
  [peer-groups.config]
    peer-group-name = "k8s-group"
    peer-as = 64496
  [peer-groups.transport.config]
    passive-mode = true
  [peer-groups.route-reflector.config]
    route-reflector-client = true
    route-reflector-cluster-id = "192.0.2.1"
  [[peer-groups.afi-safis]]
    [peer-groups.afi-safis.config]
      afi-safi-name = "ipv4-unicast"
```

```bash
$ k get bgppeers gobgp-peer-updated -o yaml
apiVersion: crd.projectcalico.org/v1
kind: BGPPeer
metadata:
  name: gobgp-peer-updated
spec:
  asNumber: 64496
  nodeSelector: all()
  peerIP: 172.18.0.5
```

```bash
$ k get bgpconfigurations.crd.projectcalico.org default -o yaml
apiVersion: crd.projectcalico.org/v1
kind: BGPConfiguration
metadata:
  name: default
spec:
  asNumber: 64496
  nodeToNodeMeshEnabled: false
```


- Validating Default Calicoctl configurations in Karbon

Test Environment:

- Karbon (2.4), Kubernetes Production Cluster v1.21.8, Node OS (ntnx-1.2), Calico v3.21.4
- AHV VM Network: 10.38.11.0/26
- Default POD CIDR Network: 172.20.0.0/16
- Default Service CIDR Network: 172.19.0.0/16

❯ calicoctl get nodes -o wide                                                                                                                                                                       ─╯
NAME                                        ASN       IPV4             IPV6   
karbon-kalm-main-11-1-83b32f-k8s-master-0   (64512)   10.38.11.32/26          
karbon-kalm-main-11-1-83b32f-k8s-master-1   (64512)   10.38.11.47/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-0   (64512)   10.38.11.33/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-1   (64512)   10.38.11.44/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-2   (64512)   10.38.11.41/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-3   (64512)   10.38.11.36/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-4   (64512)   10.38.11.52/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-5   (64512)   10.38.11.61/26          
karbon-kalm-main-11-1-83b32f-k8s-worker-6   (64512)   10.38.11.56/26  
                                                                                                                                                                        ─╯
❯ calicoctl get ippools -o wide                                                                                                                                           ─╯
NAME                  CIDR            NAT    IPIPMODE   VXLANMODE   DISABLED   DISABLEBGPEXPORT   SELECTOR
default-ipv4-ippool   172.20.0.0/16   true   Never      Never       false      false              all()

setup bgp router 

make gobgp-build && make gobgp-rr

sudo calicoctl node status
Calico process is running.

IPv4 BGP status
+--------------+-------------------+-------+----------+-------------+
| PEER ADDRESS |     PEER TYPE     | STATE |  SINCE   |    INFO     |
+--------------+-------------------+-------+----------+-------------+
| 10.38.11.32  | node-to-node mesh | up    | 19:13:45 | Established |
| 10.38.11.47  | node-to-node mesh | up    | 19:15:19 | Established |
| 10.38.11.44  | node-to-node mesh | up    | 19:15:46 | Established |
| 10.38.11.41  | node-to-node mesh | up    | 19:16:17 | Established |
| 10.38.11.36  | node-to-node mesh | up    | 19:13:43 | Established |
| 10.38.11.52  | node-to-node mesh | up    | 19:13:43 | Established |
| 10.38.11.61  | node-to-node mesh | up    | 19:14:46 | Established |
| 10.38.11.56  | node-to-node mesh | up    | 19:14:16 | Established |
+--------------+-------------------+-------+----------+-------------+


calicoctl get node karbon-kalm-main-11-1-83b32f-k8s-worker-0 -o yaml --export > node.yaml

cat <<EOF | kubectl apply -f -
apiVersion: projectcalico.org/v3
kind: Node
metadata:
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    karbon-default: "true"
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: karbon-kalm-main-11-1-83b32f-k8s-worker-0
    kubernetes.io/os: linux
    kubernetes.io/role: node
    node.kubernetes.io/node: ""
    calico-route-reflector: ""
  name: karbon-kalm-main-11-1-83b32f-k8s-worker-0
spec:
  addresses:
  - address: 10.38.11.33/26
    type: CalicoNodeIP
  - address: 10.38.11.33
    type: InternalIP
  bgp:
    routeReflectorClusterID: 192.168.0.1
    ipv4Address: 10.38.11.33/26
  orchRefs:
  - nodeName: karbon-kalm-main-11-1-83b32f-k8s-worker-0
    orchestrator: k8s
EOF
