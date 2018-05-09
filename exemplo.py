import Projeto1 as pj1
import time


# Medindo o tempo de execucao do script
# Horario inicial
start_time = time.time()

# instalar pacote Projeto1
# no terminal: python setup.py install

# definindo caminho do diretorio com os arquivos fits
# bias, flats e ciencia estão no mesmo diretorio
data_path = '/home2/viviane15/Downloads/xo2b/'


# Ainda nao existem arquivos com os mesmos nomes das imagens fits a serem salvas 
# durante a reducao nos diretorios onde serao salvas

# salva master_bias.fits em "/Users/Viviane/Downloads/xo2b/xo2b/master" e retorna matriz
master_bias = pj1.master_bias(data_path, 'bias')

# retorna array de flats corrigidos de bias, nao salva em fits
flat_b = pj1.flat_b(data_path, master_bias, 'flat')

# retorna array de flats corrigidos de bias e nrmalizados, nao salva em fits
normal_flat = pj1.normal_flat(data_path, flat_b)

# retorna matriz de master_flat e salva master_flat.fits em  "/Users/Viviane/Downloads/xo2b/xo2b/master"
# mesma pasta em que esta o master_bias
master_flat = pj1.master_flat(data_path, normal_flat)

# retorna array de imagens de ciencia corrigidas de bias, nao salva fits
science_b = pj1.science_b(data_path, 'xo2b',master_bias)

# retorna array de imagens de ciencia corrigidas de bias e flat para uso posterior e salva cada xo2b_bf_*.fits em
# "/Users/Viviane/Downloads/xo2b/xo2b/science_bf"
science_bf = pj1.science_bf(data_path, science_b, master_flat, 'xo2b')

# teste estatistico do masterbias
pj1.test_mbias(master_bias)

# teste estatistico dos flats normalizados
pj1.test_flat(normal_flat)

# teste das imagens de ciencia
science = pj1.find_files(data_path,'xo2b')
n = 0
diferenca = science_bf[0] -  science[0]
pj1.save_fits(data_path, diferenca, 'diferenca_' + str(n), 'teste estatistico da imagem de ciencia' + str(n), 'teste/')
# Abrir imagem fits e verificar diferenca entre as bordas e o centro


#Medindo o tempo de execucao do script
end_time = time.time()   # horario final
elapsed_time = end_time - start_time  # tempo decorrido em segundos
print(elapsed_time/60)

