

apt = {


  render: function(plot, svgPlotID, divCaptionID) {
    console.log("Rendering:", plot);
     
    // Important constants
    var WIDTH = 500,
        LEGEND_SPACE = 150,
        HEIGHT = 500,
        NUM_TICKS = 5,
        BORDER_PADDING = 10,  
        VERTICAL_TICK_AXIS_PADDING = 40, 
        HORIZONTAL_TICK_AXIS_PADDING = 40, 
        TOP_MARGIN = 5, 
        RIGHT_MARGIN = 40, 
        MIN_SUBPLOT_HEIGHT = 250, 
        MIN_SUBPLOT_WIDTH = 250, 
        LABEL_OFFSET = 8,
        MAX_NUM_POINTS_FOR_LABELING = 40;

    function writeCaption(string, div) {
      div.classed("caption", true)
        .append("p")
        .html("<br /><b>Caption: </b>" + string);
    }


    function drawColor(outerContainer, margin) {
      if (plot.hasColor) {
        var color = d3.scale.category10(),
            width = +outerContainer.attr("width") - LEGEND_SPACE;

        if (plot.colorOrdinal) {
          var colordomain = _.uniq(_.map(plot.data, function(d) { 
            return d[plot.color]
          }));
          colordomain = _.sortBy(colordomain, function(d) { 
            return plot.cordering[d] 
          });

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
          .attr("transform", function(d, i) { 
            return "translate(0," + (i*20 + margin.top) + ")"; 
          });
        legend.append("rect")
          .attr("x", width + 80)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color)
        legendText = legend.append("text")
          .attr("x", width + 74)
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
        r = Math.random();
        marks.selectAll(subplot.markTag)
          .attr(locationAttr, function(d) {
            d.r = Math.random();
            return s(d.r); 
          });
        marks.selectAll("text")
          .attr("y", function(d) { return s(d.r) + LABEL_OFFSET; });
      } else if (subplot.markType == "bar") {
        // TODO: This shouldn't happen. Raise an error if it does.
      }
      var axisSelector = _.map(className.split(" "), function (d) {
        return "." + d;
      }).join("");
      d3.selectAll(axisSelector)
        .selectAll("path")
        .style("display", "none");
    }


    function wrapAxisLabel(label, displayedLength, desiredLength) {
      if (desiredLength < 0) {
        throw "Cannot wrap label: negative space input for axis label.";
      } 
      if (displayedLength < 0) {
        throw "Cannot wrap label: negative display length input for label.";
      }

      var wrappedLabel = [];
      var charLength = displayedLength / label.length; 
      var charsPerLine = Math.floor(desiredLength / charLength);
      
      var i = 0;
      var j = 0;
      while (i < label.length) {
        j += 1;
        if (j > 10) {
          break;
        }
        //console.log("i is ", i); 
        var nextSegment = label.slice(i, i + charsPerLine);
        //console.log("next segment is ", nextSegment);
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


    function createScale(axisData, rangeStart, rangeEnd, rangePoints, bars) {

      var s = d3.scale.linear()
        .range([rangeStart, rangeEnd]),
          rangeWidth = 1.0;
      if (bars && !rangePoints) {
        rangeWidth = 0.1;
      }

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
        if (rangePoints) { 
        // if (subplot.markType == "point"
          // TODO: Figure out why passing in range function doesn't work.
          s = d3.scale.ordinal()
            .rangePoints([rangeStart, rangeEnd], rangeWidth)
            .domain(scaleDomain);
        }
        else {
          s = d3.scale.ordinal()
            .rangeRoundBands([rangeStart, rangeEnd], rangeWidth)
            .domain(scaleDomain);
        }
      }
      return s;
    }


    function drawVerticalAxis(marks, subplot, subplotContainer, leftmost, margin) {     
      var width = +subplotContainer.attr("width") - margin.left - margin.right,
          height = +subplotContainer.attr("height") - margin.top - margin.bottom,
          bars = subplot.markType == "bar";

      if (subplot.hasVaxis) {
        var axisLabelHeight = displayedAxisLabelHeight(subplot.vaxis.label, height, subplotContainer);
        var y = createScale(subplot.vaxis, height, 0, true, bars),
            offset = {
              "horizontal": -1*(margin.left - axisLabelHeight),
              "vertical": (height/2)
            };

        createAxis(subplot.vaxis, y, "left", subplotContainer, "y axis", 0, false);

        if (leftmost) {
          wrapAndApplyAxisLabel(height - margin.top, subplotContainer, offset, "rotate(-90)", subplot.vaxis.label, false);
        }  
        
        if (!bars) {
          marks.selectAll(subplot.markTag)
            .attr("cy", function(d) { return y(d[subplot.vaxis.pos]); });
          marks.selectAll("text")
            .attr("y", function(d) { return y(d[subplot.vaxis.pos]) + LABEL_OFFSET; });
        } else if (subplot.markType == "bar") {
          marks.selectAll(subplot.markTag)
            .attr("y", function(d) { return y(d[subplot.vaxis.pos]); })
            .attr("height", function(d) { return height - y(d[subplot.vaxis.pos]); });
        }

      } else {
        drawInvisibleAxis(marks, subplot, subplotContainer, height/4, height, height - height/4, "left", "y axis", 0, "cy");
      }
    }


    function drawHorizontalAxis(marks, subplot, subplotContainer, bottommost, margin) {
      var width = +subplotContainer.attr("width") - margin.left - margin.right,
          height = +subplotContainer.attr("height") - margin.top - margin.bottom,
          rotate = !subplot.haxis.quantitative,
          bars = subplot.markType == "bar";

      if (subplot.hasHaxis) {

        var axisLabelHeight = displayedAxisLabelHeight(subplot.haxis.label, width, subplotContainer);

        var x = createScale(subplot.haxis, 0, width, false, bars),
            offset = {
              "horizontal": width/2,
              "vertical": height + margin.bottom - axisLabelHeight
            };

        createAxis(subplot.haxis, x, "bottom", subplotContainer, "x axis", height, rotate);
        if (bottommost) {
          wrapAndApplyAxisLabel(width, subplotContainer, offset, "", subplot.haxis.label, true);
        }
        
        if (!bars) {
          marks.selectAll(subplot.markTag)
            .attr("cx", function(d) { return x(d[subplot.haxis.pos]); });
          marks.selectAll("text")
            .attr("x", function(d) { return x(d[subplot.haxis.pos]) + LABEL_OFFSET; });
        }
        else if (subplot.markType == "bar") {
          // TODO: FIXME: rangeBand only works if x is ordinal, insert safety check
          marks.selectAll(subplot.markTag)
            .attr("x", function(d) { return x(d[subplot.haxis.pos]); })
            .attr("width", x.rangeBand());
        }

      } else {
        drawInvisibleAxis(marks, subplot, subplotContainer, width/4, 0, width/4, "bottom", "x axis", height, "cx");
      }
    }


    function drawMarks(subplot, subplotContainer) {
      // TODO: FIXME: `id` is currently hard-coded and should not be.
      var groups = subplotContainer.selectAll("g")
        .data(plot.data)
        .enter().append("g");
      var marks = groups.append(subplot.markTag)
        .attr("class", function(d) { return subplot.markClass + " mark"; })
        .attr("id", function(d) { return "mark_" + d.APTREMAKEID; }) // FIXME
        .attr("cx", function(d) { return d[subplot.haxis.pos]; })
        .attr("cy", function(d) { return d[subplot.vaxis.pos]; });
      if (subplot.markType == "point") {
        marks.attr("r", 5);
        if (plot.data.length < MAX_NUM_POINTS_FOR_LABELING) {
          groups.append("text")
              .text(function(d) {
                if (subplot.markCoding) {
                  return subplot.markCoding[d[subplot.markLabel]]; 
                } else {
                  return d[subplot.markLabel];
                }
              });
        }
      }
      return groups;
    }


    function helpRender(subplot, subplotContainerID, leftmost, bottommost, margin) {

      var subplotContainer = d3.select("#" + subplotContainerID),
          marks = drawMarks(subplot, subplotContainer);

      console.log("Subplot", subplot);
      // TODO: Make bottommost, leftmost into subplot attributes?
      drawHorizontalAxis(marks, subplot, subplotContainer, bottommost, margin);
      drawVerticalAxis(marks, subplot, subplotContainer, leftmost, margin);
    }


    function displayedAxisLabelHeight(label, plotLength, svgContainer) {
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
        return displayedAxisLabelHeight(label, plotLength, svgContainer);
      }));
      return _.max([0, maxAxisLabelHeight]);
    }


    function displayedTickLabelLength(aContainer, aString, angleInDegrees) {
      var text = aContainer.append("text")
        .text(aString);
      // FIXME: There has to be a less hacky way to do this.
      var textDisplayLength = text[0][0].getBBox().width;
      if (angleInDegrees > 0.0) {
        var angleInRadians = angleInDegrees*Math.PI/180;
        var textDisplayLength = textDisplayLength*Math.sin(angleInRadians);
      }
      text.remove();
      return textDisplayLength;
    }


    function isNumber(n) {
      return !isNaN(parseFloat(n)) && isFinite(n);
    }


    function maxTickLabelLength(hasAxis, axis, container, angle) {
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
      var maxTickLabelLenth = _.max(_.map(labels, function(label) {
        var tickLabel = (label +  "");
        if (isNumber(label)) {
          // This seems to reasonably match d3's axis formatting.
          tickLabel = d3.format(".2r")(label); 
        } 
        displayedLength = displayedTickLabelLength(container, tickLabel, angle);
        return displayedLength;
      }));
      return _.max([0, maxTickLabelLenth]);
    }
    

    function computeMarginNeeded(axis, dimension, outer, tickAngle, padding) {
      var hasAxis = "has" + axis[0].toUpperCase() + axis.slice(1,axis.length);
      var tickLabelSpace = maxTickLabelLength(hasAxis, axis, outer, tickAngle);
      var axisLabelSpace = maxAxisLabelHeight(hasAxis, axis, dimension, outer);
      var spaceNeeded = tickLabelSpace + padding + axisLabelSpace;
      return spaceNeeded;
    }


    function setUpInnerSubplots(outer) {

      var inners = outer.selectAll("svg")
            .data(plot.subplots)
            .enter().append("svg").append("g"),

          plotWidth = _.max([MIN_SUBPLOT_WIDTH, Math.floor(WIDTH/plot.ncols)]),
          plotHeight = _.max([MIN_SUBPLOT_HEIGHT, Math.floor(HEIGHT/plot.nrows)]),
          
          bottomMargin = computeMarginNeeded("haxis", plotWidth, outer, 45.0, HORIZONTAL_TICK_AXIS_PADDING),
          leftMargin = computeMarginNeeded("vaxis", plotHeight, outer, 0.0, VERTICAL_TICK_AXIS_PADDING),
          
          margin = { // TODO: have special margins for sidemost plots
            top: TOP_MARGIN,
            bottom: bottomMargin,
            left: leftMargin,
            right: RIGHT_MARGIN 
          },

        containerHeight = plotHeight + margin.top + margin.bottom,
        containerWidth = plotWidth + margin.left + margin.right;

      outer.attr("width", containerWidth*plot.ncols + LEGEND_SPACE)
        .attr("height", containerHeight*plot.nrows);

      inners.attr("width", containerWidth)
        .attr("height", containerHeight)
        .attr("id", function(d) {
            return "subplotArea_" + d.ridx + "_" + d.cidx;
          })
        .attr("transform", function(d) { 
            var left = d.cidx*containerWidth + margin.left,
                top = d.ridx*containerHeight + margin.top;
            return "translate(" + left + "," + top + ")"; 
          })
        .each(function(d) { 
            var leftmost = (d.cidx == 0),
                bottommost = ((d.ridx+1) == plot.nrows);
            helpRender(d, $(this).attr("id"), leftmost, bottommost, margin); 
          });

      return margin;
    }
    

    function setUpOuterContainer(outer) {
      outer.attr("width", WIDTH + LEGEND_SPACE)
        .attr("height", HEIGHT);
      return outer;
    }

    // Run
    var outerContainer = d3.select(svgPlotID),
        captionContainer = d3.select(divCaptionID),
        margin = setUpInnerSubplots(outerContainer);   
    drawColor(outerContainer, margin);
    if (plot.caption) {
      writeCaption(plot.caption, captionContainer);
    }
    //return outerContainer;

  }
}
