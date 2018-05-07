
'''
Pacote Reducao Fotometria


______________
Pacote para reducao de dados fotometricos 
Faz a correcao de bias e flat das imagens de ciencia

funciona com imagens de bias, flat e ciencia em formato fits
Imagens finais e geradas durante o processo de reducao podem ser salvas em formato fits:
masterbias, flats reduzidos de bias, flats reduzidos de bias e normalizados, masterflat, ciencia reduzida de bias,
ciencia reduzida de bias e flat

________
funcoes:
find_files
save_fits
master_bias
flat_b
normal_flat
master_flat
science_b
science_bf


git add --all
git commit -m 'comentario'
git push -u origin master

'''

import glob
from astropy.io import fits
import numpy as np
from numba import jit
from pathlib import Path
import time
import sys
import os

def update_progress(progress):
    """
    Progress Bar to visualize the status of a procedure
    ___
    INPUT:
    progress: percent of the data

    ___
    Example:
    print ""
    print "progress : 0->1"
    for i in range(100):
        time.sleep(0.1)
        update_progress(i/100.0)
    """
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


@jit
def find_files(data_path, prefix):
	'''
	Cria array com matrizes a partir de todos os arquivos fits que possuem o prefixo dado como parametro e presentes
	no caminho indicado

	:param data_path: str - caminho do diretorio onde estao os arquivos desejados em formato fits
	:param prefix: str - prefixo comum aos arquivos de interesse

	________
	:return: array com matrizes das imagens fits no caminho dado, com o prefixo especificado

	________
	exemplo:
	find_files('/home2/viviane15/Downloads/xo2b/', 'bias')
	'''
	paths = np.sort(glob.glob(data_path +  prefix + '*fits'))
	fit_files=[]

	cont = 1
	n = float(len(paths))
	print("\nProgress find_files {0} : 0->1".format(prefix))
	for i in paths:
		img = fits.getdata(i)
		img = img.astype(np.float64)
		fit_files.append(img)

		update_progress(cont / n)
		cont += 1

	fit_files = np.array(fit_files)
	return fit_files


@jit
def save_fits(data_path, s, nome, comment = '', folder = ''):
	'''
	Salva matriz em arquivo de formato fits no caminho indicado, podendo criar novo diretorio se especificado.
	Nao pode ser salvo se ja existir arquivo com mesmo nome no diretorio, apenas retornando mensagem informando se for
	o caso

	:param data_path: str - caminho do diretorio onde sera salvo o arquivo fit
	:param s:
	:param nome: str - nome que sera dado ao arquivo (sem extensao .fits)
	:param comment: str - comentario que pode ser adicionado ao header da imagem fits se especificado, default =''
	:param pasta: str - nome do novo diretorio (terminando com /) que pode ser criado para destino do arquivo
	se especificado, default = ''

	________
	:return: none

	________
	exemplo:
	save_fits('/home2/viviane15/Downloads/xo2b/', master_bias, 'master_bias', 'imagem de master bias obtida a
	partir da mediana', 'master/')
	'''

	outfile = data_path + folder + nome + '.fits'
	file = Path(outfile)
	if not file.is_file():

		hdu = fits.PrimaryHDU()

		if folder != '':
			Path(data_path + folder).mkdir(exist_ok=True)  #substitui pasta existente

		hdu.data = s
		hdu.header['comment'] = comment
		hdu.writeto(outfile)

	else:
		print('\nArquivo {0} ja existe\n'.format(str(nome)))



@jit
def master_bias(data_path, prefix_bias = 'bias', save = True, folder = '/master/'):
	'''
	Gera uma matriz de master_bias atraves da mediana das matrizes de bias, podendo salvar em arquivo fits

	:param data_path: str - caminho do diretorio onde estao os arquivos de bias em formato fit
	:param prefix_bias: str - prefixo do nome dos arquivos de bias, default: 'bias'
	:param save: bool - chama funcao save para salvar o master bias em um arquivo fits, default: True

	________
	:return: matriz do master bias
	'''

	bias_files = find_files(data_path, prefix_bias)

	master_bias = np.median(bias_files,axis=0)  # obtendo a matriz master_bias pela mediana das matrizes de bias

	if save:
		n = len(bias_files)
		comment_mb = 'masterbias obtido a partir da mediana de {0} imagens bias'.format(str(n))
		save_fits(data_path, master_bias, 'master_bias', comment_mb, folder)

	return master_bias


@jit
def flat_b(data_path, mb, prefix_flat = 'flat', save = False, folder = 'flats_b/'):
	'''
	Cria array com matrizes dos flats e faz a reducao de bias, atraves da subtracao da matriz de master_bias
	de cada matriz de flat

	:param data_path: str - caminho do diretorio onde estao os arquivos de flat em formato fit
	:param prefix_flat: str - prefixo do nome dos arquivos de flat, default: 'flat'
	:param mb: matriz de master bias

	________
	:return: array com matrizes de flat reduzidas de bias
	'''
	flat_files = find_files(data_path, prefix_flat) # array com matrizes de flat

	n = float(len(flat_files))
	cont = 1

	# inicializando lista para receber matrizes de flat corrigidas de bias
	flats_b = []
	print("\nProgress flats_b : 0->1")
	# laco para subtracao da matriz de masterbias de cada matriz de flat
	for i in flat_files:
		f_b = i - mb
		flats_b.append(f_b)

		if save:
			# comentario adicionado ao header de cada arquivo fits de flats reduzidos de bias
			comment = 'Flat reduzido de bias'
			save_fits(data_path, f_b, 'flat_b_' + str(cont), comment, folder)  # ??? substitui pasta?

		update_progress(cont / n)
		cont+=1

	# convertendo lista em array
	flats_b = np.array(flats_b)

	return flats_b  #array de flats corrigidos de bias


