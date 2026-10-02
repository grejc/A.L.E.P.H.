
Aparentemente, os fluxos de telemetria estão sendo classificados pelo modelo como 'Infiltration', ou seja, o modelo está classificando a telemetria como exfiltração de dados, o que não deixa de ser verdade segundo o artigo 

[Collecting Telemetry Data Privately](https://arxiv.org/abs/1712.01524)
[Bolin Ding](https://arxiv.org/search/cs?searchtype=author&query=Ding,+B), [Janardhan Kulkarni](https://arxiv.org/search/cs?searchtype=author&query=Kulkarni,+J), [Sergey Yekhanin](https://arxiv.org/search/cs?searchtype=author&query=Yekhanin,+S)

Mesmo com a telemetria de algumas aplicações desativadas, ainda estava ocorrendo coleta de telemetria, e todas estavam tomando um bloqueio de 5 minutos definido no pipeline de inferência. Mas ainda pode ser equívovo visto a performance mediocre que o modelo teve em classificar esse tipo de ataque;

Muito disso foi devido ao fato de que o ataque ocorreu em duas etapas:
1. **C2C**: Download Dropbox (HTTPS/443) → Exploit Adobe PDF → Backdoor Metasploit (C2 via HTTP/HTTPS/DNS)
2. **PortScan**: Metasploit ativo → Nmap IP Sweep → Full Port Scan → Enumeração de Serviços (SMB/RDP/RPC)

O CICFlowMeter extrai estatísticas de fluxos agregados, não é ruim, mas para esse modelo falha miseravelmente para certos vetores de ataques. Além de que, a janela para gerar os dados usou `active_timeout = 1800s` e `idle_timeout = 120s`, ou seja, seria necessário esperar no mínimo 120 segundos para que um fluxo fosse montado e a inferencia fosse realizada; Um nmap rodando no modo básico leva menos de 30 segundos para fazer um scan completo da máquina;

---
Após passar pelo treinamento com o CSE-CIC-IDS2018 corrigido; Re-executei o pipeline de defesa ativa. Até o momento enquanto trafego normalmente pela rede, a maioria esmagadora dos tráfegos foram identificado como benignos, salvo a exceção do IP usado para multicast *239.255.255.250*

---

Dá para meio que se dizer que na minha metodologia se incluí os passos:
- Inferir fluxos de rede em uma sessão com tráfego normal, completamente humano;
- Inferir fluxos de rede em uma sessão com tráfego normal + ataques humanos manuais
- Inferir fluxos de rede em uma sessão com tráfego normal + ataques humanos "scriptados"
- Inferir fluxos de rede em uma sessão com tráfego normal + ataques gerados por uma LLM supervisionada
- Inferir fluxos de rede em uma sessão com tráfego normal + ataques gerados por uma LLM não supervisionada (mas auditada)


---

Acabei de rodar o nmap básico e todos os fluxos gerados foram classificados como benignos.
Estou rodando o modo stealth no momento, ainda não concluiu, mas já  pode-se dizer que ele também não identificará, realmente, não identificou o ataque levou cerca de 10 minutos.  Comecei o semi-agressivo 22:01h e ele finalizou as 22:04h. Iniciei o agressivo às 22:28h e ele finalizou às 22:43h. Adicionei o IP _239.255.255.250_ na whitelist para ele não ficar sendo bloqueado.

Deixei a noite inteira rodando e pelos logs busquei as seguintes informações:
- _112398_ fluxos coletados
- _98941_ fluxos pertencem ao IP atacante
- _18_ classificados como ataque , sendo que:
	- _13_ classificados como **_Infiltration - NMAP Portscan_**
	- _5_ classificados como **_DoS_**

---
Novo dia

Para esse segundo teste vou informar _`--threshold 0.51`_ porque notei que no último teste só não foi bloqueado porque eu havia definido o threshold para 0.8, ou seja, só iria bloquear se a confiança do modelo atingisse 80%, e das 13 identificadas 11 eram acima de 51% de confiança;
Adicionei o IP _35.186.224.9_ que provavelmente é telemetria do Spotify;
E alterar o `active_timeout` de captura de _1800s_ para _240s_ (o dobro do `idle_timeout`)


Fiz a [[Reconhecimento#Metodologia]] iniciando às 14:48h
Iniciei o ataque às 14:51h
Ataque finalizado às  14:51h
Não está mais chegando pacotes do atacante
Iniciando ataque às 15:05h (estimativa de finalização 15:11h)
Ataque finalizado às 15:10h e 5 minutos aguardados 
Iniciando ataque às 15:17 
Ataque finalizado às 15:19
Iniciando ataque às 16:47:39
Ataque finalizado às 17:02:51

Acho que a flag `decode_tunnels` atrapalhou, eu vi que ele bloqueou o IP 192.168.3.1 que é o do modem, mas não sei dizer se é isso mesmo;
Mas antes de testar novamente, vou corrigir algumas coisas do código, treinar um novo modelo e reiniciar o computar porque eles já está sofrendo um pouco...
As coisas no código são, refatorar o InferencePipeline para que ele infira diretamente no plugin que extrai as features; e a troca da acurácia OvR

---

Acho que no fim das contas vou tentar subir o ambiente do MITRE Caldeira em um docker e coletar com isso mesmo...