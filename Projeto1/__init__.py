import glob
from astropy.io import fits
import numpy as np
from numba import jit

'''

git add --all
git commit -m 'comentario'
git push -u origin master

'''

	
##'/home2/viviane15/Downloads/xo2b/' 

data_path = '/home2/viviane15/Downloads/xo2b/'

@jit
def find_files(n):
	paths = np.sort(glob.glob(data_path + n))  
	fit_files=[]                                     
	for i in paths:                            
		img = fits.getdata(i)                         
		img = img.astype(np.float64)
		fit_files.append(img)
	
	fit_files = np.array(fit_files)
	return fit_files
	

@jit	
def save_fits(s, nome, comentario = False, pasta = ''):  #(s, comentario = False)
	
	hdu = fits.PrimaryHDU()
	outfile = data_path + pasta + nome +'.fits'
	hdu.data = s
	hdu.header['comment'] = comentario
	hdu.writeto(outfile)
	
	

def master_bias():
	
	bias_files = find_files('bias*.fits')
		
	master_bias = np.median(bias_files,axis=0)         #tirando a mediana
		
	save_fits(master_bias, 'master_bias', 'Masterbias obtido a partir da mediana')
	
	#return master_bias  #img
	print('feito')
	
master_bias()
	
def	flat_b():
	flat_files = find_files('flat*.fits')
	mb = master_bias()
	
	flats_b = []
	for i in flat_files:
		f_b = i - mb 
		flats_b.append(f_b)
		
	flats_b = np.array(flats_b)
		
	return flats_b  #lista de imgs
		
	
	
def normal_flat():
	fb = flat_b()
	
	norms = []
	for i in fb:   #???????????
		med = np.median(i)
		norm = i/med
		norms.append(norm)
		
	norms = np.array(norms)
	
	return norms  #lista de imgs
	


def master_Flat():
	n = normal_flat()  #???????
		
	master_flat = np.median(n, axis=0)
	
	save_fits(master_flat, 'master_flat', 'Masterflat obtido a partir da mediana')
	
	return master_flat  #img
	


def science_b():
	science_files = find_files('xo2b*.fits')
	mb = master_bias() #??????
	
	science_b = []
	for i in science_files:
		s_b = i - mb
		science_b.append(s_b)
		
	science_b = np.array(science_b)
	return science_b
	
	
	
def science_bf():
	
	science_bf =[]
	cont = 0	
	for i in science_b():
		s_bf = i/master_Flat()
		science_bf.append(s_bf)
		
		save_fits(i, 'xo2b_bf_'+ str(cont), 'imagem de ciencia bf', 'ciencia')  #????? n funciona
		cont+=1	
		
	science_bf = np.array(science_bf)
	
	return science_bf
	
	
		
		
		
	
		
	
	
	
	
	
	
	
