REQUIRED_TOOLS_LIST += docker

DEFAULT_SHELL ?= /bin/zsh
IMAGE_REGISTRY_ORG ?= ghcr.io/jesse-gonzalez

.PHONY: docker-build
docker-build: #### Build Calm DSL Util Image locally with necessary tools to develop and manage Cloud-Native Apps (e.g., kubectl, argocd, git, helm, helmfile, etc.)
	@docker image ls --filter "reference=${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils" --format "{{.Repository}}:{{.ID}}" | xargs -I {} docker rmi -f {}
	@docker build -t ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils:latest .

.PHONY: docker-run
docker-run: ### Launch into Calm DSL development container. If image isn't available, build will auto-run
	[ -n "$$(docker image ls ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils -q)" ] || docker pull ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils:latest
	# this will exec you into the interactive container
	docker run --rm -it \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v `pwd`:/dsl-workspace \
		-w '/dsl-workspace' \
		-e ENVIRONMENT='${ENVIRONMENT}' \
		${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils /bin/sh -c "${DEFAULT_SHELL}"

.PHONY: docker-login
docker-login: #### Login to Github Private Registry
	@echo "$(GITHUB_PASS)" | docker login ghcr.io --username $(GITHUB_USER) --password-stdin

.PHONY: docker-push
docker-push: docker-login ## Tag and Push latest image and short sha version to desired image repo.
	[ -n "$$(docker image ls ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils -q)" ] || make docker-build
	@docker push ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils:latest
	@docker tag ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils:$(GIT_COMMIT_ID)
	@docker push ${IMAGE_REGISTRY_ORG}/cloud-native-calm-utils:$(GIT_COMMIT_ID)	