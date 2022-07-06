
NAMESPACE=@@{namespace}@@
INSTANCE_NAME=@@{instance_name}@@
K8S_CLUSTER_NAME=@@{k8s_cluster_name}@@

export KUBECONFIG=~/${K8S_CLUSTER_NAME}_${INSTANCE_NAME}.cfg

GITHUB_USER=@@{GitHub User.username}@@
GITHUB_PASS=@@{GitHub User.secret}@@

# this step will fully delete helm chart and namespaces
kubectl config set-context --current --namespace=${NAMESPACE}
helm uninstall ${INSTANCE_NAME} --namespace=${NAMESPACE}
kubectl delete ns ${NAMESPACE}

rm ~/${K8S_CLUSTER_NAME}_${INSTANCE_NAME}.cfg


#runner-deployment-name=runner-deployment
#./config.sh remove --token TOKEN