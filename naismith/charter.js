(function () {
  
  /*
<!DOCTYPE html>
<html>
  <head>
    <title>d3stuff</title>
    <style>
      #graph {
        background-image:url('court-lines.gif');
        width:470px;
        height:300px;
      }
    </style>
  </head>
  <body>

    <div id="graph"></div>

    <script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>
    <script type="text/javascript" src="smartmatch.js"></script>
    <script type="text/javascript" src="quarry.js"></script>
    <script type="text/javascript" src="data.js"></script>
    <script type="text/javascript" src="app.js"></script>
  </body>
</html>
  */

  var root = this

    , origin = {x: 25, y: 29}

    , graphWidth = 470
    , graphHeight = 300

    , paddingLeft = 7 // right of left out of bounds marker
    , paddingBottom = 11 // top of bottom court line
    
    , pxPerFt = 8.5

    , data = Q(shotData).findAll({
        is_fast_break: false,
        //assist: null,
        shooter: /LeBron/,
        //tags: 'alley oop'
        //team: 'OKC',
        //oppt: 'LAL',
      })
  ;

  var graph = d3.select('#graph')
    .append('svg:svg')
      .attr('width', graphWidth)
      .attr('height', graphHeight)
  ;

  graph.selectAll('circle')
    .data(data)
      .enter()
      .append('circle')
        .attr('r', 5)
        .attr('cx', function (d) {
           return pxPerFt*(origin.x - d.x) + paddingLeft;
         })
        .attr('cy', function (d) {
           return pxPerFt*(origin.y - d.y);
         })
        .attr('fill', function (d) {
           return d.make ? 'green' : 'red';
         })
        .attr('opacity', function (d) {
           return d.make && d['point_value'] === 3 ? .6 : .4;
         })
  ;

}).call(this);
