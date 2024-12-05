help:
	@echo "make preplab to push on V0"
	@echo "make r2lab to push on production"

############################## for deploying before packaging
# default is to mess with our preplab and let the production
# site do proper upgrades using pip3
deployment ?= preplab

ifeq "$(deployment)" "production"
    DEST=r2lab.inria.fr
else
    DEST=preplab.pl.sophia.inria.fr
endif

# installing in /tmp/sidecar-sync for testing
sync:
	rsync -av --relative $$(git ls-files) root@$(DEST):/tmp/sidecar-sync/
	@echo '===== once copied, do the following as root on $(DEST)'
	@echo 'export PYTHONPATH=/tmp/sidecar-sync'
	@echo 'python /tmp/sidecar-sync/sidecar-server.py'

r2lab:
	$(MAKE) sync deployment=production

preplab:
	$(MAKE) sync deployment=preplab

.PHONY: sync r2lab preplab
