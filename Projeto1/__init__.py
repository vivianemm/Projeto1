import glob
from astropy.io import fits
import numpy as np

data_path = caminho          #'/home2/viviane15/Downloads/xo2b/'  



def master_bias():
	imagens_bias = glob.glob(data_path+'bias*.fits')  #caminhos
	bias_fits=[]
	for i in imagens_bias:
		img = fits.getdata(i)
		bias_fits.append(img)
	
	bias_fits = np.array(bias_fits)
	master_bias = np.median(bias_fits)
	
	hdu = fits.PrimaryHDU()                #criando HDU
	hdu.data = master_bias
	
	hdu.header['master_bias'] = True
	hdu.header['comment'] = 'Masterbias obtido a partir da mediana de tantas imagens'
	hdu.writeto('master_bias.fits')
	
	
	
def masterFlat():
	imagens_flats = glob.glob(data_path+'flat*.fits')
	flats_fits=[]
	
	for i in imagens_flats:
		img = fits.getdata(i)
		flats_fits.append(img)
		
	bias_fits = np.array(flats_fits)
	master_flat = np.median(flats_fits)
	
	hdu = fits.PrimaryHDU()                #criando HDU
	hdu.data = master_flat
	
	hdu.header['masterflat'] = True
	hdu.header['comment'] = 'Masterflat obtido a partir da mediana de tantas imagens'
	hdu.writeto('master_flat.fits')
	
	

def science():
	science_files = glob.glob(data_path+'xo2b*.fits')
	science_fits = []
	
	for i in science_files:
		img = fits.getdata(i)
		science_files.append(img)
		
	
	
	
	
	
	
	
