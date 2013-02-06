(function () {

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
