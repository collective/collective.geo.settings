

from collective.geo.settings.browser.widget import MapLayer

class OSMMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "osm"

    jsfactory = """
    function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
        'http://tile.openstreetmap.org/',
        { 'type' : 'png',
          getURL: cgmap.osm_getTileURL,
          displayOutsideMaxExtent: true,
          attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'});}"""

class BingStreetMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "bmap"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Streets',
        { 'type': VEMapStyle.Shaded,
          'sphericalMercator': true });}"""

class BingRoadsMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "brod"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Roads',
        { 'type': VEMapStyle.Road,
          'sphericalMercator': true });}"""

class BingAerialMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "baer"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Aerial',
        { 'type': VEMapStyle.Aerial,
          'sphericalMercator': true });}"""

class BingHybridMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "bhyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Hybrid',
        { 'type': VEMapStyle.Hybrid,
          'sphericalMercator': true });}"""

class GoogleStreetMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "gmap"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Google',
        {'sphericalMercator': true});}"""

class GoogleSatelliteMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "gsat"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Satellite (Google)' ,
        {'type': G_SATELLITE_MAP, 'sphericalMercator': true});}"""

class GoogleHybridMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "ghyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Hybrid (Google)' ,
        {'type': G_HYBRID_MAP, 'sphericalMercator': true});}"""

class GoogleTerrainMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "gter"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Terrain (Google)' ,
        {'type': G_PHYSICAL_MAP, 'sphericalMercator': true});}"""

class YahooStreetMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "ymap"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Street',
        {'type': YAHOO_MAP_REG, 'sphericalMercator': true});}"""

class YahooSatelliteMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "ysat"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Satellite',
        {'type': YAHOO_MAP_SAT, 'sphericalMercator': true});}"""

class YahooHybridMapLayer(MapLayer):

    def __init__(self):
        pass

    name = "yhyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Hybrid',
        {'type': YAHOO_MAP_HYB, 'sphericalMercator': true});}"""
