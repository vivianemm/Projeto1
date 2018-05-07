import __init__

# definindo caminho do diretorio com os arquivos fits
data_path = '/Users/Viviane/Downloads/xo2b/xo2b/'   # ou '/home2/viviane15/Downloads/xo2b/'

# Ainda nao existem arquivos com os mesmos nomes das imagens fits a serem salvas durante a reducao nos diretorios onde
# serao salvas

# salva master_bias.fits em "/Users/Viviane/Downloads/xo2b/xo2b/master" e retorna matriz
master_bias = __init__.master_bias(data_path, 'bias')

# retorna array de flats corrigidos de bias, nao salva em fits
flat_b = __init__.flat_b(data_path, master_bias, 'flat')

# retorna array de flats corrigidos de bias e nrmalizados, nao salva em fits
normal_flat = __init__.normal_flat(data_path, flat_b)

# retorna matriz de master_flat e salva master_flat.fits em  "/Users/Viviane/Downloads/xo2b/xo2b/master"
master_flat = __init__.master_flat(data_path, normal_flat)

# retorna array de imagens de ciencia corrigidas de bias, nao salva fits
#science_b = science_b(data_path, 'xo2b',mb)

# retorna array de imagens de ciencia corrigidas de bias e flat para uso posterior e salva cada xo2b_bf_*.fits em
# "/Users/Viviane/Downloads/xo2b/xo2b/science_bf"
#science_bf = science_bf(data_path, science_b, master_flat, 'xo2b')
