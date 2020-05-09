Title: Plotly without borders: choropleth maps with Mapbox and custom borders
Date: 2018-11-23 10:46
Category: Data Science
Tags: plotly, python, maps, geojson, mapbox
Slug: plotly_choropleth_map
Description: A tutorial to draw nice looking interactive choropleth maps with plotly using a custom geojson file and a Mapbox map. Plotting the 2017 unemployment rate of Italian provinces.

When it comes to plotting interactive maps with python you do not have many choices.
The best modules out there are Bokeh, Plotly and Folium. Among the many types
of maps that you can think of, one in particular can be pretty tricky to draw: the choropleth map.
In this map you colour the area within the borders of a particular region
(can be a state, a province, a county, etc.) based on some aggregated metric of that region.

The problem with plotly's choropleth map is that it is limited to the US states, US counties and world countries.
If you have your custom borders for whatever location on planet earth, the solution is to resort to
a _scattermapbox_ plot, which uses the world map provided by Mapbox, and overlay your
custom borders on top of this map.
You need to get a free [Mapbox access token](https://www.mapbox.com/help/define-access-token/)
in order to use this type of plot.

This solution, I have to admit, feels a bit hacky because of the amount of
preprocessing involved. The end result, however, is definitely worth it.
You will have a full interactive map that you can inspect down to the street level,
with customisable hover tools and all the great features that plotly offers, one for all: the iframe embedding.

I will plot the 2017 unemployment rates of the Italian provinces for the population older than 15.
The end result is going to look like this:

<iframe width="900" height="800" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/24.embed"></iframe>

In this post I take you through the steps necessary to make this map.
[Here is](https://github.com/vincepota/plotly_choropleth_tutorial/blob/master/tutorial.ipynb) the jupyter notebook.

### Usual housekeeping


```python
import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process
from matplotlib.colors import Normalize
from matplotlib import cm
from itertools import product
import copy

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.plotly as ply

MAPBOX_APIKEY = "Your_Mapbox_API_key"
```

### The Data

The [raw data](http://dati.istat.it/Index.aspx?DataSetCode=DCCV_TAXDISOCCU1#) come from the Italian National Institute of Statistics.
After some quick data preprocessing with pandas, I saved the final dataset
[to csv](https://github.com/vincepota/plotly_choropleth_tutorial/blob/master/italy_unemployment_2017.csv).

```python
un = pd.read_csv('italy_unemployment_2017.csv', index_col=0)
un = un['Value']/100. # from dataframe to series
un.name = 'province' # from Italian to english
un.head()
#
# province
# Torino                  0.093748
# Vercelli                0.096164
# Biella                  0.071894
# Verbano-Cusio-Ossola    0.068392
# Novara                  0.111541
```

### Get and load the geojson

The province borders come from a [geojson file](http://geojson.org/).
A geojson is a json file with standardised keys, each mapping to geographical
features (coordinates of lines, points or polygons) and to non-geographical features.
You will be able to find detailed geojsons for most of the countries in the world.
[Highmaps](https://code.highcharts.com/mapdata/) is a rich resource to start with.
Here I am using the geojson of the Italian provinces [published by datajournalism](https://gist.github.com/datajournalism-it/212e7134625fbee6f9f7).

```python
with open('province.geojson') as f:
     geojson = json.load(f)

# the total number of provinces
n_provinces = len(geojson['features'])

# the provinces names
province_names = [geojson['features'][k]['properties']['NOME_PRO'] for k in range(n_provinces)]
print("there are {} provinces ".format(n_provinces))
#  there are 110 provinces
```
Note that the key `properties` contains the non-geographical features that will change from geojson to geojson.

### Get the centroid of each province

These are the x and y coordinates needed by `scattermapbox`.
Plotly does not support hover text over a polygon, so we need to draw tiny scatter points
at the centre of each province so that when we hover over it, it will give the impression that the hover text is coming
from the province polygon itself.

```python
def get_centers():
    lon, lat =[], []

    for k in range(n_provinces):
        geometry = geojson['features'][k]['geometry']

        if geometry['type'] == 'Polygon':
            coords=np.array(geometry['coordinates'][0])
        elif geometry['type'] == 'MultiPolygon':
            coords=np.array(geometry['coordinates'][0][0])

        # the centroids
        lon.append(sum(coords[:,0]) / len(coords[:,0]))
        lat.append(sum(coords[:,1]) / len(coords[:,1]))

    return lon, lat
```

### Match the province names of dataframe and geojson

We need to match the province name in the dataframe with the province name in the geojson.
This is easy when we are matching, for instance, _MILANO_ with _Milano_. However, there are cases
where the match is not straightforward because of spelling differences.
For instance, the same province is spelled _Reggio di Calabria_ in the dataframe and _Reggio Calabria_ in the geojson.
I am sure similar cases can be found in the province names of other countries.

To fix this mismatch, you can fuzzy match the strings and take only the strings with the highest match rate.

```python
def match_regions(list1, list2):
    # take only the best match
    matched = [process.extract(list1[i], list2, limit=1, scorer=fuzz.partial_ratio)[0][0] for i in range(0,len(list1))]

    return {key: value for (key, value) in zip(list1, matched)}

match_dict = match_regions(un.index, province_names)
print(match_dict)

# {'Prato': 'Prato',
# 'Ragusa': 'Ragusa',
# 'Ravenna': 'Ravenna',
# 'Reggio di Calabria': 'Reggio Calabria',
# "Reggio nell'Emilia": 'Reggio Emilia',
# 'Rieti': 'Rieti',
# 'Rimini': 'Rimini',
# ...
# }
```

and you can see that _Reggio di Calabria_ has been matched to _Reggio Calabria_. The function above can match all the provinces but two.
This is good enough for this tutorial.

### Reindex the dataframe

Rename and reindex the dataframe to match the province names in the geojson. Give it the same ordering as the geojson.

```python
df_tmp = un.copy() # do not overwrite the dataframe
df_tmp.index = df_tmp.index.map(match_dict) # rename
df_tmp = df_tmp[~df_tmp.index.duplicated(keep=False)] # drop duplicates
                                                      # from fuzzy match gone wrong
#give the same index order as the geojson
df_reindexed = df_tmp.reindex(index = province_names)
```

### Create source dictionaries

Create the dictionary that plotly uses to draw the province borders.
In this specific case I have 108 provinces with an average of 1500 longitude and latitude pairs for each province.
Plotly can take a few seconds to render all these borders.

Depending on the resolution of your geojson and on the purpose of your map,
you might consider downsampling the longitude and latitude coordinates.
Downsampling the coordinates will decrease the resolution of the borders, but it will speed up the rendering time.
I argue that, with these particular data, you can barely tell the difference between original and downsampled borders.

```python
def make_sources(downsample = 10):
    sources = []
    geojson_copy = copy.deepcopy(geojson['features']) # do not oeverwrite the original file

    for feature in geojson_copy:

        if downsample > 0:
            coords = np.array(feature['geometry']['coordinates'][0][0])
            coords = coords[::downsample]
            feature['geometry']['coordinates'] = [[coords]]

        sources.append(dict(type = 'FeatureCollection',
                            features = [feature])
                      )
    return sources
```

### Create and normalise the colour scale

Generate a list of normalised rgba colours for each province. Use grey if data are missing.
Given a colourmap and a normalization object, the matplotlib function `scalarmappable()` transforms input
floats into rgba colours using the `to_rgba()` method.

The colourscale of the colourbar also needs to be custom made because plotly offers less variety of
colourmaps with respect to matplotlib.
In order to use the full library of [matplotlib colourmaps](https://matplotlib.org/examples/color/colormaps_reference.html),
the plotly documentation states:

> the colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsv, or named color string...

which is what I am doing in  `get_colorscale()`.

```python
def scalarmappable(cmap, cmin, cmax):
        colormap = cm.get_cmap(cmap)
        norm = Normalize(vmin=cmin, vmax=cmax)
        return cm.ScalarMappable(norm=norm, cmap=colormap)

def get_scatter_colors(sm, df):
    grey = 'rgba(128,128,128,1)'
    return ['rgba' + str(sm.to_rgba(m, bytes = True, alpha = 1)) if not np.isnan(m) else grey for m in df]

def get_colorscale(sm, df, cmin, cmax):
    xrange = np.linspace(0, 1, len(df))
    values = np.linspace(cmin, cmax, len(df))

    return [[i, 'rgba' + str(sm.to_rgba(v, bytes = True))] for i,v in zip(xrange, values) ]
```

### Customise the hover text

Change the hover text for provinces with no data.

```python
def get_hover_text(df) :
    text_value = (df*100).round(2).astype(str) + "%"
    with_data = '<b>{}</b> <br> {} unemployment rate'
    no_data = '<b>{}</b> <br> no data'

    return [with_data.format(p,v) if v != 'nan%' else no_data.format(p) for p,v in zip(df.index, text_value)]
```
## Ready to plot

We have everything we need to assemble the plot. Let's call all the functions defined above.
I have chosen a _Blues_ colourmap, but you can choose any of the matplotlib colourmaps.

```python
colormap = 'Blues'
cmin = df_reindexed.min()
cmax = df_reindexed.max()

sources = make_sources(downsample=10)
lons, lats = get_centers()

sm = scalarmappable(colormap, cmin, cmax)
scatter_colors = get_scatter_colors(sm, df_reindexed)
colorscale = get_colorscale(sm, df_reindexed, cmin, cmax)
hover_text = get_hover_text(df_reindexed)

tickformat = ".0%"
```

### Define the scatter plot

The scatter points have the same colour as the surrounding region, so they are invisible.
However, we use these points to see the hover text.
Here we also style the colourbar.

```python
data = dict(type='scattermapbox',
            lat=lats,
            lon=lons,
            mode='markers',
            text=hover_text,
            marker=dict(size=1,
                        color=scatter_colors,
                        showscale = True,
                        cmin = df_reindexed.min(),
                        cmax = df_reindexed.max(),
                        colorscale = colorscale,
                        colorbar = dict(tickformat = tickformat)
                       ),
            showlegend=False,
            hoverinfo='text'
             )
```

### Define the layers

Two layers: one for the province borders and one for the filling of each border.
Currently `sourcetype` only supports `geojson` or `vector`.

```python
layers=([dict(sourcetype = 'geojson',
              source =sources[k],
              below="",
              type = 'line',    # the borders
              line = dict(width = 1),
              color = 'black',
              ) for k in range(n_provinces)
          ] +

        [dict(sourcetype = 'geojson',
              source =sources[k],
              below="water",
              type = 'fill',   # the area inside the borders
              color = facecolor[k],
              opacity=0.8
             ) for k in range(n_provinces)
         ]
        )
```

### Define the plotly layout

The usual plotly layout with Mapbox specific properties. Keys to watch are
`hoverdistance` to fine tune the responsiveness of the hover tool, `center`
to centre the map, and `style` to style the Mapbox map using their
[built-in styles](https://www.mapbox.com/mapbox-gl-js/example/setstyle/).

```python
data_url = "http://dati.istat.it/Index.aspx?DataSetCode=DCCV_TAXDISOCCU1#"

layout = dict(title="2017 Unemployment Rate per Italian provinces <br> " +
                    """using <a href={}>open data</a> by the""".format(data_url) +
                      "Italian National Institute of Statistics",
              autosize=False,
              width=700,
              height=800,
              hovermode='closest',
              hoverdistance = 30,

              mapbox=dict(accesstoken=MAPBOX_APIKEY,
                          layers=layers,
                          bearing=0,
                          center=dict(
                                    lat=41.871941,  # the centre of Italy
                                    lon=12.567380),
                          pitch=0,
                          zoom=4.9,
                          style = 'light'
                          )
              )
```

### Plot it
```python
fig = dict(data=[data], layout=layout)
iplot(fig)
```

<iframe width="900" height="800" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/24.embed"></iframe>

## Wrapping up

Plotting a plotly choropleth map with custom geojson borders can be a tedious experience.
However, it is easy to wrap everything into a python class to make this task more pythonic.
After all, the input parameters to the functions that created this map are simply a dataframe, a colourmap,
and some styling parameters like title and zoom.
