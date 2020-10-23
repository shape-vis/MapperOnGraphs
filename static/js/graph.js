

var FDL_Graph_Vis = function( svg_name, graph_data ) {


    let color_data = null;

    // General Variables
    let svg = d3.select(svg_name);
    let svg_width  = $(svg_name).width();
    let svg_height = $(svg_name).height();

    // Variables specific to this function
    let svg_g = svg.append("g");

    let use_link = graph_data.links.filter(function(d){return d.source!="null"&&d.target!="null";});

    let link = svg_g.append( "g" )
                .attr( "class", "links" )
                .selectAll( "line" )
                .data( use_link )
                    .enter().append( "line" )
                        .attr( "stroke-width", 1 )
                        .attr( "stroke", "lightgray" );

    let node = svg_g.append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(graph_data.nodes).enter()
                    .append("circle")
                        .attr("r", 5 )
                        .attr("fill", "black" )
                        .call(d3.drag()
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended) );

    let simulation = d3.forceSimulation()
                        .force( "link",   d3.forceLink().id( function(d) { return d.id; } ) )
                        .force( "charge", d3.forceManyBody() )
                        .force( "center", d3.forceCenter(svg_width / 2, svg_height / 2) )
                        .nodes(graph_data.nodes)
                        .on("tick", ticked );

    simulation.force("link").links(use_link);

    let zoom_handler = d3.zoom().on("zoom", zoom_actions);
    zoom_handler(svg);


   function ticked() {
        link
            .attr("x1", d => d.source.x )
            .attr("y1", d => d.source.y )
            .attr("x2", d => d.target.x )
            .attr("y2", d => d.target.y );

        node
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            } );
    }

    function clicked(d) {
        //document.getElementById("object_details").innerHTML = JSON.stringify(d, undefined, 2);
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        //document.getElementById("object_details").innerHTML = JSON.stringify(d, undefined, 2);
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    function zoom_actions(){
        svg_g.attr("transform", d3.event.transform);
        //prior_tform = d3.event.transform;
    }


    return {
        update_node_radius : function( radius_func ){
            node.attr("r", radius_func );
        },

        update_link_width : function( width_func ){
            link.attr("stroke-width", width_func );
        },

        update_node_color : function( _color_data ){
            color_data = _color_data;
            ext = d3.extent( Object.keys(color_data), d=>color_data[d] );
            seqColorScheme.domain( ext );
            node.attr("fill", d => seqColorScheme( color_data[d.id] ) );
        },

        restart_simulation : function(){
            simulation.alphaTarget(0).restart();
        },

        remove : function(){
            svg_g.remove();
        }
    }

}

