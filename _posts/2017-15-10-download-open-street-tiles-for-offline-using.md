---
title:  "Download open street map tiles for offline usage"
description: "Instruction about downloading osm tiles for offile usage with C#"
modified: 2017-15-10T13:23:00-03:00
tags:
  - dot.net
  - open street map
  - open source
---
Hi everyone! Today I want to talk about downloading open street map tiles for offline usage.
I'll tell you about my journeys with them and give some links. Let's get started.

### Why did I need them?
One of my clients wanted to have a mobile app with offline maps. I was writing `API` for it.
Packing all arrays and adding maps to them were required because I needed to calculate final sizes of the arrays.


### How offline maps works?
Let's think about earth's map like about table. We have rows and columns. So, every piece of the land can be represented with the cell in this table.
You can ask me - "But how zooms works? How can I zoom-in and zoom-out maps in applications. If we have only one table?" - My answer - we have different tables.
Each one for the level of zoom. For example in our application we used 12-15 levels.

I can't say about another map's systems, but `open street map` has 19 levels of <a href="http://wiki.openstreetmap.org/wiki/Zoom_levels">zoom</a>.
For example, `level 0` represents the whole world and `level 13` represents a village or town.

You need at least 2 or 3 zoom levels for getting application's map works well (correct zoom, small viewing issues, users' satisfaction :) )

### Where can I grab them?

First of all, you need to understand that `OSM` is `OSS`. So, when you dowload data from their services, you will have to think about the consequences for all community. <a href="https://operations.osmfoundation.org/policies/tiles/">Official policy</a> tells you more about rules and don'ts.

<a href="http://wiki.openstreetmap.org/wiki/Tiles">This page</a> contains some useful info about tiles, such as list of servers, tools and so on.
As for me I was using official server with 3 subdomains:
1. <a href="http://a.tile.openstreetmap.org">`a.tile.openstreetmap.org`</a>
2. <a href="http://b.tile.openstreetmap.org">`b.tile.openstreetmap.org`</a>
3. <a href="http://c.tile.openstreetmap.org">`c.tile.openstreetmap.org`</a>

### Implementation

First of all you need coordinates of the area. 
I higly recommend <a href="http://tools.geofabrik.de/calc/">this tool</a>.

Let's imagine we need map of Saint-Petersburg for offile using.
There a few steps, which we need to do for getting them:

#### 1. Getting coordinates<a name="getting-coordinates"></a>

1. Open <a href="http://tools.geofabrik.de/calc/">tiles calculator</a>
<figure>
	<a href="/assets/images/osm/choosing.png"><img src="/assets/images/osm/choosing.png"></a>
	<figcaption>City choosing</figcaption>
</figure>

2. Go to `CD` tab and notice `Osmosis Copy` field
<figure>
	<a href="/assets/images/osm/coordinates.png"><img src="/assets/images/osm/coordinates.png"></a>
	<figcaption>City choosing</figcaption>
</figure>

You need coordinates of two points. Bottom left and top right. You need them because of tiles presenting system.
As I said in the first paragraph, tiles are stored in the grid (table) format. For calculating numbers of tiles,
we need to know coordinates of the left bottom tile (number 1 on the picture) and top right tile. If we know them, we are able to calculate ranges.
<figure>
	<a href="/assets/images/osm/grid.png"><img src="/assets/images/osm/grid.png"></a>
	<figcaption>Grid system</figcaption>
</figure>

#### 2. Writing code

1. Go to the github and see <a href="https://github.com/OsmSharp/tiles">this package</a>. It contains the great example of 
tiles abstraction writing with C# language.

2. Create two tiles with coordinates, which you got in <a href="#getting-coordinates">getting coordinates section</a>.

```csharp
   var leftBottom = Tile.CreateAroundLocation(double.Parse("59.17"), double.Parse("28.63"), 14);
   var topRight = Tile.CreateAroundLocation(double.Parse("60.85"), double.Parse("31.81"), 14);
```
3. Then create `TileRange` and be ready for dowloading tiles :)

```csharp
  //dirty, but obvious :)
  var minX = Math.Min(leftBottom.X, topRight.X);
  var maxX = Math.Max(leftBottom.X, topRight.X);

  var minY = Math.Min(leftBottom.Y, topRight.Y);
  var maxY = Math.Max(leftBottom.Y, topRight.Y);

  var tiles = new TileRange(minX, minY, maxX, maxY, zoom);
```

#### 3. Downloading tiles
Fow downloading tiles. You need to do `GET` requests in `{server}.tile.openstreetmap.org/{zoom}/{x}/{y}.png` format.
Where:
1. `{server}` - symbol of server (a,b,c)
2. `{zoom}` - level of zoom
3. `{x}` - x position of the tile
4. `{y}` - y postion of the tile 

```csharp
    foreach(var tile in tiles){
      //only one server name is just for the example. It's not recommended to use only 1 server endpoint
      var endpointUrl = $"http://a.tile.openstreetmap.org/14/{tile.X}/{tile.Y}.png"
    }
```

#### 4. Example of downloading tiles
Example below is just my personal implementation and I don't force you to do it in the same way
```csharp
        private readonly string[] _serverEndpoints = {"a", "b", "c"};

        public async Task DownloadTiles(int cityId, TileRange range, int zoom)
        {
            var random = new Random();
            var maxDegreeOfParalellism = 2;
            await range.ParallelForEachAsync(async tile =>
            {
                var url =
                    $"http://{_serverEndpoints[random.Next(0, 2)]}.tile.openstreetmap.org/{zoom}/{tile.X}/{tile.Y}.png";
                var data = await _client.GetByteArrayAsync(url);

            }, maxDegreeOfParalellism);
        }
```
`ParallelForEachAsync` available on <a href="https://github.com/tyrotoxin/AsyncEnumerable">github</a>.
`maxDegreeOfParalellism` equals two because of <a href="https://operations.osmfoundation.org/policies/tiles/">official policy</a>.


### P.S.

I need to say again, that `OSM` is `OSS` project. This means that you shouldn't build software with massive calls to `OSM` endpoints. If you do this, your `IP` will be ban. If you need to serve a lot of client requests, you can create your own tiles server or use paid-solutions.

### Conclusion

That's all. I'll be happy, It this article helps you.