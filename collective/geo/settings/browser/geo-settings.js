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
        $.each($('div.widget-cgmap'), function(i, map) {
            var mapid = map.id;
            if (mapid != 'default')
            {
                /* can not deep copy OL objects because they have
                   circular references */
                var mapoptions = $.extend({}, cgmap.createDefaultOptions());
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
        var forms = $("form");
        // set center
        var lonlat = evt.object.getCenter();
        if (lonlat)
        {
            if (evt.object.displayProjection)
            {
                lonlat = lonlat.clone();
                lonlat.transform(evt.object.getProjectionObject(), evt.object.displayProjection);
            }
            set_input(forms, evt.object.div.id, 'lon', lonlat.lon);
            set_input(forms, evt.object.div.id, 'lat', lonlat.lat);
        }
        set_input(forms, evt.object.div.id, 'zoom', evt.object.getZoom());
    }

    function map_changebaselayer(evt)
    {
        // TODO: need to use layer name.. but may contain spaces
        var forms = $("form");
            var baselayer = this.baseLayer;
        if (baselayer)
        {
            set_input(forms, this.div.id, 'activebaselayer', baselayer.name);
        }
    }

    function map_changelayer(evt)
    {
        // TODO: need to use layer name.. but may contain spaces
        var forms = $("form");
        if (this.layers)
        {
            var layeridxs = [];
            for (var i=0; i < this.layers.length; i++)
            {
                var layer = this.layers[i];
                if ((!layer.visibility) || layer.isBaseLayer) continue;
                layeridxs.push(i);
            }
            set_input(forms, this.div.id, 'activelayers', layeridxs.join(' '));
        }
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

            if (0) {
                if (x >= 0 && y >= 0)
                {
                    return this.url + z + "/" + x + "/" + y + "." + this.type;
                }
                else
                {
                    // return "none.png";
                    return "http://www.maptiler.org/img/none.png";
                }
            } else {
                if (this.map.baseLayer.CLASS_NAME == 'OpenLayers.Layer.VirtualEarth') {
                    // if (this.map.baseLayer.name == 'Virtual Earth Roads' ||
                    //     this.map.baseLayer.name == 'Virtual Earth Aerial' ||
                    //     this.map.baseLayer.name == 'Virtual Earth Hybrid') {
                    z = z + 1;
                }
                //if (mapBounds.intersectsBounds( bounds )) {
                if (x >= 0 && y >= 0) {
                    //console.log( this.url + z + "/" + x + "/" + y + "." + this.type);
                    return this.url + z + "/" + x + "/" + y + "." + this.type;
                } else {
                    // return "none.png";
                    return "http://www.maptiler.org/img/none.png";
                }
            }
        },

        initmap: function(mapid, map_options)
        {
            var map = new OpenLayers.Map(mapid, map_options);
            var layers = [];

            if (! cgmap.state[mapid]) { cgmap.state[mapid] = {}; }
            if (! cgmap.config[mapid]) { cgmap.config[mapid] = {}; }
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
            var forms = $('form');
            var state = cgmap.state[mapid];
            if (state.lon != undefined)
            {
                pos.lon = state.lon;
                set_input(forms, mapid, 'lon', pos.lon);
            }
            if (state.lat != undefined)
            {
                pos.lat = state.lat;
                set_input(forms, mapid, 'lat', pos.lat);
            }
            if (state.zoom  != undefined)
            {
                pos.zoom = state.zoom;
                set_input(forms, mapid, 'zoom', pos.zoom);
            }

            pos.lonlat = new OpenLayers.LonLat(pos.lon, pos.lat);

            /* if map has a display projection we need to transform the center */
            if (map.displayProjection)
            {
                pos.lonlat.transform(map.displayProjection, map.getProjectionObject());
            }
            map.setCenter(pos.lonlat, pos.zoom);
            /* if map has no center zoom to max oxtent */
            if (!map.getCenter())
            {
                map.zoomToMaxExtent();
            }
            /* apply active layers */
            // TODO: need to use layer name.. but may contain spaces
            if (state.activebaselayer != undefined)
            {
                var baseLayer = map.getLayersByName(state.activebaselayer)[0];
                if (baseLayer)
                {
                    map.setBaseLayer(baseLayer);
                }
                set_input(forms, mapid, 'activebaselayer', state.activebaselayer);
            }
            if (state.activelayers != undefined)
            {
                var activelayers = state.activelayers.split(' ');
                for (i=0; i< map.layers.length; i++)
                {
                    var layer = map.layers[i];
                    if (layer.isBaseLayer) {
                        continue;
                    }
                    layer.setVisibility( $.inArray(i.toString(), activelayers) >= 0 );
                }
                set_input(forms, mapid, 'activelayers', state.activelayers);
            }
            /* store map instance */
            cgmap.config[mapid].map = map;

            /* register form update listener */
            map.events.register("moveend", map, map_moveend);
            map.events.register("changebaselayer", map, map_changebaselayer);
            map.events.register("changelayer", map, map_changelayer);
        },

        extendconfig: function(options, mapid)
        {
            // TODO: may not be good with new default-handling
            if (!mapid) { mapid='default'; }
            if (!cgmap.config[mapid]) { cgmap.config[mapid] = {}; }
            $.extend(cgmap.config[mapid], options);
        },

        createDefaultOptions: function() {
            return {
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                //numZoomLevels: 22, // 19
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds( -20037508, -20037508,
                                                  20037508, 20037508.34),
                controls: [
                    new OpenLayers.Control.ArgParser(),
                    //new OpenLayers.Control.PanZoomBar(),
                    new OpenLayers.Control.Attribution(),
                    new OpenLayers.Control.LayerSwitcher(),
                    new OpenLayers.Control.MousePosition(),
                    new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
                    new OpenLayers.Control.KeyboardDefaults(),
                    new OpenLayers.Control.PanZoom()
                ]
            };
        },

        /* holds configuration values for all maps on this page
         * there should be one entry 'default' and maybe one for each map on
         * the page to override default values.
         */
        config: { },

        /* holds current state for all maps on this page
         * there should be one entry 'default' and maybe one for each map on
         * the page to override default values.
         */
        state: {}

    });

}(jQuery);


