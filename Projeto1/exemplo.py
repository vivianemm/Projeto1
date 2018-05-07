import Projeto1 as pj1

# instalar pacote Projeto1
# no terminal: python setup.py install

# definindo caminho do diretorio com os arquivos fits
# data_path = '/Users/Viviane/Downloads/xo2b/xo2b/'
data_path = '/home2/viviane15/Downloads/xo2b/'

# Ainda nao existem arquivos com os mesmos nomes das imagens fits a serem salvas durante a reducao nos diretorios onde
# serao salvas

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
#science_bf = pj1.science_bf(data_path, science_b, master_flat, 'xo2b')
