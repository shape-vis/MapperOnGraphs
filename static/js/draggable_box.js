

var DraggableBox = function( svg_name ) {

    // General Variables
    let svg = d3.select(svg_name);
    let svg_width  = $(svg_name).width();
    let svg_height = $(svg_name).height();

    var isXChecked = true,
        isYChecked = true;

    var dragbarw = 6;

    var position = {x: 300 / 2, y: 200 / 2, width: 300, height: 200 };

    var constraints = {left: 50, right: svg_width, top: 100, bottom: svg_height};


    var newg = svg.append("g")
          .data([position]);

    var dragrect = newg.append("rect")
          .attr("fill-opacity", 1)
          .attr("fill", "lightgray")
          .attr("stroke", "black")
          .attr("stroke-width", 1)
          .attr("cursor", "move")
          .call(d3.drag().on("drag", dragmove));

    var dragbarleft = newg.append("rect")
          .attr("fill", "lightblue")
          .attr("fill-opacity", 0)
          .attr("cursor", "ew-resize")
            .call(d3.drag().on("drag", ldragresize));

    var dragbarright = newg.append("rect")
          .attr("fill", "lightblue")
          .attr("fill-opacity", 0)
          .attr("cursor", "ew-resize")
            .call(d3.drag().on("drag", rdragresize));

    var dragbartop = newg.append("rect")
          .attr("fill", "lightgreen")
          .attr("fill-opacity", 0)
          .attr("cursor", "ns-resize")
            .call(d3.drag().on("drag", tdragresize));

    var dragbarbottom = newg.append("rect")
          .attr("fill", "lightgreen")
          .attr("fill-opacity", 0)
          .attr("cursor", "ns-resize")
            .call(d3.drag().on("drag", bdragresize));

    function update_positions(){

        dragrect
          .attr("x", function(d) { return d.x; })
          .attr("y", function(d) { return d.y; })
          .attr("height", function(d) { return d.height; })
          .attr("width", function(d) { return d.width; } );

        dragbarleft
          .attr("x", function(d) { return d.x - (dragbarw/2); })
          .attr("y", function(d) { return d.y + (dragbarw/2); })
          .attr("height", function(d) { return d.height - dragbarw; })
          .attr("width", dragbarw)

        dragbarright
          .attr("x", function(d) { return d.x + d.width - (dragbarw/2); })
          .attr("y", function(d) { return d.y + (dragbarw/2); })
          .attr("height", function(d) { return d.height - dragbarw; })
          .attr("width", dragbarw);

        dragbartop
          .attr("x", function(d) { return d.x + (dragbarw/2); })
          .attr("y", function(d) { return d.y - (dragbarw/2); })
          .attr("height", dragbarw)
          .attr("width", function(d) { return d.width - dragbarw; });

        dragbarbottom
          .attr("x", function(d) { return d.x + (dragbarw/2); })
          .attr("y", function(d) { return d.y + d.height - (dragbarw/2); })
          .attr("height", dragbarw)
          .attr("width", function(d) { return d.width - dragbarw; });

    }

    function dragmove(d) {
      if (isXChecked) {
            d.x = Math.max(constraints.left, Math.min(constraints.right - d.width, d3.event.x));
      }
      if (isYChecked) {
            d.y = Math.max(constraints.top, Math.min(constraints.bottom - d.height, d3.event.y))
      }
      update_positions();
    }

    function ldragresize(d) {
       if (isXChecked) {
          var oldx = d.x;
          d.x = Math.max(constraints.left, Math.min(d.x + d.width - (dragbarw / 2), d3.event.x));
          d.width = Math.max(dragbarw+1,d.width + (oldx - d.x));
      }
      update_positions();
    }

    function rdragresize(d) {
       if (isXChecked) {
         var dragx = Math.max(d.x + (dragbarw/2), Math.min(constraints.right, d.x + d.width + d3.event.dx));
         d.width = Math.max(dragbarw+1,dragx - d.x);
      }
      update_positions();
    }

    function tdragresize(d) {
       if (isYChecked) {
          var oldy = d.y;
          d.y = Math.max(constraints.top, Math.min(d.y + d.height - (dragbarw / 2), d3.event.y));
          d.height = Math.max(dragbarw+1,d.height + (oldy - d.y));
      }
      update_positions();
    }

    function bdragresize(d) {
       if (isYChecked) {
         var dragy = Math.max(d.y + (dragbarw/2), Math.min(constraints.bottom, d.y + d.height + d3.event.dy));
         d.height = Math.max(dragbarw+1,dragy - d.y);
      }
      update_positions();
    }


    update_positions();


    return {
        lock_x : function( ){
            isXChecked = false;
            dragbarleft.attr("visibility", "hidden");
            dragbarright.attr("visibility", "hidden");
        },

        unlock_x : function(){
            isXChecked = true;
            dragbarleft.attr("visibility", "visible");
            dragbarright.attr("visibility", "visible");
        },

        lock_y : function( ){
            isYChecked = false;
            dragbartop.attr("visibility", "hidden");
            dragbarbottom.attr("visibility", "hidden");
        },

        unlock_y : function(){
            isYChecked = true;
            dragbartop.attr("visibility", "visible");
            dragbarbottom.attr("visibility", "visible");
        },

        get_position : function(){
            return position;
        },

        set_constraints : function( left, right, top, bottom ){
            constraints.left = left;
            constraints.right = right;
            constraints.top = top;
            constraints.bottom = bottom;
        },

        set_position : function( left, top, width, height ){
            position.x = left;
            position.y = top;
            position.width = width;
            position.height = height;
            update_positions();
        },

        attr : function( field, value ){
            return dragrect.attr(field, value );
        }
    }
}