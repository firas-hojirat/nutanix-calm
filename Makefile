.DEFAULT_GOAL := help
MAKEFLAGS += --no-builtin-rules --no-builtin-variables
.SUFFIXES:

ENVIRONMENT ?= kalm-main-12-4

## load common variables and anything environment specific that overrides
export ENV_GLOBAL_PATH 	 := $(CURDIR)/config/_common/.env
export ENV_OVERRIDE_PATH := $(CURDIR)/config/${ENVIRONMENT}/.env

## include modules from .mk folder, in order
MODULES := utils git docker kind karbon terraform packer calm
include $(patsubst %,.mk/%.mk,$(MODULES))

## validate that the cli tools are available if not running in docker container
REQUIRED_TOOLS_LIST :=

ifeq (,$(wildcard /.dockerenv))
CHECK_TOOLS := $(foreach tool,$(REQUIRED_TOOLS_LIST), $(if $(shell which $(tool)),some string,$(error "No $(tool) in PATH")))
endif

## import GPG keys for all environments in .local folder
GPG_IMPORT = $(shell find .local -name sops_gpg_key | egrep -i "common|${ENVIRONMENT}" | xargs -I {} gpg --quiet --import {} 2>/dev/null)

## import common/global and environment specific override variables
include $(ENV_GLOBAL_PATH)
-include $(ENV_OVERRIDE_PATH)

export

##########
## SCENARIOS/WORKFLOWS

init-bastion-host-svm set-bastion-host init-runbook-infra init-kalm-cluster init-helm-charts bootstrap-kalm-all bootstrap-reset-all: check-dsl-init

.PHONY: init-bastion-host-svm
init-bastion-host-svm: ### Initialize Karbon Admin Bastion Workstation. .i.e., make init-bastion-host-svm ENVIRONMENT=kalm-main-16-1
	@make create-dsl-bps launch-dsl-bps DSL_BP=bastion_host_svm ENVIRONMENT=${ENVIRONMENT};
	@make set-bastion-host ENVIRONMENT=${ENVIRONMENT};

.PHONY: set-bastion-host
set-bastion-host: #### Update Dynamic IP for Linux Bastion Endpoint. .i.e., make set-bastion-host ENVIRONMENT=kalm-main-16-1
	@export BASTION_HOST_SVM_IP=$(shell calm get apps -n bastion-host-svm -q -l 1 --filter=_state==running | xargs -I {} calm describe app {} -o json | jq '.status.resources.deployment_list[0].substrate_configuration.element_list[0].address' | tr -d '"'); \
		grep -i BASTION_HOST_SVM_IP $(ENV_OVERRIDE_PATH) && sed -i "s/BASTION_HOST_SVM_IP =.*/BASTION_HOST_SVM_IP = $$BASTION_HOST_SVM_IP/g" $(ENV_OVERRIDE_PATH) || echo -e "BASTION_HOST_SVM_IP = $$BASTION_HOST_SVM_IP" >> $(ENV_OVERRIDE_PATH);

.PHONY: init-runbook-infra
init-runbook-infra: ### Initialize Calm Shared Infra from Endpoint, Runbook and Supporting Blueprints perspective. .i.e., make init-runbook-infra ENVIRONMENT=kalm-main-16-1
	@make set-bastion-host ENVIRONMENT=${ENVIRONMENT};
	@make create-all-dsl-endpoints ENVIRONMENT=${ENVIRONMENT};
	@make create-all-dsl-runbooks ENVIRONMENT=${ENVIRONMENT};
	@make run-all-dsl-runbook-scenarios RUNBOOK=update_calm_categories ENVIRONMENT=${ENVIRONMENT};
	@make run-all-dsl-runbook-scenarios RUNBOOK=update_ad_dns ENVIRONMENT=${ENVIRONMENT};
	@make run-all-dsl-runbook-scenarios RUNBOOK=update_objects_bucket ENVIRONMENT=${ENVIRONMENT};

.PHONY: init-helm-charts
init-helm-charts: ### Intialize Helm Chart Marketplace. i.e., make init-helm-charts ENVIRONMENT=kalm-main-16-1
	@make create-all-helm-charts ENVIRONMENT=${ENVIRONMENT};

.PHONY: init-kalm-cluster
init-kalm-cluster: ### Initialize Karbon Cluster. i.e., make init-kalm-cluster ENVIRONMENT=kalm-main-16-1
	@make set-bastion-host ENVIRONMENT=${ENVIRONMENT};
	@make run-all-dsl-runbook-scenarios RUNBOOK=update_ad_dns ENVIRONMENT=${ENVIRONMENT};
	@make create-dsl-bps launch-dsl-bps DSL_BP=karbon_cluster_deployment ENVIRONMENT=${ENVIRONMENT};

.PHONY: bootstrap-kalm-all
bootstrap-kalm-all: ### Bootstrap Bastion Host, Shared Infra and Karbon Cluster. i.e., make bootstrap-kalm-all ENVIRONMENT=kalm-main-16-1
	@make init-dsl-config ENVIRONMENT=${ENVIRONMENT};
	@make init-bastion-host-svm ENVIRONMENT=${ENVIRONMENT};
	@make init-runbook-infra ENVIRONMENT=${ENVIRONMENT};
	@make init-kalm-cluster ENVIRONMENT=${ENVIRONMENT};
	@make create-all-helm-charts ENVIRONMENT=${ENVIRONMENT};
	@make publish-all-blueprints ENVIRONMENT=${ENVIRONMENT};
	@make download-karbon-creds ENVIRONMENT=${ENVIRONMENT};

.PHONY: bootstrap-reset-all
bootstrap-reset-all: ### WARNING: This WILL delete ALL existing apps, blueprints, runbooks, endpoints found in calm environment. i.e., make bootstrap-reset-all ENVIRONMENT=kalm-main-16-1
	@calm get apps --limit 50 -q --filter=_state==provisioning | grep -v "No application found" | xargs -I {} -t sh -c "calm stop app {} --watch 2>/dev/null";
	@calm get apps --limit 50 -q --filter=_state==deleting | grep -v "No application found" | xargs -I {} -t sh -c "calm stop app {} --watch 2>/dev/null";
	@calm get apps --limit 50 -q --filter=_state==error | grep -v "No application found" | xargs -I {} -t sh -c "calm delete app {}";
	@calm get apps --limit 50 -q --filter=_state==running | egrep -v "karbon|bastion" | grep -v "No application found" | xargs -I {} -t sh -c "calm delete app --soft {}";
	@calm get apps -q -n karbon --filter=_state==running | grep -v "No application found" | xargs -I {} -t sh -c "calm delete app {}";
	@calm get apps -q -n bastion --filter=_state==running | grep -v "No application found" | xargs -I {} -t sh -c "calm delete app {}";
	@calm get bps --limit 50 -q | grep -v "No blueprint found" | xargs -I {} -t sh -c "calm delete bp {}";
	@calm get runbooks -q | grep -v "No runbook found" | xargs -I {} -t sh -c "calm delete runbook {}";
	@calm get endpoints -q | grep -v "No endpoint found" | xargs -I {} -t sh -c "calm delete endpoint {}";
