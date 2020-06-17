

function reload_graph_vis( graph_data ){
	$("#graph_vis").empty();

    let gv_svg = d3.select("#graph_vis"),
        gv_svg_width  = $("#graph_vis").width(),
        gv_svg_height = $("#graph_vis").height();

	let gv_svg_g = gv_svg.append("g");

	let simulation = d3.forceSimulation()
                        .force( "link",   d3.forceLink().id( function(d) { return d.id; } ) )
                        .force( "charge", d3.forceManyBody() )
                        .force( "center", d3.forceCenter(gv_svg_width / 2, gv_svg_height / 2) );

    let use_link = graph_data.links.filter(function(d){return d.source!="null"&&d.target!="null";});

    let link = gv_svg_g.append( "g" )
                .attr( "class", "links" )
                .selectAll( "line" )
                .data( use_link )
                    .enter().append( "line" )
                        .attr( "stroke-width", 1 )
                        .attr( "stroke", "lightgray" );

    let node = gv_svg_g.append("g")
                .attr("class", "nodes")
                .selectAll("g")
                .data(graph_data.nodes)
                    .enter().append("g")

    let circles = node.append("circle")
                    .attr("r", 5 )
                    .attr("fill", "black" )
                    .on("click", clicked)
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended) );


    simulation
        .nodes(graph_data.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(use_link);

    let zoom_handler = d3.zoom().on("zoom", zoom_actions);
    zoom_handler(gv_svg);



    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

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
        //console.log( d3.event.transform );
        gv_svg_g.attr("transform", d3.event.transform);
        prior_tform = d3.event.transform;
    }

}

/*
		var simulation = null;
		var prior_tform = null;



			var showing_mapper = document.getElementById('showMapper').checked;

			//if( prior_sel_idx < 0 ) return;


			var gv_svg_g = gv_svg.append("g");
			if( prior_tform != null ){
				gv_svg_g.attr("transform", prior_tform);
			}
			//
//			gv_svg.call(d3.zoom().on("zoom", function () {
//				gv_svg.attr("transform", d3.event.transform)
//			}));

			var color = d3.scaleOrdinal( d3.schemeCategory20 );

			url = "graph?";
			if( showing_mapper ){
				url = "mog?";
			}

			var curr = 0;

			console.log( url + $('#parameterForm').serialize() )
			d3.json( url + $('#parameterForm').serialize(), function(error, graph) {
				if (error) throw error;

				console.log( graph);

				var color_func = null;
				var rad_func = null;

				if( showing_mapper ){
					dmin = d3.min( graph.nodes, function(n){ return n['min_value']; } );
					dmax = d3.max( graph.nodes, function(n){ return n['max_value']; } );
					console.log( [dmin,dmax] );

					myColor = d3.scaleSequential().domain([dmin,dmax])
  							.interpolator(d3.interpolateViridis);
				  	color_func = function(d){ console.log(d['avg_value']); return myColor(d['avg_value']); };
				  	rad_func = function(d){ l = d['components'].length; return (l>10)?10:l; }
				}
				else{
					myColor = d3.scaleOrdinal()
									.domain(graph.nodes, function(n){ return n['type']; } )
				  					.range(d3.schemeSet3);
				  	color_func = function(d){ return myColor(d['type']); };
				  	rad_func = function(d){ return 5; }
				}
			});

		}

*/