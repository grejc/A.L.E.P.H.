
## **Para o ambiente WEB:**

Foi utilizada uma aplicação DVWA (Damn Vulnerable Web Application) que possui vulnerabilidades categorizadas e que, podem ser fácilmente exploradas. Ela é utilizada por profissionais de cybersegurança para testarem suas skills em um ambiente seguro, controlado e principalmente LEGAL.

Para iniciar o ambiente é necessário ter o docker instalado. Rodando os seguintes comandos:
- `docker pull vulnerables/web-dvwa` : baixará a imagem
- `docker run --rm -it -p 8080:80 vulnerables/web-dvwa`: rodará o serviço mapeando a porta 80 do docker para a porta 8080 da sua própria máquina;
	- `--rm` : remove o container quando ele for parado
	- `-it`: fornece um terminal iterativo (util para ver os logs do container)

Acessar o DVWA:
	`http://localhost:8080`

Efetuar o login (credenciais padrões):
	- **Username**: `admin`
	- **Password**: `password`

![[DVWA_1.png]]

Após efetuar o login é preciso criar/resetar a base de dados para que o DVWA crie as tabelas necessárias e as preencha com dados de exemplo;

![[DVWA_2.png]]

![[DVWA_3.png]]

Uma vez completo o DVWA irá recarregar a página, basta logar novamente com credenciais padrões;

![[DVWA_4.png]]

Agora o DVWA está pronto!

### Função

Esse ambiente será utilizado para testar como o modelo se comporta diante de:
- [[Web Attack - Brute Force|Brute Force Web]]
- [[Web Attack - XSS|Web Attack - XSS]] (DOM, Reflected, Stored)
- Negação de Serviço HTTP:
  - [[DoS - Hulk]]
  - [[DoS - GoldenEye]]
  - [[DoS - Slowloris]]
  - [[DDoS - HOIC]]
  - [[DDoS - LOIC HTTP]]
- [[Web Attack - SQL Injection|SQL Injection]]

Para a matriz completa de ataques mapeados a partir do CSE-CIC-IDS2018, consulte [[00 - Mapeamento de Ataques Kali Linux]].