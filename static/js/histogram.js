

var histogram_vis = function( svg_name ) {

    // General Variables
    let svg = d3.select(svg_name);
    let svg_width  = $(svg_name).width();
    let svg_height = $(svg_name).height();

    // Variables specific to this function
    let bars = null;
    let position = { left: 20, top: 20, right: 200, bottom: 300 };


    return {

        set_position : function( left, top, width, height ){
            position.left   = left;
            position.right  = left+width;
            position.top    = top;
            position.bottom = top+height;
        },

        remove : function( ){
            if( bars ) bars.remove();
            bars = null;
        },

        update_drawing : function( bar_count, data ){

            if( bars ) bars.remove();

            let ext = d3.extent( data );

			let bins = d3.histogram()
			                .domain(ext)
            			    .thresholds( [...Array(bar_count).keys()].map( d=> ext[0]*(1-d/bar_count) + ext[1]*d/bar_count ) )
                                ( data );

            let x = d3.scaleLinear()
                        .range([ position.left, position.right ])
                        .domain([0, d3.max(bins, function(d) { return d.length; })]);

            let y = d3.scaleLinear()
                        .range([ position.top, position.bottom ])
                        .domain(ext);

            seqColorScheme.domain( ext );

            bars = svg.append( "g" )
                        .selectAll( "rect" )
                          .data(bins)
                          .enter()
                          .append("rect")
                            .attr("x", d => x(0) )
                            .attr("y", d => y(d.x0) )
                            .attr("width", d => x(d.length)-x(0)+2 )
                            .attr("height", d => y(d.x1) - y(d.x0) - 1 )
                            .style("fill", d => seqColorScheme(d.x0) )

        }
    }

}