@jit
def normal_flat(data_path, fb, save = False, folder = 'normal_flats/'):
	'''
	Cria array de flats normalizados a partir de array de flats ja reduzidos de bias, dividindo cada um pela sua mediana

	:param fb: array com matrizes de flat reduzidas de bias

	________
	:return: array de matrizes de flat reduzidas de bias e normalizadas
	'''


	n = float(len(fb))

	# inicializando lista para receber as matrizes de flat apos normalizacao
	norms = []
	cont = 1
	print("\nProgress normal_flat : 0->1")

	# laco para normalizacao das matrizes de flat, atraves da divisao de cada um pela sua mediana
	for i in fb:
		med = np.median(i)
		norm = i/med
		norms.append(norm)

		if save:
			# comentario adicionado ao header de cada arquivo fits de flats normalizados
			comment = 'Flat reduzido de bias e normalizado'
			save_fits(data_path, norm, 'normal_flat_' + str(cont), comment, folder)  # ??? substitui pasta?


		update_progress(cont / n)
		cont += 1

	# convertendo lista em array
	norms = np.array(norms)

	return norms # array de flats corrigidos de bias e normalizados



@jit
def master_flat(data_path, norms, save = True, folder = 'master/'):
	'''
	Gera master flat atraves da mediana de array de flats reduzidos de bias e normalizados, podendo salvar em formato fits

	:param norms: array - array com imagens de flats reduzidos de bias e normalizados

	________
	:return: array - imagem do master flat obtido pela mediana
	'''

	# obtendo a matriz master_flat pela mediana das matrizes de flat corrigidas de bias e normalizadas
	master_flat = np.median(norms, axis=0)

	if save:
		n = len(norms)
		comment = 'Masterflat obtido a partir da mediana de {0} imagens de flat apos a reducao de bias e normalizacao'.format(str(n))

		save_fits(data_path, master_flat, 'master_flat', comment, folder)

	return master_flat


@jit
def science_b(data_path, prefix_science, mb, save = False, folder = 'science_B/'):
	'''
	Cria array com matrizes de ciencia retorna array com suas matrizes reduzidas de bias

	:param data_path: Type: str - caminho do diretorio onde estao os arquivos de ciencia em formato fit
	:param prefix_science: Type: str - prefixo dos arquivos de ciencia
	:param mb: array - matriz de master_bias

	________
	:return: array - array de matrizes de ciencia reduzidas de bias
	'''

	# array com matrizes de ciencia
	science_files = find_files(data_path, prefix_science)

	n = float(len(science_files))
	cont = 1

	# inicializando lista para receber matrizes de ciencia apos a correcao de bias
	science_b = []
	print("\nProgress science_b : 0->1")
	# laco para correcao de bias da ciencia, subtraindo a matriz de master bias de cada imagem de ciencia
	for i in science_files:
		s_b = i - mb
		science_b.append(s_b)

		if save:
			comment = 'imagem de ciencia reduzida de bias'
			save_fits(data_path, s_b, prefix_science + '_b_' + str(cont), comment, folder)

		update_progress(cont / n)
		cont += 1

	# convertendo a lista em array
	science_b = np.array(science_b)
	return science_b



@jit
def science_bf(data_path, science_bias, master_flat, prefix_science, save = True, folder = 'science_bf/'):
	'''


	:param science_bias: array - array de matrizes de ciencia ja reduzidas de bias

	:param master_flat: array - matriz de master flat

	:param pasta_ciencia: str - nome do novo diretorio onde serao salvas as imagens de ciencia reduzidas de bias e flat
	em formato fits, default: 'ciencia_bf/'

	________
	:return: array - array de matrizes das imagens de ciencia reduzidas de bias e flat
	'''

	n = float(len(science_bias))

	# inicializando lista para receber matrizes de ciencia apos a correcao de flat
	science_bf =[]
	cont = 1
	comment = 'Imagem de ciencia reduzida de flat e bias'
	print("\nProgress science_bf : 0->1")
	# laco para correcao de flat da ciencia, dividindo cada imagem de ciencia pela matriz de master flat
	for i in science_bias:
		science_bf = i/master_flat
		science_bf.append(science_bf)

		if save:
			save_fits(data_path, science_bf, prefix_science + '_bf_' + str(cont), comment, folder)

		update_progress(cont / n)
		cont += 1

	# convertendo a lista em array
	science_bf = np.array(science_bf)

	return science_bf  # array com imagens de ciencia corrigidas de bias e flat

#data_path = '/Users/Viviane/Downloads/xo2b/xo2b/'
#mb = master_bias(data_path, 'bias')
#fb = flat_b(data_path, mb, 'flat')
#fbn = normal_flat(data_path, fb)
#masterf = master_flat(data_path, fbn)
#science_b(data_path, 'xo2b',mb)

