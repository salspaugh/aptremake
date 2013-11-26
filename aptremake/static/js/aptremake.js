function render(plot) {
  
  console.log("Rendering:", plot);
   
  // Important constants:
  var MARGIN = {TOP: 20, RIGHT: 10, BOTTOM: 70, LEFT: 50};
  var WIDTH = 650; 
  var WIDTH_PLUS = 750;
  var HEIGHT = 650; 
  var NUM_TICKS = 5;

  function drawColor(outerContainer) {
    if (plot.hasColor) {
      var color = d3.scale.category10();

      if (plot.color_ordinal) {
        var colordomain = _.uniq(_.map(plot.data, 
                    function(d) { return d.color } ));
        colordomain = _.sortBy(colordomain, function(d) { return plot.cordering[d] });

        var color = d3.scale.ordinal()
          .domain(colordomain)
          .range(colorbrewer.RdBu[colordomain.length]);
      }
      
      d3.selectAll(".mark")
        .style("stroke", "black")
        .style("fill", function(d) { return color(d[plot.color]); });

      console.log(color.domain());

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

  function drawVerticalAxis(marks, subplot, subplotContainer, width, height) {
    if (subplot.hasVaxis) {
      
      var y = d3.scale.linear()
        .range([height, 0]);
      
      y.domain(d3.extent(plot.data, function(d) { return +d[subplot.vpos]; })).nice();
      
      if (subplot.vpos_ordinal || subplot.vpos_nominal) {
        var vdomain = _.uniq(_.map(plot.data, function(d) { return +d[subplot.vpos]; } ));
        if (subplot.vpos_ordinal) {
          vdomain = _.sortBy(vdomain, function(d) { return subplot.vordering[d]; });
        }
        var y = d3.scale.ordinal()
          .rangepoints([height, 0], 1)
          .domain(vdomain);
      }

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
       
      subplotContainer.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(subplot.vlabel)
      
      if (subplot.marktype == "point") {
        marks.attr("cy", function(d) { return y(+d[subplot.vpos]); });
      } else if (subplot.marktype == "bar") {
        if (subplot.sideways) {
          marks.attr("y", function(d) { return y(+d[subplot.vpos]); })
            .attr("height", y.rangeBand())
        } 
        else {
          marks.attr("y", function(d) { return y(+d[subplot.vpos]); })
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
      if (subplot.marktype == "point") {
        marks.attr("cy", function(d) { return y(Math.random()); });
      } else if (subplot.marktype == "bar") {
        // TODO: Check: This shouldn't happen.
      }
    }
  }

  function drawHorizontalAxis(marks, subplot, subplotContainer, width, height) {
    if (subplot.hasHaxis) {
      
      var x = d3.scale.linear()
        .range([0, width]);
      x.domain(d3.extent(plot.data, function(d) { return +d[subplot.hpos]; })).nice();
      
      if (subplot.hpos_ordinal || subplot.hpos_nominal) {
        var hdomain = _.uniq(_.map(plot.data, function(d) { return +d[subplot.hpos] } ));
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
      xAxisCall.append("text")
        .attr("class", "label")
        .attr("x", width)
        .attr("y", -6)
        .style("text-anchor", "end")
        .text(subplot.hlabel);
      
      if (subplot.marktype == "point") {
        marks.attr("cx", function(d) { return x(+d[subplot.hpos]); });
      }
      else if (subplot.marktype == "bar") {
        if (subplot.sideways) {
          marks.attr("x", function(d) { return x(+d[subplot.hpos]); })
            .attr("width", function(d) { return width - x(+d[subplot.hpos]); });
        } 
        else {
          marks.attr("x", function(d) { return x(+d[subplot.hpos]); })
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
      if (subplot.marktype == "point") {
        marks.attr("cx", function(d) { return x(Math.random()); });
      } else if (subplot.marktype == "bar") {
        // TODO: Check: This shouldn't happen.
      }
    }
  }

  function drawMarks(subplot, subplotContainer) {
    var marks = subplotContainer.selectAll(subplot.markclass)
      .data(plot.data)
      .enter().append(subplot.marktag)
      .attr("class", function(d) { return subplot.markclass + " mark"; })
      .attr("id", function(d) { return "mark_" + d.id; })
      .attr("cx", function(d) { return +d[subplot.hpos]; })
      .attr("cy", function(d) { return +d[subplot.vpos]; });
    if (subplot.marktype == "point") {
      marks.attr("r", 5);
    }
    return marks;
  }

  function helpRender(subplot, subplotContainerID) {

    var subplotContainer = d3.select("#" + subplotContainerID);

    var width = +subplotContainer.attr("width") - MARGIN.LEFT - MARGIN.RIGHT;
    var height = +subplotContainer.attr("height") - MARGIN.TOP - MARGIN.BOTTOM;

    subplotContainer.append("rect") // FIXME: Remove after debugging
      .attr("width", width)
      .attr("height", height)
      .attr("fill", "pink");

    console.log("Subplot", subplot);
    marks = drawMarks(subplot, subplotContainer);
    drawHorizontalAxis(marks, subplot, subplotContainer, width, height);
    drawVerticalAxis(marks, subplot, subplotContainer, width, height);
  }

  function setUpInnerSubplots(outerContainer) {

    var subplotAreaWidth = Math.floor(WIDTH/plot.numcols);
    var subplotAreaHeight = Math.floor(HEIGHT/plot.numrows);

    var inners = outerContainer.selectAll("svg")
      .data(plot.subplots)
      .enter().append("svg").append("g");

    inners.attr("width", subplotAreaWidth)
      .attr("height", subplotAreaHeight)
      .attr("id", function(d) {
        return "subplotArea_" + d.rowidx + "_" + d.colidx;
        })
      .attr("transform", function(d) { 
        var left = d.colidx*subplotAreaWidth + MARGIN.LEFT;
        var top = d.rowidx*subplotAreaHeight + MARGIN.TOP;
        return "translate(" + left + "," + top + ")"; 
        })
      .each(function(d) { helpRender(d, $(this).attr("id")) });
  }
  
  function setUpOuterContainer() {

    var outer = d3.select("#presentation");
    outer.attr("width", WIDTH_PLUS)
      .attr("height", HEIGHT);
    outer.append("rect") // FIXME: Remove after debugging
      .attr("width", WIDTH)
      .attr("height", HEIGHT)
      .attr("fill", "#acb1d3");
    return outer;
  }


  // Run:
  var outerContainer = setUpOuterContainer();
  setUpInnerSubplots(outerContainer);
  drawColor(outerContainer);
}

