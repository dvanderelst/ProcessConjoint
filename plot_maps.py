import pandas
from matplotlib import pyplot
from mpl_toolkits.basemap import Basemap
from library import PlotSettings

data = pandas.read_csv('demographic_data/locations.csv')

grp = data.groupby(['Set','Dataset'])
cnt = grp.count()
cnt = cnt.reset_index()
print(cnt)
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
subset = data.query('Set in [3]')
x, y = usa(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y, alpha=0.5)
pyplot.title('Study 1')
# -------------------------------------------------------
pyplot.subplot(2, 2, 2)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [0,1]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y, alpha=0.5)
pyplot.title('Study 2 and 3')
# -------------------------------------------------------
pyplot.subplot(2, 2, 3)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [5]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y, alpha=0.5)
pyplot.title('Study 4')
# -------------------------------------------------------
pyplot.subplot(2, 2, 4)
world.etopo(scale=0.5, alpha=0.5)
subset = data.query('Set in [4]')
x, y = world(subset.Longitude, subset.Latitude)
pyplot.scatter(x, y, alpha=0.5)
pyplot.title('Study 5')

pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('maps.pdf'))
pyplot.show()
PlotSettings.copy_output()
