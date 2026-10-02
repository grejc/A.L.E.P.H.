# ==============================================================================
# Makefile para Compilação da Tese de Graduação (ALF-MoE)
# ==============================================================================

TARGET    = main
TEX       = pdflatex
BIB       = bibtex
LATEXMK   = latexmk
TEXFLAGS  = -interaction=nonstopmode -halt-on-error -file-line-error
MKFLAGS   = -interaction=nonstopmode -synctex=1

# Lista de dependências para detecção de alterações
TEX_SRCS  = $(wildcard *.tex) $(wildcard chapters/*.tex)
BIB_SRCS  = $(wildcard *.bib)
STY_SRCS  = $(wildcard *.sty)
FIG_SRCS  = $(wildcard figures/*.*) $(wildcard figures/*/*.*)

# Cores para o terminal
CYAN  = \033[0;36m
GREEN = \033[0;32m
YELLOW= \033[0;33m
RED   = \033[0;31m
RESET = \033[0m

.PHONY: all pdf full fast latexmk watch pvc clean distclean help

# Alvo padrão: compilação completa inteligente via latexmk
all: $(TARGET).pdf

pdf: $(TARGET).pdf

$(TARGET).pdf: $(TEX_SRCS) $(BIB_SRCS) $(STY_SRCS)
	@echo "$(CYAN)==> Compilando $(TARGET).pdf com latexmk...$(RESET)"
	$(LATEXMK) -pdf $(MKFLAGS) $(TARGET).tex
	@echo "$(GREEN)==> Compilação concluída com sucesso: $(TARGET).pdf$(RESET)"

# Compilação completa tradicional (4 passos manuais garantidos)
full:
	@echo "$(CYAN)==> [1/4] Primeira passagem: pdflatex...$(RESET)"
	$(TEX) $(TEXFLAGS) $(TARGET).tex
	@echo "$(CYAN)==> [2/4] Processando bibliografia: bibtex...$(RESET)"
	$(BIB) $(TARGET)
	@echo "$(CYAN)==> [3/4] Segunda passagem: pdflatex (resolvendo citações)...$(RESET)"
	$(TEX) $(TEXFLAGS) $(TARGET).tex
	@echo "$(CYAN)==> [4/4] Terceira passagem: pdflatex (resolvendo referências cruzadas)...$(RESET)"
	$(TEX) $(TEXFLAGS) $(TARGET).tex
	@echo "$(GREEN)==> Compilação completa finalizada com sucesso: $(TARGET).pdf$(RESET)"

# Compilação rápida (uma única passagem, útil para checagem de sintaxe)
fast:
	@echo "$(YELLOW)==> Compilação rápida (passagem única de pdflatex)...$(RESET)"
	$(TEX) $(TEXFLAGS) $(TARGET).tex
	@echo "$(GREEN)==> Passagem rápida concluída.$(RESET)"

# Compilação explícita via latexmk
latexmk:
	@echo "$(CYAN)==> Executando latexmk...$(RESET)"
	$(LATEXMK) -pdf $(MKFLAGS) $(TARGET).tex
	@echo "$(GREEN)==> latexmk finalizado.$(RESET)"

# Modo contínuo / vigia: recompila automaticamente ao salvar qualquer arquivo .tex/.bib
watch: pvc

pvc:
	@echo "$(YELLOW)==> Iniciando modo de monitoramento contínuo (pressione Ctrl+C para encerrar)...$(RESET)"
	$(LATEXMK) -pvc -pdf $(MKFLAGS) $(TARGET).tex

# Limpeza de arquivos auxiliares de compilação (preserva o PDF gerado)
clean:
	@echo "$(YELLOW)==> Removendo arquivos auxiliares de compilação...$(RESET)"
	@rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
	@rm -f *.fdb_latexmk *.fls *.synctex.gz *.brf *.idx *.ilg *.ind
	@rm -f *.nav *.snm *.vrb texput.log
	@rm -f chapters/*.aux
	@echo "$(GREEN)==> Limpeza concluída (PDF preservado).$(RESET)"

# Limpeza completa (remove auxiliares e o PDF gerado)
distclean: clean
	@echo "$(RED)==> Removendo $(TARGET).pdf...$(RESET)"
	@rm -f $(TARGET).pdf
	@echo "$(GREEN)==> Limpeza total finalizada.$(RESET)"

# Ajuda interativa com descrição de alvos
help:
	@echo "======================================================================"
	@echo "                  Makefile - Tese de Graduação (ALF-MoE)              "
	@echo "======================================================================"
	@echo "Comandos disponíveis:"
	@echo "  make              Compila o PDF de forma inteligente via latexmk (padrão)"
	@echo "  make pdf          Equivalente a 'make'"
	@echo "  make full         Executa o pipeline manual completo de 4 passos"
	@echo "                    (pdflatex -> bibtex -> pdflatex -> pdflatex)"
	@echo "  make fast         Executa uma única passagem rápida do pdflatex"
	@echo "  make watch        Modo contínuo: monitora arquivos e recompila ao salvar"
	@echo "  make clean        Remove arquivos temporários (.aux, .log, .bbl, etc.)"
	@echo "  make distclean    Remove arquivos temporários E o arquivo main.pdf"
	@echo "  make help         Exibe este menu de ajuda"
	@echo "======================================================================"
