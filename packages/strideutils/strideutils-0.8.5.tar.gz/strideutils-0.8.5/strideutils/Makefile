CONFIG_PATH=config.yaml
CONFIG_MAP=strideutils-config
K8S_NAMESPACE=stride-main
KUBECTL := $(shell which kubectl)

update-config:
	@echo "Updating Strideutils configmap"
	@echo "$(CONFIG_PATH)"
	@$(KUBECTL) delete configmap $(CONFIG_MAP) -n $(K8S_NAMESPACE) --ignore-not-found=true
	@$(KUBECTL) create configmap $(CONFIG_MAP) --from-file=$(CONFIG_PATH) -n $(K8S_NAMESPACE)
