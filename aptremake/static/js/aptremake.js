function render(design) {
    
    console.log(design)

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

    points = svg.selectAll(".hi")
        .data(design.data)
        .enter().append("circle")
        .style("fill", "black")
        .attr("r", 3)
        .attr("mark", function(d) { return d.mark; });
        //.attr("cx", function(d) { return Math.floor(Math.random() * 100); })
        //.attr("cy", function(d) { return Math.floor(Math.random() * 100); });

    if (design.haxis) {
    
        var x = d3.scale.linear()
            .range([0, width]);


        x.domain(d3.extent(design.data, function(d) { return d.hpos; })).nice();
        
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(5); // FIXME: Maybe this shouldn't be hard-coded.
     
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

        points.attr("cx", function(d) { return x(d.hpos); });

    }
    
    if (design.vaxis) {
    
        var y = d3.scale.linear()
            .range([height, 0]);
        
        y.domain(d3.extent(design.data, function(d) { return d.vpos; })).nice();

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(5); // FIXME: Maybe this shouldn't be hard-coded.
       
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

    } 
    
    if (design.color) {

        var color = d3.scale.category10();

        points.style("fill", function(d) { return color(d.color); });


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
