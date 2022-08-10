REQUIRED_TOOLS_LIST += kubectl kubectl-krew kubectl-karbon jq

download-karbon-creds download-all-karbon-cfgs merge-karbon-contexts fix-image-pull-secrets: print-vars

.PHONY: download-karbon-creds
download-karbon-creds: ### Leverage karbon krew/kubectl plugin to login and download config and ssh keys
	[ -n "$$(kubectl karbon version)" ] || kubectl krew update && kubectl krew install karbon
	@KARBON_PASSWORD=${PC_PASSWORD} kubectl karbon login -k --server ${PC_IP_ADDRESS} --cluster ${KARBON_CLUSTER} --user ${PC_USER} --kubeconfig ~/.kube/${KARBON_CLUSTER}.cfg --ssh-file --force
	@make merge-karbon-contexts

.PHONY: download-all-karbon-cfgs
download-all-karbon-cfgs: #### Download all kubeconfigs from all environments that have Karbon Cluster running
	@ls config/*/nutanix.ncmstate | cut -d/ -f2 | xargs -I {} sh -c 'jq -r ".entities[].status | select((.description | contains(\"karbon-clusters\")) and (.state == \"running\")) | .name " config/{}/nutanix.ncmstate' \
		| xargs -I {} grep -l {} config/*/nutanix.ncmstate | cut -d/ -f2 | xargs -I {} make download-karbon-creds ENVIRONMENT={} && echo "reload shell. i.e., source ~/.zshrc and run kubectx to switch clusters"

.PHONY: merge-karbon-contexts
merge-karbon-contexts: #### Merge all K8s cluster kubeconfigs within path to config file.  Needed to support multiple clusters in future
	@export KUBECONFIG=$$KUBECONFIG:~/.kube/${KARBON_CLUSTER}.cfg; \
		kubectl config view --flatten >| ~/.kube/config && chmod 600 ~/.kube/config;
	@kubectl config use-context ${KUBECTL_CONTEXT};
	@kubectl cluster-info

.PHONY: fix-image-pull-secrets
fix-image-pull-secrets: #### Add image pull secret to get around image download rate limiting issues
	@kubectl get ns -o name | cut -d / -f2 | xargs -I {} sh -c "kubectl create secret docker-registry image-pull-secret --docker-username=${DOCKER_HUB_USER} --docker-password=${DOCKER_HUB_PASS} -n {} --dry-run=client -o yaml | kubectl apply -f - "
	@kubectl get serviceaccount --no-headers --all-namespaces | awk '{ print $$1 , $$2 }' | xargs -n2 sh -c 'kubectl patch serviceaccount $$2 -p "{\"imagePullSecrets\": [{\"name\": \"image-pull-secret\"}]}" -n $$1' sh

