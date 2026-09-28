## Atacante humano

### Ataque básico
```bash
nmap -vv --reason -oA [nome_do_arquivo] [ALVO]
```

`-vv` serve para que o nmap fique verboso
`--reason` mostra o motivo exato de uma porta ser considerada aberta ou fechada
`-oA` salva os resultados em três formatos diferentes (Normal, Grepable e XML)

### Ataque moderado/agressivo
```bash
nmap -p 1-65535 -A -T4 --version-all --osscan-guess -vv --reason -oA [nome_do_arquivo] [ALVO]
```

`-p 1-65535` indica que o scan deve ocorrer da porta 1 até a porta 65535, ou seja, todas as portas
`-A` flag que habilita detecção de sistema operacional `-O`, detecção de versão de serviços (`-sV`), varredura de scripts padrão (`-sC`) e rastreamento de rota (`traceroute`).
`-T4` Torna a varredura mais rápida. O `-T4` é agressivo e recomendado para redes estáveis;

### Ataque agressivo + scripts
```bash
nmap -p 1-65535 -A -T5 --version-all --osscan-guess --script="vuln,discovery,intrusive" -vv --reason -oA [nome_do_arquivo] [ALVO]
```

## Agente LLM



---

> [!NOTE]
> Para a contextualização teórica deste ataque no benchmark CSE-CIC-IDS2018 e seu impacto nas features do modelo ALF-MoE, consulte:
> - [[Infiltration - NMAP Portscan]]
> - [[00 - Mapeamento de Ataques Kali Linux]]