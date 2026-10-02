# ==============================================================================
# Makefile Principal do Repositório ALF-MoE
# ==============================================================================

THESIS_DIR = UndergraduateThesis

.PHONY: all pdf full fast watch clean distclean help

all: pdf

pdf:
	@$(MAKE) -C $(THESIS_DIR) pdf

full:
	@$(MAKE) -C $(THESIS_DIR) full

fast:
	@$(MAKE) -C $(THESIS_DIR) fast

watch:
	@$(MAKE) -C $(THESIS_DIR) watch

clean:
	@$(MAKE) -C $(THESIS_DIR) clean

distclean:
	@$(MAKE) -C $(THESIS_DIR) distclean

help:
	@$(MAKE) -C $(THESIS_DIR) help
