(function () {

  var root = this

    , origin = {x: 25, y: 29}

    , graphWidth = 470
    , graphHeight = 300

    , paddingLeft = 7 // right of left out of bounds marker
    , paddingBottom = 11 // top of bottom court line

    , pxPerFt = 8.5

    , data = Q(shotData).findAll({
        //is_fast_break: false,
        //assist: null,
        shooter: 'Griffin, Blake',
        //tags: 'alley oop'
        //team: 'MIA',
        //oppt: 'LAL',
      })
  ;

  var hexbin = d3.hexbin()
    .size([graphWidth, graphHeight])
    .radius(pxPerFt)
  ;

  hbpts = hexbin(data);
  console.log('hi');
  this.data = data;

  var color = d3.scale.linear()
    .domain([0, 0.8, 2])
    .range(['rgb(69, 117, 180)', 'rgb(255, 255, 191)', 'rgb(215, 48, 39)'])
    .interpolate(d3.interpolateLab)
  ;


  var maxFreq = d3.max(hbpts, function (d) { return d.length; });

  var radius = d3.scale.sqrt()
    .domain([0, d3.min([50, maxFreq])])
    .range([0, pxPerFt])
  ;




  var svg = d3.select('#graph')
    .append('svg')
      .attr('width', graphWidth)
      .attr('height', graphHeight)
  ;

  svg.append('clipPath')
    .attr('id', 'clip')
    .append('rect')
      .attr('class', 'mesh')
      .attr('width', graphWidth - paddingLeft)
      .attr('height', graphHeight - paddingBottom)
  ;

  svg.append('g')
    .attr('clip-path', 'url(#clip)')
    .selectAll('.hexagon')
      .data(hbpts)
      .enter()
        .append('path')
        .attr('class', 'hexagon')
        .attr('d', function (d) {
           var r = radius(d.length);
           return hexbin.hexagon(r > pxPerFt ? pxPerFt : r);
         })
        .attr('transform', function (d) {
           //var xTrans = pxPerFt*(origin.x - d.x) + paddingLeft
           //  , yTrans = pxPerFt*(origin.y - d.y);
           //return 'translate(' + xTrans + ',' + yTrans + ')';
           return 'translate(' + d.x + ',' + d.y + ')';
         })
        .style('fill', function (d) {
           var pts = d3.sum(d, function (shot) {
             return shot.make ? shot.point_value : 0;
           });
           return color(pts/d.length);
           //return color(d.length);
         })
        .attr('opacity', 0.75)
  ;



}).call(this);
