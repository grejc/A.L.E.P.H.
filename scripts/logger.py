#!/usr/bin/env python3
"""
Módulo de Auditoria e Registro para Agentes Autônomos (ALF-MoE).

Este módulo implementa o protocolo estrito de auditoria forense para agentes
e subagentes de teste adversarial, persistindo os registros em formato JSON Lines (.jsonl).

Pode ser invocado via linha de comando (CLI) ou importado diretamente em scripts Python.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Diretório raiz do projeto e caminhos padrão
DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_PATH = DEFAULT_REPO_ROOT / "logs" / "audit_agents.jsonl"
DEFAULT_STATUS = "LOGGED"
MAX_AGENT_WORDS = 3
MAX_REASON_WORDS = 25


def get_iso_timestamp() -> str:
    """Gera timestamp no formato ISO-8601 UTC com milissegundos e sufixo 'Z'."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def resolve_log_path(log_path: Optional[Union[str, Path]] = None) -> Path:
    """Resolve o caminho absoluto para o arquivo de log de auditoria."""
    if log_path:
        return Path(log_path).resolve()

    env_path = os.environ.get("AGENT_AUDIT_LOG_FILE")
    if env_path:
        return Path(env_path).resolve()

    return DEFAULT_LOG_PATH


def count_agent_words(agent: str) -> int:
    """
    Calcula a quantidade de palavras no nome do agente.
    Suporta divisão por espaços em branco ou decomposição de nomes em PascalCase/CamelCase.
    """
    clean_name = agent.strip()
    if not clean_name:
        return 0

    tokens = clean_name.split()
    if len(tokens) > 1:
        return len(tokens)

    # Identificador único (ex: PortScanScout, WebAuthAuditor, SqlInjectionProbe)
    subwords = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z][a-z0-9]|\b)", clean_name)
    return len(subwords) if subwords else 1


def count_reason_words(reason: str) -> int:
    """Calcula a quantidade de palavras na justificativa técnica."""
    clean_reason = reason.strip()
    if not clean_reason:
        return 0
    return len(clean_reason.split())


def validate_agent_name(agent: str, max_words: int = MAX_AGENT_WORDS, strict: bool = True) -> int:
    """Valida o formato e limite de palavras do nome do agente."""
    if not isinstance(agent, str) or not agent.strip():
        raise ValueError("O identificador do agente ('agent') não pode ser vazio.")

    words_count = count_agent_words(agent)
    if words_count > max_words:
        msg = (
            f"Nome do agente '{agent}' excede o limite máximo de {max_words} palavras "
            f"(detectadas: {words_count} palavras)."
        )
        if strict:
            raise ValueError(msg)
        sys.stderr.write(f"[AVISO AUDITORIA] {msg}\n")

    return words_count


def validate_reason(reason: str, max_words: int = MAX_REASON_WORDS, strict: bool = True) -> int:
    """Valida o comprimento da justificativa técnica da ação."""
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("O motivo da execução ('reason') não pode ser vazio.")

    words_count = count_reason_words(reason)
    if words_count > max_words:
        msg = (
            f"O motivo da execução excede o limite estrito de {max_words} palavras "
            f"(detectadas: {words_count} palavras). Texto: '{reason}'"
        )
        if strict:
            raise ValueError(msg)
        sys.stderr.write(f"[AVISO AUDITORIA] {msg}\n")

    return words_count


@dataclass
class AuditEvent:
    """Estrutura formal de um evento de auditoria de agente."""

    timestamp: str
    agent: str
    last_command: str
    next_command: str
    reason: str
    status: str = DEFAULT_STATUS

    def to_dict(self) -> Dict[str, Any]:
        """Converte o evento em dicionário ordenado conforme a especificação."""
        return {
            "timestamp": self.timestamp,
            "agent": self.agent,
            "last_command": self.last_command,
            "next_command": self.next_command,
            "reason": self.reason,
            "status": self.status,
        }

    def to_json(self) -> str:
        """Serializa o evento para JSON em linha única."""
        return json.dumps(self.to_dict(), ensure_ascii=False)


