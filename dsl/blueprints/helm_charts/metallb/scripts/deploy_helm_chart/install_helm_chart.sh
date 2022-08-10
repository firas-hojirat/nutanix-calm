K8S_CLUSTER_NAME=@@{k8s_cluster_name}@@

METALLB_NET_RANGE=@@{metallb_network_range}@@
METALLB_CHART_VERSION=0.13.4

export KUBECONFIG=~/${K8S_CLUSTER_NAME}.cfg

echo "Install MetalLB"
## Create namespace regardless if it exists
kubectl create ns metallb-system -o yaml --dry-run=client | kubectl apply -f -

# Create metallb memberlist secret with layer2 details
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

while [[ $(kubectl get pods -l app.kubernetes.io/component=controller -n metallb-system -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do 
  echo "waiting for controller pods to be ready to ensure webhook services are up and running" && sleep 1;
done

echo "Configure MetalLB IPAddressPool Custom Resource"

cat <<EOF | kubectl apply -f -
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
