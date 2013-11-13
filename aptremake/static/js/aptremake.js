function render(design) {

    console.log("Design being rendered:", design)
  
    // Constants:
    var NUM_TICKS = 5;
    var POINT_SIZE = 5;
    var MARGIN = {TOP: 40, RIGHT: 30, BOTTOM: 50, LEFT: 70}, // Is this necessary?
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

    points = svg.selectAll(".dots")
        .data(design.data)
        .enter().append("circle")
        .style("fill", "#BBB")
        .style("stroke", "black")
        .attr("r", POINT_SIZE)
        .attr("mark", function(d) { return d.mark; });

    if (design.haxis) {
    
        var x = d3.scale.linear()
            .range([0, WIDTH]);
        x.domain(d3.extent(design.data, function(d) { return d.hpos; })).nice();
        
        if (design.hpos_ordinal || design.hpos_nominal) {
            var x = d3.scale.ordinal()
                .rangePoints([0, WIDTH], 1)
                .domain(_.uniq(_.map(design.data, 
                                function(d) { return d.hpos } )));
        }

        
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(NUM_TICKS); // FIXME: Maybe this shouldn't be hard-coded.
     
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + HEIGHT + ")")
            .call(xAxis)
           .append("text")
            .attr("class", "label")
            .attr("x", WIDTH)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text(design.hlabel);

        points.attr("cx", function(d) { return x(d.hpos); });

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

        points.attr("cx", function(d) { return x(Math.random()); });
    }
    
    if (design.vaxis) {
        
        var y = d3.scale.linear()
            .range([HEIGHT, 0]);
        
        y.domain(d3.extent(design.data, function(d) { return d.vpos; })).nice();
        
        if (design.vpos_ordinal || design.vpos_nominal) {
            var y = d3.scale.ordinal()
                .rangePoints([HEIGHT, 0], 1)
                .domain(_.uniq(_.map(design.data, 
                                function(d) { return d.vpos } )));
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
        
        points.attr("cy", function(d) { return y(d.vpos); });

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

        //d3.selectAll(".axis path")
        //    .style("stroke", "white");

        points.attr("cy", function(d) { return y(Math.random()); });
    
    }
    
    if (design.color) {

        var color = d3.scale.category10();

        if (design.color_ordinal) {
            var colordomain = _.uniq(_.map(design.data, 
                                    function(d) { return d.color } ));
            console.log(colordomain);

            var color = d3.scale.ordinal()
                .domain(colordomain)
                .range(colorbrewer.RdBu[colordomain.length]);
        }

        points.style("stroke", "black")
            .style("fill", function(d) { return color(d.color); });

        var legend = svg.selectAll(".legend")
            .data(color.domain())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        legend.append("rect")
            .attr("x", WIDTH + 100)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color)
            .style("stroke", "black");

        legend.append("text")
            .attr("x", WIDTH + 94)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function(d) { return d; });

    }

}
