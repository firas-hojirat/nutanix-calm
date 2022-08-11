NAMESPACE=@@{namespace}@@
INSTANCE_NAME=@@{instance_name}@@
K8S_CLUSTER_NAME=@@{k8s_cluster_name}@@

METALLB_NET_RANGE=@@{metallb_network_range}@@
METALLB_CHART_VERSION=0.13.4

## TEST DATA ONLY: 
## METALLB_NET_RANGE=10.38.11.16-10.38.11.18
## METALLB_CHART_VERSION=0.13.4

echo "Login karbonctl"
karbonctl login --pc-ip @@{pc_instance_ip}@@ --pc-port @@{pc_instance_port}@@ --pc-username @@{Prism Central User.username}@@ --pc-password @@{Prism Central User.secret}@@

echo "Set KUBECONFIG"
karbonctl cluster kubeconfig --cluster-name ${K8S_CLUSTER_NAME} > ~/${K8S_CLUSTER_NAME}.cfg

export KUBECONFIG=~/${K8S_CLUSTER_NAME}.cfg

echo "Install MetalLB"

## Create namespace regardless if it exists
kubectl create ns metallb-system --save-config -o yaml --dry-run=client | kubectl apply -f -

# create metallb memberlist secret with layer2 details
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"

# install metallb via helm
helm repo add metallb https://metallb.github.io/metallb
helm repo update
helm search repo metallb/metallb
helm upgrade --install metallb metallb/metallb \
	--namespace metallb-system \
	--set controller.rbac.create=true	\
  --version=${METALLB_CHART_VERSION} \
	--wait

kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=metallb -n metallb-system

while [[ -z $(kubectl get ep metallb-webhook-service -n metallb-system -o jsonpath='{.subsets[].addresses[]}' 2>/dev/null) ]]; do
  echo "waiting for metallb-webhook-service endpoints to be up and running to avoid internal webhook request failures..."
  sleep 1
done

echo "Configure MetalLB IPAddressPool Custom Resource"

cat <<EOF | kubectl apply -n metallb-system -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-metallb-ippool
  namespace: metallb-system
spec:
  addresses:
  - $(echo ${METALLB_NET_RANGE})
EOF

## validate ip pool was created in metallb-system namespace
kubectl get ipaddresspool -n metallb-system -o yaml