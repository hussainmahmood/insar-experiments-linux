import shutil
import os
import time
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

def readProduct(productFilename, *args, **kwargs):
	print(f"Reading... {productFilename}")
	product = ProductIO.readProduct(productFilename)
	if kwargs.get('width', False):
		print(f"Width: {product.getSceneRasterWidth()} px")
	if kwargs.get('height', False):
		print(f"Height: {product.getSceneRasterHeight()} px")
	if kwargs.get('bands', False):
		print(f"Bands: {', '.join(product.getBandNames())}")

	print(f"Done\r\nProduct name: {product.getName()}")
	return product

def SnaphuExport(outputPath, product, suffix="Wrp", *args, **kwargs):
	print(f"Exporting {product.getName()}...")
	filename = f"{product.getName()}_{suffix}"
	targetFilename = f"{outputPath}/{filename}"
	parameters = HashMap()
	parameters.put('initMethod', 'MCF')
	parameters.put('colOverlap', '400')
	parameters.put('rowOverlap', '400')
	parameters.put('numberOfTileCols', '20')
	parameters.put('numberOfTileRows', '20')
	parameters.put('statCostMode', 'DEFO')
	parameters.put('targetFolder', 'snaphu')
	parameters.put('tileCostThreshold', '500')
	parameters.put('numberOfProcessors', '4')
	try:
		snaphu_export = GPF.createProduct('SnaphuExport', parameters, product)
		ProductIO.writeProduct(snaphu_export, targetFilename, "Snaphu")
		del snaphu_export
	except Exception as e:
		raise Exception(f"Problem completing operation\r\n{e}")
	else:
		print(f"Done\r\nProduct saved at: {targetFilename}")

	return targetFilename

def main():
	for subset_file in [f for f in os.listdir('subsets') if f.endswith('.dim')]:
		subset_path = f"subsets/{subset_file}"
		product = readProduct(subset_path)
		snaphu_export_path = SnaphuExport("snaphu", product)
		product.dispose() 



if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")