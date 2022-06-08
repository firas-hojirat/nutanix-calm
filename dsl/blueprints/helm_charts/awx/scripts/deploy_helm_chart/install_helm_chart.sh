WILDCARD_INGRESS_DNS_FQDN=@@{wildcard_ingress_dns_fqdn}@@
NIPIO_INGRESS_DOMAIN=@@{nipio_ingress_domain}@@
NAMESPACE=@@{namespace}@@
INSTANCE_NAME=@@{instance_name}@@
K8S_CLUSTER_NAME=@@{k8s_cluster_name}@@

## configure admin user
AWX_USER=@@{Awx User.username}@@
AWX_PASS=@@{Awx User.secret}@@

## See https://github.com/ansible/awx-operator#helm-install-on-existing-cluster for additional helm options

## install helm awx-operator first, then create instance
helm repo add awx-operator https://ansible.github.io/awx-operator/
helm repo update
helm search repo awx-operator
helm upgrade --install ${INSTANCE_NAME} awx-operator/awx-operator \
	--namespace ${NAMESPACE} \
  --create-namespace \
	--wait

helm status ${INSTANCE_NAME} -n ${NAMESPACE}

kubectl wait --for=condition=Ready -l control-plane=controller-manager pod -A --timeout=5m

## create instance

kubectl create secret generic awx-admin-password --from-literal=password=$AWX_PASS

cat <<EOF | kubectl apply -f  -
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx
spec:
  admin_user: $(echo $AWX_USER)
  admin_password_secret: awx-admin-password
  hostname: $INSTANCE_NAME.$NIPIO_INGRESS_DOMAIN
  ingress_type: ingress
  ingress_tls_secret: aws-ingress-tls
  ingress_annotations: |
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "selfsigned-cluster-issuer"
EOF

kubectl wait --for=condition=Ready -l app.kubernetes.io/instance=postgres-awx pod -A --timeout=5m
kubectl wait --for=condition=Ready -l app.kubernetes.io/name=awx pod -A --timeout=5m

kubectl describe awx -n awx

echo "Navigate to https://${INSTANCE_NAME}.${NIPIO_INGRESS_DOMAIN} via browser to access instance"
