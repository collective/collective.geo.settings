/* cgmap is a namespace object, holding all relevant javascript
 * variables and methods used within collective.geo.*
 */

/* define a few common Openlayers methods to be reused */

var cgmap = function($)
{
  if (!cgmap)
  {
    cgmap = { };
  }

  /* initalise all maps after page has been loaded and the dom tree
   * is fully intstantiated
   */
  $(document).ready( function() {
    $.each($('div.cgmap'), function(i, map) {
      var mapid = map.id;
      if (mapid != 'default')
      {
        /* can not deep copy OL objects because they have circular references */
        var mapoptions = $.extend({}, cgmap.config['default'].options);
        /* merge in map specific settings */
        if (cgmap.config[mapid])
        {
          $.extend(mapoptions, cgmap.config[mapid].options);
        }
        cgmap.initmap(mapid, mapoptions);

        $(map).parents().bind("scroll", mapid, function(evt) {
                                cgmap.config[evt.data].map.events.clearMouseCache();
                              });

      }
    });

  });

  /* adds/sets hidden input field in forms
   *
   */
  function set_input(forms, id, name, value)
  {
    var iname = 'cgmap_state.' + id + "." + name + ":record";
    var inputs = forms.find("[name='" + iname + "']");
    if (inputs.length == 0)
    {
      var keyelems = forms.find("[name='cgmap_state_mapids']");
      if (keyelems.length == 0)
      {
        forms.append("<input type='hidden' name='cgmap_state_mapids' value='" + id + "' />");
      }
      else if (keyelems[0].value.indexOf(id) < 0)
      {
        keyelems.val(keyelems[0].value + ' ' + id);
      }
      inputs = forms.append("<input type='hidden' name='" + iname + "' />");
      inputs = forms.find("[name='" + iname + "']");
    }
    inputs.val(value);
  }

  function map_moveend(evt)
  {
    var forms = jq("form");
    // set center
    var lonlat = evt.object.getCenter();
    if (lonlat)
    {
      if (evt.object.displayProjection)
      {
        lonlat = lonlat.clone();
        lonlat.transform(evt.object.projection, evt.object.displayProjection);
      }
      set_input(forms, evt.object.div.id, 'lon', lonlat.lon);
      set_input(forms, evt.object.div.id, 'lat', lonlat.lat);
    }
    set_input(forms, evt.object.div.id, 'zoom', evt.object.getZoom());
  }

  function map_changebaselayer(evt)
  {
    var forms = jq("form");
    // TODO: set active base layer
  }

  function map_changelayer(evt)
  {
    var forms = jq("form");
    // TODO: set active overlays
  }


  return $.extend(cgmap, {

    osm_getTileURL: function(bounds)
    {
      var res = this.map.getResolution();
      var x = Math.round((bounds.left - this.maxExtent.left) /
                         (res * this.tileSize.w));
      var y = Math.round((this.maxExtent.top - bounds.top) /
                         (res * this.tileSize.h));
      var z = this.map.getZoom();
      var limit = Math.pow(2, z);

      if (y < 0 || y >= limit)
      {
        return OpenLayers.Util.getImagesLocation() + "404.png";
      }
      else
      {
        x = ((x % limit) + limit) % limit;
        return this.url + z + "/" + x + "/" + y + "." + this.type;
      }
    },

    overlay_getTileURL: function(bounds)
    {
      var res = this.map.getResolution();
      var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
      var y = Math.round((bounds.bottom - this.maxExtent.bottom) / (res * this.tileSize.h));
      var z = this.map.getZoom();
      if (x >= 0 && y >= 0)
      {
        return this.url + z + "/" + x + "/" + y + "." + this.type;
      }
      else
      {
        return "http://www.maptiler.org/img/none.png";
      }
    },

    initmap: function(mapid, map_options)
    {
      var map = new OpenLayers.Map(mapid, map_options);
      var layers = [];

      if (! cgmap.state[mapid]) { cgmap.state[mapid] = {}; }
      if (! cgmap.config[mapid]) { cgmap.config[mapid] = {}; }
      /* merge default and map specifc layers if asked to */
      if (!cgmap.config[mapid].nodefaultlayers)
      {
        layers.push.apply(layers, cgmap.config['default'].layers);
      }
      if (cgmap.config[mapid].layers)
      {
        layers.push.apply(layers, cgmap.config[mapid].layers);
      }
      /* add collected layers to map */
      for (var i=0; i < layers.length; i++)
      {
        map.addLayer(layers[i]());
      }
      /* determine map-state (center and zoom) */
      var pos = { lon: cgmap.state['default'].lon,
                  lat: cgmap.state['default'].lat,
                  zoom: cgmap.state['default'].zoom};
      /* add hidden fields to all forms to pass map-states on form submit
       * and get the values back if me stay on this page
       */
      var forms = jq('form');
      if (cgmap.state[mapid].lon)
      {
        pos.lon = cgmap.state[mapid].lon;
        set_input(forms, mapid, 'lon', pos.lon);
      }
      if (cgmap.state[mapid].lat)
      {
        pos.lat = cgmap.state[mapid].lat;
        set_input(forms, mapid, 'lat', pos.lat);
      }
      if (cgmap.state[mapid].zoom)
      {
        pos.zoom = cgmap.state[mapid].zoom;
        set_input(forms, mapid, 'zoom', pos.zoom);
      }

      pos.lonlat = new OpenLayers.LonLat(pos.lon, pos.lat);

      /* if map has a display projection we need to transform the center */
      if (map.displayProjection)
      {
        pos.lonlat.transform(map.displayProjection, map.projection);
      }
      map.setCenter(pos.lonlat, pos.zoom);
      /* if map has no center zoom to max oxtent */
      if (!map.getCenter())
      {
        map.zoomToMaxExtent();
      }
      /* store map instance */
      cgmap.config[mapid].map = map;

      /* register form update listener */
      map.events.register("moveend", map, map_moveend);
      // map.events.register("changebaselayer", map, map_changebaselayer);
      // map.events.register("changelayer", map, map_changelayer);
    },

    extendconfig: function(options, mapid)
    {
      if (!mapid) { mapid='default'; }
      if (!cgmap.config[mapid]) { cgmap.config[mapid] = {}; }
      $.extend(cgmap.config[mapid], options);
    },

    /* holds configuration values for all maps on this page
     * there should be one entry 'default' and maybe one for each map on
     * the page to override default values.
     */
    config: { 'default':
              { 'options':
                { //theme: null, if sot to null, editingtoolbar does nt show up
                  projection: new OpenLayers.Projection("EPSG:900913"),
                  displayProjection: new OpenLayers.Projection("EPSG:4326"),
                  units: "m",
                  numZoomLevels: 22, // 19
                  maxResolution: 156543.0339,
                  maxExtent: new OpenLayers.Bounds( -20037508.34, -20037508.34,
                                                    20037508.34, 20037508.34),
                  controls: [
                    new OpenLayers.Control.ArgParser(),
                    new OpenLayers.Control.PanZoomBar(),
                    new OpenLayers.Control.Attribution(),
                    new OpenLayers.Control.LayerSwitcher(),
                    new OpenLayers.Control.MousePosition(),
                    new OpenLayers.Control.KeyboardDefaults(),
                    new OpenLayers.Control.ZoomBox()
                  ]
                }}},

    /* holds current state for all maps on this page
     * there should be one entry 'default' and maybe one for each map on
     * the page to override default values.
     */
    state: {}

  });

}(jQuery);
