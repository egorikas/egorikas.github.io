---
title:  "How to generate vector tiles for offline using from OSM metadata"
description: "Guide about creating vector maps which can be read by Mapsforge software"
modified: 2018-04-22T23:24:00-03:00
tags:
  - open source 
  - open street map
  - .net core
  - .net
---

Hi everyone! Today I want to talk about generating vector tiles for offline using from OSM metadata.
I'll tell you about my journeys with them and give some links. Let's get started.

## Why did I need them?
Once, I wrote a  about <a href="http://egorikas.com/download-open-street-tiles-for-offline-using/">blog-post</a> dowloading open street maps tiles.
After release, client decided to switch application from usual tiles to vector ones. And that was the strange journey, but I want to share this expirience with you.


## Why Mapsforge?
<a href="https://github.com/mapsforge/mapsforge">Mapsforge</a> is an open-source solution and the client wanted to use it)


## So, what should I do?

First of all, you need to dowload a file with OSM raw-data. In my case I needed the whole planet's map (because the client wanted to generate different places from it), so 
I downloaded a file for the whole <a href="https://wiki.openstreetmap.org/wiki/Planet.osm#Processing_the_File">planet</a> ......

## A few days later...

After the file had been downloaded, I started to investigate, what I could do with it.
So, this is the list of steps.
1. Read about <a href="https://github.com/cgeo/cgeo/wiki/How-to-create-your-own-offline-maps">generation maps for Mapsforge</a>
2. Read about <a href="https://wiki.openstreetmap.org/wiki/Osmosis">Osmosis tool</a> and <a href="https://github.com/openstreetmap/osmosis">grab it</a>
3. Read about <a href="https://github.com/mapsforge/mapsforge/blob/master/docs/Getting-Started-Map-Writer.md">mapsforge map-writer</a>
4. Configure `osmosis` and `mapsforge map-writer`

## Generation

You need to call the commands 

```
osmosis --read-pbf planet-latest.osm.pbf --bounding-box top={top} left={left} bottom={bottom} right={right} --write-pbf map.pbf
osmosis --rb file="map.pbf" --mapfile-writer file="map.map"
```

Coordinates for `left|bottom|right|top`, you can check at <a href="http://tools.geofabrik.de/calc/">tiles calculator</a>
<figure class="align-center" style="width: 422px; height: 391px">
	<a href="/assets/images/osm/choosing_osmosis.png"><img src="/assets/images/osm/choosing_osmosis.png"></a>
</figure>

## An hour later ...

Generating of one map takes about an hour. So, just wait and you get a result.

## P.S. for C# developers

There is a possibility to use `.net` libraries instead of 

```
osmosis --read-pbf planet-latest.osm.pbf --bounding-box top={top} left={left} bottom={bottom} right={right} --write-pbf map.pbf
```

Go to <a href="https://github.com/OsmSharp/">OsmSharp's repo</a>. These guys did a great job and you can parse `some_area.osm.pbf` without osmosis.
It's regrettable, but I haven't find the solution for generating vector maps in geofabrik format without `mapsforge map-writer`.


## Conclusion

That’s all, thank you for you attention!
