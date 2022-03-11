

var CoverVisualization = function(svg_name ) {

    // General Variables
    let svg = d3.select(svg_name);

    // Variables specific to this function
    let bars = null;
    let position = { left: 20, top: 20, right: 200, bottom: 300 };

    let defs = svg.append("defs");

    //Append a linearGradient element to the defs and give it a unique id
    function createGradient(startCol, endCol) {
        let name = "linear-gradient-" + Math.random()
        var linearGradient = defs.append("linearGradient")
            .attr("id", name);

        linearGradient
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "0%").attr("y2", "100%");

        //Set the color for the start (0%)
        linearGradient.append("stop")
            .attr("offset", "0%")
            .attr("stop-color", startCol); //light blue

        //Set the color for the end (100%)
        linearGradient.append("stop")
            .attr("offset", "100%")
            .attr("stop-color", endCol); //dark blue

        return "url(#"+name+")"
    }


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

        update_drawing : function( coverN, coverOverlap, colorScheme ){

            if( bars ) bars.remove();

            let bar_ranges = []
            let group_maxes = new Array(coverN).fill(-1);
            let max_group = 0;
            for( let i = 0; i < coverN; i++){
                let minV = Math.max(0,i/coverN-coverOverlap-0.0001)
                let maxV = Math.min(1,(i+1)/coverN+coverOverlap+0.0001)

                let grp = 0;
                while( group_maxes[grp] > minV ) grp++;
                group_maxes[grp] = maxV
                max_group = Math.max(grp,max_group)

                bar_ranges.push( [minV, maxV, grp] )
            }

            let x = d3.scaleLinear()
                        .range([ position.left, position.right ])
                        .domain([0, max_group+1]);

            let y = d3.scaleLinear()
                        .range([ position.top, position.bottom ])
                        .domain( [0,1] );

            svg.append("g")
                    .append("rect")
                        .attr("x", position.left-2 )
                        .attr("y", position.top-2 )
                        .attr("width", position.right-position.left+4 )
                        .attr("height", position.bottom-position.top+4 )
                        .style("fill", "none" )
                        .style("stroke", "black" )

            bars = svg.append( "g" )
                        .selectAll( "rect" )
                          .data(bar_ranges)
                          .enter()
                          .append("rect")
                            .attr("x", d => x(d[2]) )
                            .attr("y", d => y(d[0]) )
                            .attr("width", d => x(d[2]+1)-x(d[2])-1 )
                            .attr("height", d => y(d[1]) - y(d[0]) )
                            //.style("fill", d => seqColorScheme((d[0]+d[1])/2) )
                            .style("fill", d => createGradient( colorScheme(d[0]), colorScheme(d[1]) ) )
                            .style("stroke",'DarkGray')
                            .style("stroke-width",'0.4')


        }
    }

}

