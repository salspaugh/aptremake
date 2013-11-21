function render(design) {

    console.log("Design being rendered:", design)
  
    // Constants:
    var NUM_TICKS = 5;
    var POINT_SIZE = 5;
    var MARGIN = {TOP: 40, RIGHT: 50, BOTTOM: 90, LEFT: 70}, // Is this necessary?
        WIDTH = 400 - MARGIN.LEFT - MARGIN.RIGHT,  // Such things appear at the top
        WIDTH_PLUS = WIDTH + 500;
        HEIGHT = 400 - MARGIN.TOP - MARGIN.BOTTOM; // of most d3 examples.
    var INVISIBLE_AXIS_HEIGHT = HEIGHT/4;
    var INVISIBLE_AXIS_WIDTH = WIDTH/4;
      
    // Set up the presentation space:
    svg = d3.select("#presentation")
        .attr("width", WIDTH_PLUS)
        .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
       .append("g")
        .attr("transform", "translate(" + MARGIN.LEFT + "," + MARGIN.TOP + ")");

    if (design.marktype == "dot") {
        dots = svg.selectAll(".dot") // TODO: Figure out if I should put "var" here.
            .data(design.data)
            .enter().append("circle")
            .style("fill", "#BBB")
            .style("stroke", "black")
            .attr("r", POINT_SIZE)
            .attr("mark", function(d) { return d.mark; });
    }
    else if (design.marktype == "bar") {
        bars = svg.selectAll(".bar")
            .data(design.data)
            .enter().append("rect")
            .attr("class", "bar")
            .style("fill", "#BBB")
            .style("stroke", "black");
    }

    if (design.haxis) {
    
        var x = d3.scale.linear()
            .range([0, WIDTH]);
        x.domain(d3.extent(design.data, function(d) { return d.hpos; })).nice();
        
        if (design.hpos_ordinal || design.hpos_nominal) {

            var hdomain = _.uniq(_.map(design.data, 
                                function(d) { return d.hpos } ));
            if (design.hpos_ordinal) {
                hdomain = _.sortBy(hdomain, function(d) { return design.hordering[d] });
            }
            var x = d3.scale.ordinal()
                //.rangePoints([0, WIDTH], 1)
                .rangeRoundBands([0, WIDTH], .1)
                .domain(hdomain);
        }

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
     
        xAxisCall = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + HEIGHT + ")")
            .call(xAxis);
        xAxisCall.selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) { return "rotate(-90)" });
        xAxisCall.append("text")
            .attr("class", "label")
            .attr("x", WIDTH)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text(design.hlabel);
        
        if (design.marktype == "dot") {
            dots.attr("cx", function(d) { return x(d.hpos); });
        }
        else if (design.marktype == "bar") {
            if (design.sideways) {
                bars.attr("x", function(d) { return x(d.hpos); })
                    .attr("width", function(d) { return WIDTH - x(d.hpos); });
            } 
            else {
                bars.attr("x", function(d) { return x(d.hpos); })
                    .attr("width", x.rangeBand())
            }
        }
    } else {
        
        var x = d3.scale.linear()
            .range([0, INVISIBLE_AXIS_WIDTH])
            .domain([0, 1]);
        
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(0); // No ticks.
     
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + HEIGHT + ")")
            .call(xAxis);

        if (design.marktype == "dot") {
            dots.attr("cx", function(d) { return x(Math.random()); });
        } else if (design.marktype == "bar") {
            // TODO: Check: This shouldn't happen.
        }
    }
    
    if (design.vaxis) {
        
        var y = d3.scale.linear()
            .range([HEIGHT, 0]);
        
        y.domain(d3.extent(design.data, function(d) { return d.vpos; })).nice();
        
        if (design.vpos_ordinal || design.vpos_nominal) {

            var vdomain = _.uniq(_.map(design.data, 
                                function(d) { return d.vpos } ));
            if (design.vpos_ordinal) {
                vdomain = _.sortBy(vdomain, function(d) { return design.vordering[d] });
            }
            var y = d3.scale.ordinal()
                .rangePoints([HEIGHT, 0], 1)
                .domain(vdomain);
        }

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
       
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
           .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text(design.vlabel)
        
        if (design.marktype == "dot") {
            dots.attr("cy", function(d) { return y(d.vpos); });
        } else if (design.marktype == "bar") {
            if (design.sideways) {
                bars.attr("y", function(d) { return y(d.vpos); })
                    .attr("height", y.rangeBand())
            } 
            else {
                bars.attr("y", function(d) { return y(d.vpos); })
                    .attr("height", function(d) { return HEIGHT - y(d.vpos); });
            }
        }
    } else {
        
        var y = d3.scale.linear()
            .range([HEIGHT, HEIGHT-INVISIBLE_AXIS_HEIGHT])
            .domain([0, 1]);

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(0); // No ticks.

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        // TODO: Figure out how to make this extra axis invisible.
        //d3.selectAll(".axis path")
        //    .style("stroke", "white");
        if (design.marktype == "dot") {
            dots.attr("cy", function(d) { return y(Math.random()); });
        } else if (design.marktype == "bar") {
            // TODO: Check: This shouldn't happen.
        }
    
    }
    
    if (design.color) {

        var color = d3.scale.category10();

        if (design.color_ordinal) {
            var colordomain = _.uniq(_.map(design.data, 
                                    function(d) { return d.color } ));
            colordomain = _.sortBy(colordomain, function(d) { return design.colorordering[d] });

            var color = d3.scale.ordinal()
                .domain(colordomain)
                .range(colorbrewer.RdBu[colordomain.length]);
        }
        if (design.marktype == "dot") {
            dots.style("stroke", "black")
                .style("fill", function(d) { return color(d.color); });
        } else if (design.marktype == "bar") {
            bars.style("stroke", "black")
                .style("fill", function(d) { return color(d.color); });
        }

        var legend = svg.selectAll(".legend")
            .data(color.domain())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        legend.append("rect")
            .attr("x", WIDTH + 90) // TODO: Make distance from plot dependent on data.
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color)
            .style("stroke", "black");

        legend.append("text")
            .attr("x", WIDTH + 84)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function(d) { return d; });

    }

}
