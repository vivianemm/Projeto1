import glob
from astropy.io import fits
import numpy as np
from numba import jit
import pathlib

'''

git add --all
git commit -m 'comentario'
git push -u origin master

'''

#rodar dentro do diretorio da imagens
#chamar science_bf ????

data_path = '/home2/viviane15/Downloads/xo2b/'

@jit
def find_files(data_path, prefix):
	paths = np.sort(glob.glob(data_path + prefix + '*fits'))
	fit_files=[]
	for i in paths:
		img = fits.getdata(i)
		img = img.astype(np.float64)
		fit_files.append(img)

	fit_files = np.array(fit_files)
	return fit_files


@jit
def save_fits(s, nome, comentario = False, pasta = ''):  #pasta tem que exitir, n pode existir arquivo com mesmo nome #caminho???

	hdu = fits.PrimaryHDU()

	if pasta == '':
		outfile = nome +'.fits'
	else:
		pathlib.Path(data_path + pasta).mkdir(exist_ok=True)  #substitui pasta existente

	hdu.data = s
	hdu.header['comment'] = comentario
	hdu.writeto(outfile)


@jit
def master_bias(data_path, prefix_bias,save = True, comment_mb ='', pasta_mb = 'master'):

	bias_files = find_files(data_path, prefix_bias)

	master_bias = np.median(bias_files,axis=0)

	if save:
		save_fits(master_bias, 'master_bias', comment_mb, pasta_mb)

	return master_bias  #img


@jit
def	flat_b(data_path, prefix_flat, prefix_bias):
	flat_files = find_files(prefix_flat)
	mb = master_bias(data_path, prefix_bias, False)

	flats_b = []
	for i in flat_files:
		f_b = i - mb
		flats_b.append(f_b)

	flats_b = np.array(flats_b)

	return flats_b  #lista de imgs


@jit
def normal_flat(data_path, prefix_flat, prefix_bias):
	fb = flat_b(data_path, prefix_flat, prefix_bias)

	norms = []
	for i in fb:
		med = np.median(i)
		norm = i/med
		norms.append(norm)

	norms = np.array(norms)

	return norms  #lista de imgs


@jit
def master_Flat(data_path, prefix_flat, prefix_bias, comment_mf = '', pasta_mf = 'master'):
	n = normal_flat(data_path, prefix_flat, prefix_bias)

	master_flat = np.median(n, axis=0)

	save_fits(master_flat, 'master_flat', comment_mf, pasta_mf) #??? substitui pasta?

	return master_flat  #img


@jit
def science_b(data_path, prefix_science, prefix_bias):
	'''
	exemplo
	x = 'xo2b'
	'''
	science_files = find_files(data_path, prefix_science)
	mb = master_bias(data_path, prefix_bias)

	science_b = []
	for i in science_files:
		s_b = i - mb
		science_b.append(s_b)

	science_b = np.array(science_b)
	return science_b


@jit
def science_bf(data_path, prefix_bias, prefix_flat, prefix_science, prefix_final, pasta_mb, pasta_mf, pasta_ciencia = 'ciencia'):

	science_bf =[]
	cont = 0
	science_bias = science_b(prefix_science, prefix_bias)
	mf = master_FLat(prefix_flat, prefix_bias)
	for i in science_b:
		s_bf = i/mf
		science_bf.append(s_bf)

		save_fits(i, prefix_science + str(cont), 'imagem de ciencia bf', pasta_ciencia)  #????? n funciona - acho q nao
		cont+=1

	science_bf = np.array(science_bf)

	return science_bf
