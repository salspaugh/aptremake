function render(plot) {
  
  console.log("Rendering:", plot);
   
  // Important constants:
  var MARGIN = {TOP: 20, RIGHT: 10, BOTTOM: 70, LEFT: 60};
  var WIDTH = 650; 
  var WIDTH_PLUS = 750;
  var HEIGHT = 650; 
  var NUM_TICKS = 5;
  var LEFTPADDING = -1*(MARGIN.LEFT-10);
  var BOTTOMPADDING = -1*(MARGIN.BOTTOM-10);

  function drawColor(outerContainer) {
    if (plot.hasColor) {
      var color = d3.scale.category10();

      if (plot.color_ordinal) {
        var colordomain = _.uniq(_.map(plot.data, 
                    function(d) { return d[plot.color] } ));
        colordomain = _.sortBy(colordomain, function(d) { return plot.cordering[d] });

        console.log(colordomain);

        var color = d3.scale.ordinal()
          .domain(colordomain)
          .range(colorbrewer.RdBu[colordomain.length]);
      }
      
      d3.selectAll(".mark")
        .style("stroke", "black")
        .style("fill", function(d) { return color(d[plot.color]); });

      var legend = outerContainer.selectAll(".legend")
        .data(color.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + (i*20 + MARGIN.TOP) + ")"; });
      legend.append("rect")
        .attr("x", WIDTH + 80)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color)
        .style("stroke", "black");
      legend.append("text")
        .attr("x", WIDTH + 74)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });
    }
  }

  function drawVerticalAxis(marks, subplot, subplotContainer, width, height, leftmost) {
    if (subplot.hasVaxis) {
      
      var y = d3.scale.linear()
        .range([height, 0]);
      
      // TODO: Figure out why this isn't working like it was before, or if it was:
      //y.domain(d3.extent(plot.data, function(d) { return d[subplot.vpos]; })).nice();
      v = _.map(plot.data, function (d) { return d[subplot.vpos]; });
      y.domain([_.min([0, _.min(v)]), _.max(v)]).nice();
      
      if (subplot.vpos_ordinal || subplot.vpos_nominal) {
        var vdomain = _.uniq(_.map(plot.data, function(d) { return d[subplot.vpos]; } ));
        if (subplot.vpos_ordinal) {
          vdomain = _.sortBy(vdomain, function(d) { return subplot.vordering[d]; });
        }
        var y = d3.scale.ordinal()
          .rangePoints([height, 0], 1)
          .domain(vdomain);
      }

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
       
      subplotContainer.append("g")
        .attr("class", "y axis")
        .call(yAxis);

      if (leftmost) {
        subplotContainer.append("text")
          .attr("text-anchor", "middle")
          .attr("transform", "translate(" + LEFTPADDING + ", " + (height/2) + ") rotate(-90)")
          .text(subplot.vlabel);
      }     
      
      if (subplot.markType == "point") {
        marks.attr("cy", function(d) { return y(d[subplot.vpos]); });
      } else if (subplot.markType == "bar") {
        if (subplot.sideways) {
          marks.attr("y", function(d) { return y(d[subplot.vpos]); })
            .attr("height", y.rangeBand())
        } 
        else {
          marks.attr("y", function(d) { return y(d[subplot.vpos]); })
            .attr("height", function(d) { return height - y(d[subplot.vpos]); });
        }
      }
    } else {
      var invisible_axis_height = height/4;
      var y = d3.scale.linear()
        .range([height, height-invisible_axis_height])
        .domain([0, 1]);
      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(0); // No ticks.
      subplotContainer.append("g")
        .attr("class", "y axis")
        .call(yAxis);
      // TODO: Figure out how to make this extra axis invisible.
      if (subplot.markType == "point") {
        marks.attr("cy", function(d) { return y(Math.random()); });
      } else if (subplot.markType == "bar") {
        // TODO: Check: This shouldn't happen.
      }
    }
  }

  function drawHorizontalAxis(marks, subplot, subplotContainer, width, height, bottommost) {
    if (subplot.hasHaxis) {
      
      var x = d3.scale.linear()
        .range([0, width]);
      
      //x.domain(d3.extent(plot.data, function(d) { return d[subplot.hpos]; })).nice();
      h = _.map(plot.data, function (d) { return d[subplot.hpos]; });
      x.domain([_.min([0, _.min(h)]), _.max(h)]).nice();
      
      if (subplot.hpos_ordinal || subplot.hpos_nominal) {
        var hdomain = _.uniq(_.map(plot.data, function(d) { return d[subplot.hpos] } ));
        if (subplot.hpos_ordinal) {
          hdomain = _.sortBy(hdomain, function(d) { return subplot.hordering[d] });
        }
        var x = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1)
          .domain(hdomain);
      }

      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(NUM_TICKS); 
      
      var xAxisCall = subplotContainer.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
      xAxisCall.selectAll("text")  
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", function(d) { return "rotate(-90)" });
      
      if (bottommost) {
        subplotContainer.append("text")
          .attr("text-anchor", "middle")
          .attr("transform", "translate(" + (width/2) + ", " + (height - BOTTOMPADDING) + ")")
          .text(subplot.hlabel);
      }
      
      if (subplot.markType == "point") {
        marks.attr("cx", function(d) { return x(d[subplot.hpos]); });
      }
      else if (subplot.markType == "bar") {
        if (subplot.sideways) {
          marks.attr("x", function(d) { return x(d[subplot.hpos]); })
            .attr("width", function(d) { return width - x(d[subplot.hpos]); });
        } 
        else { // TODO: FIXME: rangeBand only works if x is ordinal, insert safety check
          marks.attr("x", function(d) { return x(d[subplot.hpos]); })
            .attr("width", x.rangeBand())
        }
      }
    } else {
      var invisible_axis_width = width/4;
      var x = d3.scale.linear()
        .range([0, invisible_axis_width])
        .domain([0, 1]);
      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(0); // No ticks.
      subplotContainer.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
      if (subplot.markType == "point") {
        marks.attr("cx", function(d) { return x(Math.random()); });
      } else if (subplot.markType == "bar") {
        // TODO: Check: This shouldn't happen.
      }
    }
  }

  function drawMarks(subplot, subplotContainer) {
    var marks = subplotContainer.selectAll(subplot.markClass)
      .data(plot.data)
      .enter().append(subplot.markTag)
      .attr("class", function(d) { return subplot.markClass + " mark"; })
      .attr("id", function(d) { return "mark_" + d.APTREMAKEID; })
      .attr("cx", function(d) { return d[subplot.hpos]; })
      .attr("cy", function(d) { return d[subplot.vpos]; });
    if (subplot.markType == "point") {
      marks.attr("r", 5);
    }
    return marks;
  }

  function helpRender(subplot, subplotContainerID, leftmost, bottommost) {

    var subplotContainer = d3.select("#" + subplotContainerID);

    var width = +subplotContainer.attr("width") - MARGIN.LEFT - MARGIN.RIGHT;
    var height = +subplotContainer.attr("height") - MARGIN.TOP - MARGIN.BOTTOM;

    console.log("Subplot", subplot);
    marks = drawMarks(subplot, subplotContainer);
    drawHorizontalAxis(marks, subplot, subplotContainer, width, height, bottommost);
    drawVerticalAxis(marks, subplot, subplotContainer, width, height, leftmost);
  }

  function setUpInnerSubplots(outerContainer) {

    var subplotAreaWidth = Math.floor(WIDTH/plot.ncols);
    var subplotAreaHeight = Math.floor(HEIGHT/plot.nrows);

    var inners = outerContainer.selectAll("svg")
      .data(plot.subplots)
      .enter().append("svg").append("g");

    inners.attr("width", subplotAreaWidth)
      .attr("height", subplotAreaHeight)
      .attr("id", function(d) {
          return "subplotArea_" + d.ridx + "_" + d.cidx;
        })
      .attr("transform", function(d) { 
          var left = d.cidx*subplotAreaWidth + MARGIN.LEFT;
          var top = d.ridx*subplotAreaHeight + MARGIN.TOP;
          return "translate(" + left + "," + top + ")"; 
        })
      .each(function(d) { 
          var leftmost = (d.cidx == 0);
          var bottommost = ((d.ridx+1) == plot.nrows);
          helpRender(d, $(this).attr("id"), leftmost, bottommost); 
        });
  }
  
  function setUpOuterContainer() {

    var outer = d3.select("#presentation");
    outer.attr("width", WIDTH_PLUS)
      .attr("height", HEIGHT);
    return outer;
  }

  // Run:
  var outerContainer = setUpOuterContainer();
  setUpInnerSubplots(outerContainer);
  drawColor(outerContainer);
}