def log_action(
    agent: str,
    last_command: str,
    next_command: str,
    reason: str,
    status: str = DEFAULT_STATUS,
    log_file: Optional[Union[str, Path]] = None,
    strict: bool = True,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Registra uma ação de auditoria no arquivo .jsonl.

    Parâmetros:
        agent: Nome do agente ou subagente (máx. 3 palavras).
        last_command: Último comando executado (ou 'START' se inicial).
        next_command: Próximo comando a ser executado no terminal.
        reason: Justificativa técnica concisa (limite de até 25 palavras).
        status: Status do registro (padrão: 'LOGGED').
        log_file: Caminho customizado para o arquivo de log.
        strict: Se True, lança erro ao violar limites de palavras.
        timestamp: Timestamp ISO customizado (se omitido, gera o horário UTC atual).

    Retorna:
        Dicionário com os dados registrados.
    """
    if last_command is None or not str(last_command).strip():
        raise ValueError("O campo 'last_command' não pode ser vazio. Use 'START' para a primeira ação.")
    if next_command is None or not str(next_command).strip():
        raise ValueError("O campo 'next_command' não pode ser vazio.")

    validate_agent_name(agent, max_words=MAX_AGENT_WORDS, strict=strict)
    validate_reason(reason, max_words=MAX_REASON_WORDS, strict=strict)

    event_time = timestamp or get_iso_timestamp()
    event = AuditEvent(
        timestamp=event_time,
        agent=agent.strip(),
        last_command=str(last_command).strip(),
        next_command=str(next_command).strip(),
        reason=reason.strip(),
        status=status.strip() if status else DEFAULT_STATUS,
    )

    target_path = resolve_log_path(log_file)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    with target_path.open("a", encoding="utf-8") as f:
        f.write(event.to_json() + "\n")

    return event.to_dict()


def read_audit_log(
    log_file: Optional[Union[str, Path]] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Lê registros do arquivo de log de auditoria."""
    target_path = resolve_log_path(log_file)
    if not target_path.exists():
        return []

    records: List[Dict[str, Any]] = []
    with target_path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError as err:
                sys.stderr.write(f"[ERRO CORRUPÇÃO] Linha {line_num} inválida: {err}\n")

    if limit is not None and limit > 0:
        return records[-limit:]
    return records


def verify_audit_log(log_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Verifica a integridade e conformidade da trilha de auditoria (Fase 5).

    Verifica se o arquivo existe, se todas as linhas são JSON válidos,
    se contêm os campos obrigatórios e se respeitam as restrições operacionais.
    """
    target_path = resolve_log_path(log_file)
    result: Dict[str, Any] = {
        "file": str(target_path),
        "exists": target_path.exists(),
        "total_records": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "agents": {},
        "errors": [],
        "is_valid": False,
    }

    if not target_path.exists():
        result["errors"].append("Arquivo de auditoria não encontrado.")
        return result

    required_fields = ["timestamp", "agent", "last_command", "next_command", "reason", "status"]

    with target_path.open("r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue

            result["total_records"] += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as err:
                result["invalid_records"] += 1
                result["errors"].append(f"Linha {line_num}: JSON inválido ({err}).")
                continue

            # Validação dos campos obrigatórios
            missing = [k for k in required_fields if k not in entry]
            if missing:
                result["invalid_records"] += 1
                result["errors"].append(f"Linha {line_num}: Campos ausentes: {missing}.")
                continue

            # Validação de limites
            agent_name = str(entry.get("agent", ""))
            reason_text = str(entry.get("reason", ""))
            agent_words = count_agent_words(agent_name)
            reason_words = count_reason_words(reason_text)

            line_errors = []
            if agent_words > MAX_AGENT_WORDS:
                line_errors.append(f"Agente com {agent_words} palavras (> {MAX_AGENT_WORDS})")
            if reason_words > MAX_REASON_WORDS:
                line_errors.append(f"Motivo com {reason_words} palavras (> {MAX_REASON_WORDS})")

            if line_errors:
                result["invalid_records"] += 1
                result["errors"].append(f"Linha {line_num}: {'; '.join(line_errors)}.")
            else:
                result["valid_records"] += 1

            result["agents"][agent_name] = result["agents"].get(agent_name, 0) + 1

    result["is_valid"] = (result["invalid_records"] == 0 and result["total_records"] > 0)
    return result


class AgentLogger:
    """
    Interface orientada a objetos para o logger de auditoria de agentes.
    
    Permite gerenciar a transição de comandos consecutivos automaticamente.
    """

    def __init__(
        self,
        agent: Optional[str] = None,
        log_file: Optional[Union[str, Path]] = None,
        strict: bool = True,
    ) -> None:
        self.agent = agent
        self.log_file = resolve_log_path(log_file)
        self.strict = strict
        self._last_command: Optional[str] = None

    def log(
        self,
        next_command: str,
        reason: str,
        last_command: Optional[str] = None,
        agent: Optional[str] = None,
        status: str = DEFAULT_STATUS,
    ) -> Dict[str, Any]:
        """
        Registra uma ação. Se last_command não for informado, usa o último
        next_command registrado pela instância (ou 'START' se primeira chamada).
        """
        active_agent = agent or self.agent
        if not active_agent:
            raise ValueError("O nome do agente deve ser fornecido na instância ou na chamada log().")

        active_last = last_command or self._last_command or "START"

        logged = log_action(
            agent=active_agent,
            last_command=active_last,
            next_command=next_command,
            reason=reason,
            status=status,
            log_file=self.log_file,
            strict=self.strict,
        )

        self._last_command = next_command
        return logged

    def verify(self) -> Dict[str, Any]:
        """Verifica a integridade do arquivo de log configurado."""
        return verify_audit_log(self.log_file)

    def tail(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera os últimos registros."""
        return read_audit_log(self.log_file, limit=limit)


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Protocolo de Auditoria e Registro para Agentes Autônomos (ALF-MoE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Comando a ser executado")

    # Subcomando: log
    log_parser = subparsers.add_parser("log", help="Registrar uma ação de agente")
    log_parser.add_argument("--agent", required=True, help="Identificador do agente (máximo 3 palavras)")
    log_parser.add_argument("--last", required=True, dest="last_command", help="Último comando executado ou 'START'")
    log_parser.add_argument("--next", required=True, dest="next_command", help="Próximo comando a ser executado")
    log_parser.add_argument("--reason", required=True, help="Justificativa técnica (limite de até 25 palavras)")
    log_parser.add_argument("--status", default=DEFAULT_STATUS, help="Status da ação (padrão: LOGGED)")
    log_parser.add_argument("--logfile", default=None, help="Caminho do arquivo de log (padrão: logs/audit_agents.jsonl)")
    log_parser.add_argument(
        "--no-strict",
        action="store_true",
        help="Desativa validação estrita de contagem de palavras (emite apenas avisos)",
    )

    # Subcomando: verify
    verify_parser = subparsers.add_parser("verify", help="Verificar integridade da trilha de auditoria")
    verify_parser.add_argument("--logfile", default=None, help="Caminho do arquivo de log a ser verificado")

    # Subcomando: show
    show_parser = subparsers.add_parser("show", help="Exibir registros recentes de auditoria")
    show_parser.add_argument("--limit", type=int, default=10, help="Quantidade de registros a exibir (padrão: 10)")
    show_parser.add_argument("--logfile", default=None, help="Caminho do arquivo de log")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Ponto de entrada para execução via linha de comando."""
    args_list = argv if argv is not None else sys.argv[1:]

    # Compatibilidade: se invocado sem subcomando mas com opções de log (--agent, etc.)
    known_commands = {"log", "verify", "show", "-h", "--help"}
    if args_list and args_list[0] not in known_commands:
        if any(arg.startswith("--agent") for arg in args_list):
            args_list = ["log"] + args_list

    parser = _build_cli_parser()

    if not args_list:
        parser.print_help()
        return 0

    args = parser.parse_args(args_list)

    if args.subcommand == "log":
        try:
            entry = log_action(
                agent=args.agent,
                last_command=args.last_command,
                next_command=args.next_command,
                reason=args.reason,
                status=args.status,
                log_file=args.logfile,
                strict=not args.no_strict,
            )
            # Imprime o JSON do registro realizado
            print(json.dumps(entry, ensure_ascii=False))
            return 0
        except Exception as exc:
            sys.stderr.write(f"Erro ao registrar auditoria: {exc}\n")
            return 1

    elif args.subcommand == "verify":
        report = verify_audit_log(args.logfile)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("is_valid") else 1

    elif args.subcommand == "show":
        records = read_audit_log(args.logfile, limit=args.limit)
        for rec in records:
            print(json.dumps(rec, ensure_ascii=False))
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