/** A few extension classes making it easier to work with openlayers
 * - a configurable EditingToolbar
 * - a Remove'Draw'Feature
 */

OpenLayers.Control.MarkerEditingToolbar = OpenLayers.Class(
    OpenLayers.Control.Panel, {

        initialize: function(layer, options) {
            OpenLayers.Control.Panel.prototype.initialize.apply(this, [options]);

            this.addControls(
	        [ new OpenLayers.Control.Navigation() ]
            );
            var controls = [
	        new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Point, {'displayClass': 'olControlDrawFeaturePoint'}),
                new OpenLayers.Control.ModifyFeature(layer)
            ];
            this.addControls(controls);

            this.defaultControl = this.controls[0];

            // TODO: don't replace... rather override
            var defaultstyle = OpenLayers.Util.applyDefaults({
                // Set the external graphic and background graphic images.
                externalGraphic: "img/marker.png",
                backgroundGraphic: "img/marker_shadow.png",

                // Makes sure the background graphic is placed correctly relative
                // to the external graphic.
                backgroundXOffset: 0,
                backgroundYOffset: -7,
                fillOpacity: 1,

                // Set the z-indexes of both graphics to make sure the background
                // graphics stay in the background (shadows on top of markers looks
                // odd; let's not do that).
                graphicZIndex: 11, //MARKER_Z_INDEX,
                backgroundGraphicZIndex: 10, //SHADOW_Z_INDEX,

                pointRadius: 10
            }, OpenLayers.Feature.Vector.style['default']);
            layer.styleMap = new OpenLayers.StyleMap({"default": defaultstyle,
                                                      "select": {externalGraphic: "img/marker-gold.png"}});

            // setup form events
            if (this.lonid && this.latid)
            {
                var point = new OpenLayers.Geometry.Point(jq('#' + this.lonid).val(),
                                                          jq('#' + this.latid).val());
                if (layer.map.displayProjection)
                {
                    point.transform(layer.map.displayProjection, layer.map.getProjectionObject());
                }
                layer.addFeatures([new OpenLayers.Feature.Vector(point)]);
                layer.events.register("featureadded", this, this.updateForm);
                layer.events.register("featuremodified", this, this.updateForm);
            }
            if (this.zoomid)
            {
                layer.map.events.register("zoomend", this, this.updateZoom);
            }
            // ensure only one feature is on the map
            layer.events.register("beforefeaturesadded", this, function(evt)
                                  {
                                      evt.object.destroyFeatures();
                                  });
        },

        updateZoom: function(evt)
        {
            jq('#' + this.zoomid).val(evt.object.getZoom());
        },

        updateForm: function(evt)
        {
            var lonlat = new OpenLayers.LonLat(evt.feature.geometry.x, evt.feature.geometry.y);
            if (evt.object.map.displayProjection)
            {
                lonlat.transform(evt.object.map.getProjectionObject(), evt.object.map.displayProjection);
            }
            jq('#' + this.lonid).val(lonlat.lon);
            jq('#' + this.latid).val(lonlat.lat);
        },

        CLASS_NAME: 'OpenLayers.Control.EditingToolbar'

    }
);


OpenLayers.Control.WKTEditingToolbar = OpenLayers.Class(
    OpenLayers.Control.Panel, {

        initialize: function(layer, options) {
            OpenLayers.Control.Panel.prototype.initialize.apply(this, [options]);

            this.addControls(
	        [ new OpenLayers.Control.Navigation() ]
            );
            var controls = [
                new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Point, {'displayClass': 'olControlDrawFeaturePoint'}),
                new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Path, {'displayClass': 'olControlDrawFeaturePath'}),
 	        new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'}),
                new OpenLayers.Control.ModifyFeature(layer)
            ];
            this.addControls(controls);

            this.defaultControl = this.controls[0];

            // init edit layer features
            if (this.wktid)
            {
                var geomwkt = document.getElementById(this.wktid).value;
                var in_options = {
                    internalProjection: layer.map.getProjectionObject(),
                    externalProjection: layer.map.displayProjection };
                var format = new OpenLayers.Format.WKT(in_options);
                var feat = format.read(geomwkt);
                if (feat)
                {
                    layer.addFeatures([feat]);
                }
            }

            layer.events.register("featureadded", this, this.updateWKTWidget);
            layer.events.register("featuremodified", this, this.updateWKTWidget);

            // ensure only one feature is on the map
            layer.events.register("beforefeaturesadded", this, function(evt) {
                evt.object.destroyFeatures();
            });
        },

        updateWKTWidget: function(evt) {
            var out_options = {
                internalProjection: evt.object.map.getProjectionObject(),
                externalProjection: evt.object.map.displayProjection };
            var format = new OpenLayers.Format.WKT(out_options);
            document.getElementById(this.wktid).value = format.write(evt.feature);
            format.destroy();
        },

        CLASS_NAME: 'OpenLayers.Control.EditingToolbar'

    }
);