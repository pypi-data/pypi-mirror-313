# Todo

- se tiver dentro do rep, vai utilizar o .tko/track pra rastrear o que foi feito
- se estiver dentro da pasta problems, vai rastrear, estando no readme ou não
- orientação de criar os problemas locais com _ para não dar conflito, mas não precisa ser obrigatório
- vai ser carregado no play sob o grupo de Problemas Locais

- na conversão de modelos
- mover pasta remote para problems
- mover os .track dentro da pasta problems para .tko/track/label
- converter rep.json para rep.yaml

fiz open não gravando o settings
inverter a tabela de self grade para o não fiz ficar perto do 1
colocar track na pasta dele
colocar repositório por parametro no tester pro repositório salvar as configurações
utilizar modelo observer para desacoplar tantas funções

```bash
tko rep list

tko init [--file <file> | --url <url> | --remote <alias>] --dir <folder> --save <alias>


tko init
tko start <remote> 
(equivalente) 
tko init --remote fup --dir fup --save fup
tko open fup

tko save <folder> <alias>
tko load <alias>

tko rep init <folder> (cria o readme e o repository.json, history.csv e daily.json)
tko rep init <folder> --remote alias
tko rep init <folder> --file path
tko rep init <folder> --url url

tko rep check <folder>
```

- rep_index.md
- rep_log.csv
- rep.json

no rep.json, ter um campo daily que é um vetor e mostra o atual, em relação ao último dia registrado
sempre sobrescreve.

```txt
daily = [
    "25/04/1984" = [{"talcoisa", 10, 8}, {"outra_coisa", 8, 5}, ]
]

```

faz um laço atualizando os valores das chaves

- ele tenta baixar o draft de onde? .cache/draft.lang
- fazer modo arquivo que permita baixar local
- testar tendo os dois readme e mapi
- testar tendo readme e faltando mapi
- testar tendo mapi e faltando readme
- testar faltando os dois

- colocar log como default e deixar um comando para limpar logs
- colocar modo pasta ao invés de modo online
- colocar modo arquivo mais prático do que ter que adicionar repositório
- modelo de tabela e modelo de input output para fup, deixa só o mula com o tio
- remover o modo monocromático
- add modelo pra converter entre markdown table para testes e tio
- tempo label do lado to fixar label ao lado dos cases
- +- label ao lado do tab para habilitar e desabilitar
- +- no mesmo simbolo se possível

- corrigir o DiffBuilder para adicionar ou remover as bordas
- se colocar as bordas, adicionar automaticamente a borda da direita.
- ao invés de fazer o scrollbar do lado direito, fazer elem embaixo

- opção de mostrar quantos testes passaram no principal
- opção de rodar os testes no computador do aluno
- for each folder tko test folder --compact
- mover coruja dinamicamente ou cortar tarefas se passarem do máximo e não tiver o mouse over

## Feedback

- Como sua autonomia e compreensão das técnicas apresentadas na atividade.
- Autonomia: Uso de ajuda externa. (grupo, monitor, colega, copilot, chatgpt, internet, tutorial)
- Compreensão: Nível de compreensão do conteúdo em 4 níveis. (superficial, básico, funcional, profundo)
