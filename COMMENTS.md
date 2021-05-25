1-) Dockerfile funcionando corretamente com o gunicorn permitindo acesso externo
2-) Jenkinsfile criado para efetuar o deploy
3-) Próximo passo finalizar a configuração do cloudformation para o provisionamento dos hosts
4-) Adicionei uma rota de healthcheck no app para que o healthcheck no target group funcione corretamente
5-) Script simples de monitoramento feito para detectar se o status da aplicação

Melhorias que podem ser feitas:

Estabilidade da aplicação:
Configurar a aplicação para passar pelo Clouflare para rotear todo o tráfego e utilizar o serviço WAF que está incluído até mesmo no plano gratuíto, para tentar impedir que bots fiquem spammando comentários aleatórios antes mesmo da request chegar no ELB além da utilização do cache para que a aplicação fique mais rápida;
Implementar cache na própria aplicação para otimizar o tempo de resposta da aplicação utilizando por ex. o decorator @cache_maker da lib repoze.lru.

Monitoramento dos hosts:
Configurar um APM para monitorar a aplicação e identificar erros e possíveis rotas lentas do sistema. Ex.: Elastic APM e Metricbeat, ambos disponíveis de forma gratuíta na stack ELK;
Script de monitoramento que consulte diretamente na AWS por meio de API, quando um container estiver para cair ou não.(Um exemplo simples está desenvolvido no diretório de monitoramento).

Melhorias IaC e Cost Optimization:
Usar AWS-CDK no lugar do cloudformation devido a maior liberdade de personalização das configurações;
Diminuir o custo da infra utilizando um segundo autoscaling para iniciar um SpotFleet.
