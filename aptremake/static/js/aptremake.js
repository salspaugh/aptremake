

apt = {


  render: function(plot) {
    console.log("Rendering:", plot);
     
    // Important constants:
    var WIDTH = 650; 
    var WIDTH_PLUS = 750;
    var HEIGHT = 650; 
    var NUM_TICKS = 5;
    var TEXT_PADDING = 20;
    var TICK_AXIS_SPACE = 40;
    var TOP_MARGIN = 10;

    function drawColor(outerContainer, margin) {
      if (plot.hasColor) {
        var color = d3.scale.category10();

        if (plot.colorOrdinal) {
          var colordomain = _.uniq(_.map(plot.data, 
                      function(d) { return d[plot.color] } ));
          colordomain = _.sortBy(colordomain, function(d) { return plot.cordering[d] });

          var color = d3.scale.ordinal()
            .domain(colordomain)
            .range(colorbrewer.RdBu[colordomain.length]);
        }
        
        d3.selectAll(".mark")
          .style("fill", function(d) { return color(d[plot.color]); });

        var legend = outerContainer.selectAll(".legend")
          .data(color.domain())
          .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(0," + (i*20 + margin.top) + ")"; });
        legend.append("rect")
          .attr("x", WIDTH + 80)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color)
        legendText = legend.append("text")
          .attr("x", WIDTH + 74)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end");
        if (plot.colorCoding) {
          legendText.text(function(d) { return plot.colorCoding[d]; });
        } else {
          legendText.text(function(d) { return d; });
        }

      }
    }


    function drawInvisibleAxis(marks, subplot, subplotContainer, axisLength, rangeStart, rangeEnd, orientation, className, translation, locationAttr) {
      // TODO: Figure out how to make this extra axis invisible.
      var invisible_axis_width = axisLength;
      var s = d3.scale.linear()
        .range([rangeStart, rangeEnd])
        .domain([0, 1]);
      var axis = d3.svg.axis()
        .scale(s)
        .orient(orientation)
        .ticks(0); // No ticks.
      subplotContainer.append("g")
        .attr("class", className)
        .attr("transform", "translate(0," + translation + ")")
        .call(axis);
      if (subplot.markType == "point") {
        marks.attr(locationAttr, function(d) { return s(Math.random()); });
      } else if (subplot.markType == "bar") {
        // TODO: This shouldn't happen. Raise an error if it does.
      }
    }


    function wrapAxisLabel(label, displayedLength, desiredLength) {
      var wrappedLabel = [];
      var charLength = displayedLength / label.length; 
      var charsPerLine = Math.floor(desiredLength / charLength);
      
      var i = 0;
      while (i < label.length) {
        var nextSegment = label.slice(i, i + charsPerLine);
        if (i + charsPerLine >= label.length) {
          wrappedLabel.push(nextSegment);
          i += charsPerLine;
          continue;
        }
        var spaceIdx = nextSegment.lastIndexOf(" ");
        if (spaceIdx < 0) {
          var lineToDisplay = label.slice(i, i + charsPerLine - 1) + "-";
          wrappedLabel.push(lineToDisplay);
          i += charsPerLine - 1;
        } else {
          var lineToDisplay = label.slice(i, i + spaceIdx);
          wrappedLabel.push(lineToDisplay);
          i += spaceIdx + 1;
        }
      }
      return wrappedLabel;
    }


    function applyAxisLabel(label, container, offset, rotation) {
      var transformation = "translate("
      if (offset && offset.horizontal && offset.vertical) {
        transformation += offset.horizontal + ", " + offset.vertical 
      } else {
        transformation += "0, 0"
      }
      transformation += ")"
      if (rotation) {
        transformation += (" " + rotation)
      }
      var text = container.append("text")
        .attr("class", "axis label")
        .attr("text-anchor", "middle")
        .attr("transform", transformation)
        .text(label);
      return text;
    }


    function wrapAndApplyAxisLabel(plotLength, container, offset, rotation, label, horizontal) {
      var text = applyAxisLabel(label, container, offset, rotation);

      // FIXME: Find less hacky way to do this.
      var textDisplayLength = text[0][0].getBBox().width; 
      var textDisplayHeight = text[0][0].getBBox().height;

      if (textDisplayLength > plotLength) {
        text.remove(); // Delete the label that's too long.
        wrappedLabel = wrapAxisLabel(label, textDisplayLength, plotLength);
        for (var i = 0; i < wrappedLabel.length; i++) {
          applyAxisLabel(wrappedLabel[i], container, offset, rotation);
          if (horizontal) {
            offset.vertical += textDisplayHeight;
          } else {
            offset.horizontal += textDisplayHeight;
          }
        }
      }
    }


    function createAxis(axisData, axisScale, orientation, subplotContainer, className, translation, rotate) {

      var axis = d3.svg.axis()
        .scale(axisScale)
        .orient(orientation);

      if (axisData.quantitative) {  
        axis.ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
      }

      axisCall = subplotContainer.append("g")
        .attr("class", className)
        .attr("transform", "translate(0," + translation + ")")
        .call(axis);

      if (axisData.coding && (axisData.nominal || axisData.ordinal)) {
        // codedTicks = axis.tickValues(); 
        // NOTE: This only works when tickValues() has already been used to
        // set tick values. Submit pull request to d3?
        codedTicks = [];
        axisCall.selectAll(".tick")
          .selectAll("text")
          .each(function(d) { codedTicks.push(d); });
        labeledTicks = _.map(codedTicks, function(item) { 
          return axisData.coding[item]; 
        });
        axis.tickValues(labeledTicks);
      }
      
      axisCall.call(axis); // This is necessary to reset the axis tick labels.

      if (rotate) {
        axisCall.selectAll("text")  
            .style("text-anchor", "start")
            .attr("dx", ".5em")
            .attr("dy", ".5em") // TODO: FIXME: Why are these hard-coded?
            .attr("transform", function(d) { return "rotate(45)" });
      }

    }


    function createScale(axisData, rangeStart, rangeEnd, usesPoints, rangeWidth) {

      var s = d3.scale.linear()
        .range([rangeStart, rangeEnd]);
      
      // TODO: Figure out why this isn't working like it was before:
      // s.domain(d3.extent(plot.data, function(d) { return d[position]; })).nice();
      positionData = _.map(plot.data, function (d) { 
        return d[axisData.pos]; 
      });
      s.domain([_.min([0, _.min(positionData)]), _.max(positionData)]).nice();
      
      if (axisData.ordinal || axisData.nominal) {
        var scaleDomain = _.uniq(_.map(plot.data, function(d) { 
          return d[axisData.pos]; 
        }));
        if (axisData.ordinal) {
          scaleDomain = _.sortBy(scaleDomain, function(d) { 
            return axisData.ordering[d];
          });
        }
        if (usesPoints) { 
          // TODO: Figure out why passing in range function doesn't work.
          var s = d3.scale.ordinal()
            .rangePoints([rangeStart, rangeEnd], rangeWidth)
            .domain(scaleDomain);
        }
        else {
          var s = d3.scale.ordinal()
            .rangeRoundBands([rangeStart, rangeEnd], rangeWidth)
            .domain(scaleDomain);
        }
      }
      return s;
    }


    function drawVerticalAxis(marks, subplot, subplotContainer, width, height, leftmost, margin) {
      if (subplot.hasVaxis) {

        var y = createScale(subplot.vaxis, height, 0, true, 1);
        createAxis(subplot.vaxis, y, "left", subplotContainer, "y axis", 0, false);

        var offset = {
          "horizontal": -1*margin.left+TEXT_PADDING,
          "vertical": (height/2)
        };
        if (leftmost) {
          wrapAndApplyAxisLabel(height - margin.top, subplotContainer, offset, "rotate(-90)", subplot.vaxis.label, false);
        }  
        
        if (subplot.markType == "point") {
          marks.attr("cy", function(d) { return y(d[subplot.vaxis.pos]); });
        } else if (subplot.markType == "bar") {
          marks.attr("y", function(d) { return y(d[subplot.vaxis.pos]); })
            .attr("height", function(d) { return height - y(d[subplot.vaxis.pos]); });
        }

      } else {
        drawInvisibleAxis(marks, subplot, subplotContainer, height/4, height, height - height/4, "left", "y axis", 0, "cy");
      }
    }


    function drawHorizontalAxis(marks, subplot, subplotContainer, width, height, bottommost, margin) {
      if (subplot.hasHaxis) {
        
        var x = createScale(subplot.haxis, 0, width, false, .1);
        createAxis(subplot.haxis, x, "bottom", subplotContainer, "x axis", height, true);

        var offset = {
          "horizontal": width/2,
          "vertical": height - (-1*margin.bottom+TEXT_PADDING)
        };
        if (bottommost) {
          wrapAndApplyAxisLabel(width, subplotContainer, offset, "", subplot.haxis.label, true);
        }
        
        if (subplot.markType == "point") {
          marks.attr("cx", function(d) { return x(d[subplot.haxis.pos]); });
        }
        else if (subplot.markType == "bar") {
          // TODO: FIXME: rangeBand only works if x is ordinal, insert safety check
          marks.attr("x", function(d) { return x(d[subplot.haxis.pos]); })
            .attr("width", x.rangeBand());
        }

      } else {
        drawInvisibleAxis(marks, subplot, subplotContainer, width/4, 0, width/4, "bottom", "x axis", height, "cx");
      }
    }


    function drawMarks(subplot, subplotContainer) {
      // TODO: FIXME: `id` is currently hard-coded and should not be.
      var marks = subplotContainer.selectAll(subplot.markClass)
        .data(plot.data)
        .enter().append(subplot.markTag)
        .attr("class", function(d) { return subplot.markClass + " mark"; })
        .attr("id", function(d) { return "mark_" + d.APTREMAKEID; }) // FIXME
        .attr("cx", function(d) { return d[subplot.haxis.pos]; })
        .attr("cy", function(d) { return d[subplot.vaxis.pos]; });
      if (subplot.markType == "point") {
        marks.attr("r", 5);
      }
      return marks;
    }


    function helpRender(subplot, subplotContainerID, leftmost, bottommost, margin) {

      var subplotContainer = d3.select("#" + subplotContainerID);

      var plotWidth = +subplotContainer.attr("width") - margin.left - margin.right;
      var plotHeight = +subplotContainer.attr("height") - margin.top - margin.bottom;

      // subplotContainer.append("rect") // FIXME: Remove after debugging
      // .attr("width", plotWidth)
      // .attr("height", plotHeight)
      // .attr("fill", "#99ff66");

      console.log("Subplot", subplot);
      marks = drawMarks(subplot, subplotContainer);
      // TODO: Make bottommost, leftmost, plotWidth and plotHeight into subplot attributes?
      drawHorizontalAxis(marks, subplot, subplotContainer, plotWidth, plotHeight, bottommost, margin);
      drawVerticalAxis(marks, subplot, subplotContainer, plotWidth, plotHeight, leftmost, margin);
    }


    function computeDisplayedAxisLabelHeight(label, plotLength, svgContainer) {
      var text = applyAxisLabel(label, svgContainer, false, "");
      // FIXME: There has to be a less hacky way to do this.
      var textDisplayWidth = text[0][0].getBBox().width;
      var textDisplayHeight = text[0][0].getBBox().height;
      text.remove();
      var wrappedLabel = wrapAxisLabel(label, textDisplayWidth, plotLength);
      return (textDisplayHeight * wrappedLabel.length); 
    }


    function maxAxisLabelHeight(hasAxis, axis, plotLength, svgContainer) {
      var labels = _.map(plot.subplots, function(subplot) {
        if (subplot[hasAxis]) {
          return subplot[axis].label;
        } else {
          return null;
        }
      });
      labels = _.filter(labels, function(d) { return d; });
      var maxAxisLabelHeight = _.max(_.map(labels, function(label) {
        label = label + "";
        return computeDisplayedAxisLabelHeight(label, plotLength, svgContainer);
      }));
      return _.max([0, maxAxisLabelHeight]);
    }


    function computeDisplayedTextLength(aContainer, aString) {
      var text = aContainer.append("text")
        .text(aString);
      // FIXME: There has to be a less hacky way to do this.
      var textDisplayLength = text[0][0].getBBox().width; 
      text.remove();
      return textDisplayLength;
    }


    function maxTickLabelLength(hasAxis, axis, container) {
      var labels = _.flatten(_.map(plot.subplots, function(subplot) { 
        if (subplot[hasAxis]) {
          if (subplot[axis].coding) {
            return _.values(subplot[axis].coding);
          } else {
            return _.map(plot.data, function(d) { 
              return d[subplot[axis].pos];
            });
          }
        }
        return "";
      }));
      labels = _.filter(labels, function(d) { return d; });
      var maxTickLabelLenth = _.max(_.map(labels, function(label) {
        // TODO: FIXME: Temporary hack. Need to get actual tick labels.
        tickLabel = (label + "").split(".")[0]; 
        displayedLength = computeDisplayedTextLength(container, tickLabel);
        return displayedLength;
      }));
      return _.max([0, maxTickLabelLenth]);
    }


    function computeMargins(svgContainer, subplotWidths, subplotHeights) {

      var maxHaxesTickLabelLength = maxTickLabelLength("hasHaxis", "haxis", svgContainer);
      var haxisLabelHeight = maxAxisLabelHeight("hasHaxis", "haxis", subplotWidths, svgContainer);
      var bottom = maxHaxesTickLabelLength + TICK_AXIS_SPACE + haxisLabelHeight;

      var maxVaxesTickLabelLength = maxTickLabelLength("hasVaxis", "vaxis", svgContainer);
      var vaxisLabelHeight = maxAxisLabelHeight("hasVaxis", "vaxis", subplotHeights - TOP_MARGIN - bottom, svgContainer);
      var left = maxVaxesTickLabelLength + TICK_AXIS_SPACE + vaxisLabelHeight;

      // TODO: Automatically set right margin to account for color legend label length.
      return {top: TOP_MARGIN, right: 40, bottom: bottom, left: left};
    }


    function setUpInnerSubplots(outerContainer) {

      var subplotAreaWidth = Math.floor(WIDTH/plot.ncols);
      var subplotAreaHeight = Math.floor(HEIGHT/plot.nrows);

      var inners = outerContainer.selectAll("svg")
        .data(plot.subplots)
        .enter().append("svg").append("g");

      var margin = computeMargins(outerContainer, subplotAreaWidth, subplotAreaHeight);

      inners.attr("width", subplotAreaWidth)
        .attr("height", subplotAreaHeight)
        .attr("id", function(d) {
            return "subplotArea_" + d.ridx + "_" + d.cidx;
          })
        .attr("transform", function(d) { 
            var left = d.cidx*subplotAreaWidth + margin.left;
            var top = d.ridx*subplotAreaHeight + margin.top;
            return "translate(" + left + "," + top + ")"; 
          })
        .each(function(d) { 
            var leftmost = (d.cidx == 0);
            var bottommost = ((d.ridx+1) == plot.nrows);
            helpRender(d, $(this).attr("id"), leftmost, bottommost, margin); 
          });

      return margin;
    }
    

    function setUpOuterContainer() {

      var outer = d3.select("#presentation");
      outer.attr("width", WIDTH_PLUS)
        .attr("height", HEIGHT);

      // outer.append("rect") // FIXME: Remove after debugging
      //   .attr("width", WIDTH)
      //   .attr("height", HEIGHT)
      //   .attr("fill", "#acb1d3");
      
      return outer;
    }

    // Run:
    var outerContainer = setUpOuterContainer();
    var margin = setUpInnerSubplots(outerContainer);
    drawColor(outerContainer, margin);
  }
}
