

var GraphVisualization = function(svg_name, _graph_data ) {

    // Copy of the graph
    let g_data = _graph_data;

    // General Variables
    let svg = d3.select(svg_name);
    let svg_width  = $(svg_name).width();
    let svg_height = $(svg_name).height();

    // Variables specific to this function
    let svg_g = svg.append("g");
    let svg_txt = svg.append("g");

    let link = null
    let node = null
    let simulation = null
    let zoom_handler = null

    let point_radius_func = 5
    let stroke_width_func = 1

    let end_cb = null, tick_cb = null
    let tick_n = 0

    let color_data = null
    let color_func = "black"

    function load_visualization() {
        link = svg_g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(g_data.links)
            .enter().append("line")
            .attr("stroke-width", stroke_width_func)
            .attr("stroke", "lightgray");

        node = svg_g.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(g_data.nodes).enter()
            .append("circle")
            .attr("r", point_radius_func )
            .attr("fill", "black")
            .attr('stroke', 'black')
            .attr('stroke-width', '1px')
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        if (color_data)
            node.attr("fill", d => color_func(color_data[d.id]));
        else
            node.attr("fill", color_func );

        simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id( d =>d.id ))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(svg_width / 2, svg_height / 2))
            .nodes(g_data.nodes)
            .on("tick", ticked)

        if( end_cb ) simulation.on("end",end_cb)

        simulation.force("link").links(g_data.links);

        zoom_handler = d3.zoom().on("zoom", function(){
            if (typeof point_radius_func === 'function')
                node.attr('r', d => point_radius_func(d) / d3.event.transform.k)
            else
                node.attr('r', point_radius_func / d3.event.transform.k)

            if (typeof stroke_width_func === 'function')
                link.attr("stroke-width", d => stroke_width_func(d) / d3.event.transform.k)
            else
                link.attr("stroke-width", stroke_width_func / d3.event.transform.k)

            svg_g.attr("transform", d3.event.transform)
        });
        svg.call(zoom_handler).call(zoom_handler.transform, d3.zoomIdentity);

        svg.style("cursor", "auto" )


    }

    function ticked() {
        link
            .attr("x1", d => d.source.x ).attr("y1", d => d.source.y )
            .attr("x2", d => d.target.x ).attr("y2", d => d.target.y );

        node
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            } );

        if( tick_cb ) tick_cb(tick_n)
        tick_n++
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
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


    function zoom_to_fit(paddingPercent, transitionDuration) {
        let bounds = svg_g.node().getBBox();
        let midX = bounds.x + bounds.width / 2,
            midY = bounds.y + bounds.height / 2;

        if (bounds.width === 0 || bounds.height === 0) return; // nothing to fit

        let scale = (paddingPercent || 0.75) / Math.max(bounds.width / svg_width, bounds.height / svg_height);
        let translate = [svg_width / 2 - scale * midX, svg_height / 2 - scale * midY];

        let transform = d3.zoomIdentity
            .translate(translate[0], translate[1])
            .scale(scale);

        svg.call(zoom_handler)
                .transition()
                .duration(transitionDuration || 0)
                .call(zoom_handler.transform, transform)
    }




    return {
        set_node_radius : function( radius_func ){
            point_radius_func = radius_func;
            if( node ) node.attr("r", point_radius_func );
        },

        set_link_width : function( width_func ){
            stroke_width_func = width_func
            if( link ) link.attr("stroke-width", stroke_width_func );
        },

        //set_node_color : function( color_scheme, _func, _data=null ){
        set_node_color : function( _func, _data=null ){
            color_func = _func
            color_data = _data
            if(node) {
                if (color_data)
                    node.attr("fill", d => color_func(color_data[d.id]));
                else
                    node.attr("fill", color_func );
            }
        },

        set_end_callback : function( cb ){
            end_cb = cb
            if( simulation ) simulation.on('end',cb)
        },

        set_tick_callback : function( cb ){
            tick_cb = cb
        },

        load : function(){
                if( g_data.nodes.length < 1000 && g_data.links.length < 2500 ) {
                    /*svg.style("cursor", "progress" )
                    setTimeout( ()=>load_visualization(), 10);*/
                    load_visualization()
                }
                else{
                    let tmp_text = svg_txt.append("text")
                            .attr("x", svg_width/2 )
                            .attr("y", svg_height/2 )
                            .attr("font-family", "sans-serif")
                            .attr("text-anchor", "middle")
                            .attr("cursor","alias")
                            .attr("font-size", "16px")
                            .attr("fill", "red")
                            .on("click",function(){
                                tmp_text.remove()
                                svg.style("cursor", "progress" )
                                setTimeout( ()=>load_visualization(), 10);
                            });

                    tmp_text.append("tspan").text("Large Graph")
                        .attr("dy","-1.2em")
                        .attr("x",svg_width/2)
                    tmp_text.append("tspan").text("(n: " + g_data.nodes.length + ", e: " + g_data.links.length + ")")
                        .attr("dy","1.2em")
                        .attr("x",svg_width/2)
                    tmp_text.append("tspan").text("Click To Load Anyways")
                        .attr("dy","1.2em")
                        .attr("x",svg_width/2)
                }

        },

        restart_simulation : function(){
            if( simulation ) simulation.alphaTarget(0).restart();
        },

        remove : function(){
            if( simulation ) simulation.stop();
            if( svg_g ) svg_g.remove();
            if( svg_txt ) svg_txt.remove();
        },

        add_count_labels : function(){
            svg_txt.append("text")
                .attr("x", svg_width-5 )
                .attr("y", svg_height-15 )
                .text(  g_data.nodes.length + " nodes")
                    .attr("font-family", "sans-serif")
                    .attr("text-anchor", "end")
                    .attr("font-size", "10px")
                    .attr("fill", "red");
            svg_txt.append("text")
                .attr("x", svg_width-5 )
                .attr("y", svg_height -5 )
                .text(  g_data.links.length + " edges")
                    .attr("font-family", "sans-serif")
                    .attr("text-anchor", "end")
                    .attr("font-size", "10px")
                    .attr("fill", "red");
        },

        add_zoom_button : function(){
            svg_txt.append("svg:image")
                .attr('x', svg_width - 25)
                .attr('y', 5)
                .attr('width', 20)
                .attr('height', 20)
                .attr("xlink:href", "static/img/fit-to-width.png")
                .on("click", () => zoom_to_fit(0.975, 2500))
        },

        zoomFit : function() {
            zoom_to_fit( 0.975,2500 );
        },

        send_to_url : function(url, addl_data={}){
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            let tmp_data = {}
            Object.keys(addl_data).forEach( k =>{
                tmp_data[k] = addl_data[k]
            })
            tmp_data['nodes'] = g_data.nodes
            tmp_data['links'] = []
            g_data.links.forEach( function(L){
               tmp_data.links.push({'value':L.value,'source':L.source.id,'target':L.target.id});
            });
            xhr.send(JSON.stringify(tmp_data));
        },

        get_graph : function(){
            return g_data
        }
    }

}

