REQUIRED_TOOLS_LIST += kind docker

KIND_CLUSTER_NAME ?= cloud-native-calm
KIND_NETWORK := kind
KUBECONFIG_PATH := $(HOME)/.kube/$(KIND_CLUSTER_NAME).cfg

.PHONY: kind-stop
kind-stop: 
	@kind delete cluster --name $(KIND_CLUSTER_NAME) || \
		echo "kind cluster is not running"

.PHONY: kind-start
kind-start: 
	@kind get clusters | grep $(KIND_CLUSTER_NAME) || \
		kind create cluster --name $(KIND_CLUSTER_NAME) --kubeconfig $(KUBECONFIG_PATH) --config ./kind.yaml

.PHONY: kind-get-creds
kind-get-creds:
	@kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(KUBECONFIG_PATH); \
	export KUBECONFIG=$$KUBECONFIG:$(KUBECONFIG_PATH); \
		kubectl config view --flatten >| ~/.kube/config && chmod 600 ~/.kube/config; \
		kubectl config use-context kind-${KIND_CLUSTER_NAME}; \
		kubectl cluster-info

.PHONY: kind-reset
kind-reset: kind-stop kind-start