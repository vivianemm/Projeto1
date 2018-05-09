# Projeto1


Primeiro projeto da disciplina Tratamento de Dados Astronômicos de 2018.1
Pacote para redução padrão de dados fotométricos em python

==================================================================================================

Utilizando o pacote
__________________________________________________________________________________________________

--> Baixar ou clonar o pacote

--> Entrar em seu diretorio pelo terminal e utilizar o comando 
'python setup.py install' para instalar o pacote

--> Chamar as funções do pacote em um script python
Fornecendo, entre os parametros, o caminho do diretorio onde se encontram as imagens FITS a
serem utilizadas na reducao
Cada função retorna um array que deve ser utilizado em funções seguintes no processo de redução

ordem recomendada: 
master_bias
flat_b
normal_flat
master_flat
science_b
science_bf

Em cada etapa, as imagens geradas podem ser salvas em formato FITS, se especificado nos parâmetros de entrada,
assim como o nome do diretório de destino das mesmas.
Por default, salva apenas o masterbias e masterflat na pasta 'master' e as imagens de ciencia corrigidas
de bias e de flat na pasta 'science_bf', dentro do diretorio onde estão as imagens utilizadas no processo de 
redução 
(pastas não precisam existir)
(Não devem existir arquivos fits com o mesmo nome no diretório onde se deseja salvar as novas imagens)

--> Pode-se realizar os testes estatísticos de bias e flat para verificar se a redução ocorreu de forma correta:
test_bias
test_flat




