import pandas
from matplotlib import pyplot
from mpl_toolkits.basemap import Basemap
from library import PlotSettings

data = pandas.read_csv('demographic_data/locations.csv')

# usa = Basemap(projection='lcc', resolution=None,
#               width=6E6, height=3E6,
#               lat_0=35, lon_0=-100)

usa = Basemap(projection='cyl', resolution=None,
            llcrnrlat=0, urcrnrlat=50,
            llcrnrlon=-170, urcrnrlon=-170+150, )

world = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-50, urcrnrlat=70,
            llcrnrlon=-180, urcrnrlon=180, )

pyplot.figure(figsize=(10,4))
# -------------------------------------------------------
pyplot.subplot(2, 2, 1)
usa.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [0,1,2]')
x, y = usa(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y)
pyplot.title('Study 1a,b,c')
# -------------------------------------------------------
pyplot.subplot(2, 2, 2)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [3]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y)
pyplot.title('Study 2')
# -------------------------------------------------------
pyplot.subplot(2, 2, 3)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [0,1]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y)
pyplot.title('Study 1b,c')
# -------------------------------------------------------
pyplot.subplot(2, 2, 4)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [5]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y)
pyplot.title('Study 3')

pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('maps.pdf'))
pyplot.show()
PlotSettings.copy_output()
