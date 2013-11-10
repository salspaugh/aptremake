function render(design) {

    // Is the following really necessary?
    // It appears at the top of most d3 examples.
    var margin = {top: 10, right: 30, bottom: 30, left: 30},
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
        
    svg = d3.select("#presentation")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
    svg.selectAll(".dot")
        .data(design.data)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 3.5)

    if (design.haxis) {
    
        var x = d3.scale.linear()
            .range([0, width]);

        x.domain(d3.extent(data, function(d) { return d.hpos; })).nice();
        
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
       
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
           .append("text")
            .attr("class", "label")
            .attr("x", width)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text(design.hlabel);

        svg.selectAll(".dot")
            .data(design.data)
            .enter().append("circle")
            .attr("cx", function(d) { return x(d.x); })
    }
    
    if (design.vaxis) {
    
        var y = d3.scale.linear()
            .range([0, height]);
        
        y.domain(d3.extent(data, function(d) { return d.vpos; })).nice();

        var yAyis = d3.svg.axis()
            .scale(y)
            .orient("left");
       
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
        
        svg.selectall(".dot")
            .data(design.data)
            .enter().append("circle")
            .attr("cy", function(d) { return y(d.y); })

    } 
    
    if (design.color) {

        svg.selectall(".dot")
            .data(design.data)
            .enter().append("circle")
            .style("fill", function(d) { return color(d.color); });

        //var legend = svg.selectAll(".legend")
        //    .data(color.domain())
        //    .enter().append("g")
        //    .attr("class", "legend")
        //    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        //legend.append("rect")
        //    .attr("x", width - 18)
        //    .attr("width", 18)
        //    .attr("height", 18)
        //    .style("fill", color);

        //legend.append("text")
        //    .attr("x", width - 24)
        //    .attr("y", 9)
        //    .attr("dy", ".35em")
        //    .style("text-anchor", "end")
        //    .text(function(d) { return d; });

    }

}
