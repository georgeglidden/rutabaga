var viewer = OpenSeadragon({
    id:            "openseadragon1",
    prefixUrl:     "/openseadragon/images/",
    navigatorSizeRatio: 0.25,
    wrapHorizontal:     true,
    tileSources:   {
        height: 512*256,
        width:  512*256,
        tileSize: 256,
        minLevel: 8,
        getTileUrl: function( level, x, y ){
            return "http://s3.amazonaws.com/com.modestmaps.bluemarble/" +
                    (level-8) + "-r" + y + "-c" + x + ".jpg";
        }
    }
});
