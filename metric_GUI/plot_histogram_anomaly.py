#####################################
#
# plot_histogram_anomaly.py
#
#
# pass in:
#   incube - the cube to plot
#   what_am_i - th ncfile name to give a plot title
####################################

import iris
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import numpy as np
import make_big_anomaly
import pdb
import os


def main(incube, outpath, what_am_i, sc, file_searcher):
    # so the first thing we want to do here is use anomalies and not raw data
    # BUT WE ONLY WANT TO DO THIS IF WE ARE USING AN RCP scenario!
    if "rcp" in sc:
        print 'rcp in scenario'
        if not os.path.isfile(file_searcher+'_all_models_anomaly.nc'):
            incube = make_big_anomaly.main(incube, file_searcher, sc)
        else:
            incube = iris.load_cube(file_searcher+'_all_models_anomaly.nc')
    try:
       print len(incube.coord('longitude').points)
       incube = incube.collapsed('longitude',iris.analysis.MEAN)
    except AttributeError:
	print 'data already has lon collapsed'
    try:
	print len(incube.coord('latitude').points)
	incube = incube.collapsed('latitude',iris.analysis.MEAN)	
    except AttributeError:
	print 'data already has lat collapsed'
    data = incube.data
    print data.shape
    hist, h = np.histogram(data, bins=np.linspace(data.min(), data.max(),10))

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.bar(h[0:-1]+((h[1::]-h[0:-1])/2) ,hist, edgecolor='black', width =(h[1::]-h[0:-1]))
    xlab = raw_input("What metric is on the x axis (e.g. Marteau onset)")
    ax.set_xlabel(str(xlab)+' anomaly, '+str(sc)+' minus historical')
    ax.set_ylabel('Number of models')

    plt.savefig(str(what_am_i) + '_histogram_anomaly_all_models.png')
    plt.show()


if __name__ == "__main__":
    main(incube, outpath, what_am_i)
