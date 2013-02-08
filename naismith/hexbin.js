(function () {

  var d3_hexbinAngles = d3.range(0, 2*Math.PI, Math.PI/3)
//    , d3_hexbinX = function (d) { return d[0]; }
//    , d3_hexbinY = function (d) { return d[1]; }
    , pxPerFt = 8.5
    , origin = {x: 25, y: 29}
    , paddingLeft = 7
    , d3_hexbinX = function (d) {
        return pxPerFt*(origin.x - d.x) + paddingLeft;
      }
    , d3_hexbinY = function (d) {
        return pxPerFt*(origin.y - d.y);
      }
  ;



  d3.hexbin = function () {

    var width = 1
      , height = 1
      , r
      , x = d3_hexbinX
      , y = d3_hexbinY
      , dx
      , dy
    ;



    function hexbin(points) {

      var binsById = {}
        , bin

        , py
        , pj
        , px
        , pi

        , i
        , n = points.length
        , point

        , py1
        , px1
        , pi2
        , pj2
        , pix2
        , py2

        , id
        , bin
      ;

      for (i = 0; i < n; i++) {
        point = points[i]
        py = y.call(hexbin, point, i)/dy
        pj = Math.round(py)
        px = x.call(hexbin, point, i)/dx - (pj & 1 ? 0.5 : 0)
        pi = Math.round(px)
        py1 = py - pj

        if (3*Math.abs(py1) > 1) {
          pix1 = px - pi;
          pi2 = pi + (px < pi ? -1 : 1)/2;
          pj2 = pj + (py < pj ? -1 : 1);
          px2 = px - pi2;
          py2 = py - pj2;
          if (px1*px1 + py1*py1 > px2*px2 + py2*py2) {
            pi = pi2 + (pj & 1 ? 1 : -1)/2;
            pj = pj2;
          }
        }

        id = pi + '-' + pj;
        bin = binsById[id];

        if (bin) {
          bin.push(point);
        } else {
          bin = [point];
          binsById[id] = bin
          bin.x = dx*(pi + (pj & 1 ? 1/2 : 0));
          bin.y = dy*pj;
        }
      }

      return d3.values(binsById)

    } // hexbin



    function hexagon(radius) {

      var x0 = 0
        , y0 = 0
      ;

      return d3_hexbinAngles.map(function (angle) {
        var x1 = radius*Math.sin(angle)
          , y1 = -radius*Math.cos(angle)
          , dx = x1 - x0
          , dy = y1 - y0;
        x0 = x1;
        y0 = y1;
        return [dx, dy];
      });

    } // hexagon



    hexbin.x = function (_) {
      if (!arguments.length) {
        return x;
      } else {
        x = _;
        return hexbin;
      }
    };

    hexbin.y = function (_) {
      if (!arguments.length) {
        return y;
      } else {
        y = _;
        return hexbin;
      }
    };

    hexbin.hexagon = function (radius) {
      if (arguments.length < 1) {
        radius = r;
      }
      return 'm' + hexagon(radius).join('l') + 'z';
    };

    hexbin.mesh = function () {
      var path = new Array()
        , mesh = hexagon(r).slice(0, 4).join('l')
        , x
        , y
        , odd
      ;
      for (y = 0, odd = false; y < height + r; y += dy, odd = !odd) {
        for (x = odd ? dx/2 : 0; x < width; x += dx) {
          path.push('M', x, ',', y, 'm', mesh);
        }
      }
      return path.join('');
    };

    hexbin.size = function (_) {
      if (!arguments.length) {
        return [width, height];
      } else {
        width = +_[0];
        height = +_[1];
        return hexbin;
      }
    };

    hexbin.radius = function (_) {
      if (!arguments.length) {
        return r;
      } else {
        r = +_;
        dx = 2*r*Math.sin(Math.PI/3);
        dy = 1.5*r;
        return hexbin;
      }
    };

    return hexbin.radius(1);

  }; // d3.hexbin



}).call(this)
