# Acadia-Hardware — top-level developer entry point.
#
# This repository ships hardware data (pin-map) and validation tools; there is
# no build. The Makefile exposes the fleet-standard `version` target (CONV-004)
# so the parent repo's `make versions` / `make release` cover all ten leaves.

.PHONY: version help

version: ## Print the project version (CONV-004)
	@echo "$$(cat VERSION)"

help: ## Show this help
	@printf '\n  \033[1m%s\033[0m\n' 'Acadia-Hardware'
	@printf '  Usage: make <target>\n'
	@printf '\n'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_.\/-]+:.*?## / { printf "    \033[36m%-24s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@printf '\n'