




var datasets = {};


function construct_options_array( arr, selected=null ){
    html = "";
    arr.sort();
    arr.forEach( function(d){
        if( d == selected )
            html += '<option value="'+d+'" selected>'+d+'</option>';
        else
            html += '<option value="'+d+'">'+d+'</option>';
    });
    return html;
}

function construct_options_dict( obj, selected=null ){
    return construct_options_array( Object.keys(obj), selected );
}

function load_datasets( ){
    d3.json( "datasets", function( dinput ) {
        datasets = dinput;
        document.getElementById("dataset").innerHTML = construct_options_dict(datasets);
        change_dataset();
    });
}


function change_dataset(){
    var ds = get_selected_dataset();
    console.log(ds)
    if( document.getElementById("datafile") != null ){
        document.getElementById("datafile").innerHTML = construct_options_dict(datasets[ds]);
    }
    change_datafile();
}

function change_datafile(){
    var ds = get_selected_dataset();
    var df = get_selected_datafile();
    if( document.getElementById("filter_func") != null ){
        document.getElementById("filter_func").innerHTML = construct_options_array(datasets[ds][df]);
    }
    reload_data();
}


function get_selected_option( elementID ){
    var e = document.getElementById(elementID);
    if( e == null ) return null;
    return e.options[e.selectedIndex].value;
}
function get_selected_dataset(){ return get_selected_option("dataset"); }
function get_selected_datafile(){ return get_selected_option("datafile"); }
function get_selected_filter_func(){ return get_selected_option("filter_func"); }





















var menu_dict = null;
var active_menu = null;
var doc_form = null;
var menu_change_callback = null;

function init_menu_vars( menu_dict ){

    Object.keys( menu_dict ).forEach( function(k){
    	if( menu_dict[k]["type"] == "select" ){
   			var options = Object.keys( menu_dict[k]["options"] );
    		if( menu_dict[k]["value"] === undefined ){
    			if( options.length > 0 )
    				menu_dict[k]["value"] = options[0];
    			else
    				menu_dict[k]["value"] = null;
    		}
    		options.forEach( function( opt ){
    			if( menu_dict[k]["options"][opt]["submenu"] !== undefined ){
    				init_menu_vars(  menu_dict[k]["options"][opt]["submenu"] );
    			}
    		});
    	}
    });

}

function extract_active_menu_items( menu_dict, menu_items={} ){
    Object.keys( menu_dict ).forEach( function(k){
    	menu_items[k] = menu_dict[k];
    	if( menu_dict[k]["type"] == "select" ){
    		var sel = menu_dict[k]["value"];
    		if( sel !== null ){
				if( menu_dict[k]["options"][sel]["submenu"] !== undefined ){
					extract_active_menu_items( menu_dict[k]["options"][sel]["submenu"], menu_items );
				}
			}
    	}
    });

    return menu_items;
}



function menu_build_range( key, obj ){

	html = '';
	html += '<div class="form-group">';
    html += '	<label for="'+ key +'">'+ obj['name'] +'</label>';
    html += '	<input type="range" class="custom-range" min="'+ obj['min'] + '" max="'+ obj['max'] +
    												  '" step="'+ obj['step'] + '" value="'+ obj['value'] +
    												  '" id="'+ key + '" name="'+ key + '" onchange="update_menu(this);">';
	html += '</div>';
	return html;
}

function menu_build_checkbox( key, obj ){

    var chk = obj['value']?'checked':'';
	html = '';
	html += '<div class="form-check">';
    html += '	<input class="form-check-input" type="checkbox" id="'+ key + '" name="'+ key + '" onchange="update_menu(this);"' + chk + '>';
    html += '	<label class="form-check-label" for="'+ key +'">'+ obj['name'] +'</label>';
	html += '<br></div>';

	return html;
}

function menu_sort_dict_keys( dict ){
    return Object.keys(dict).sort( function(a,b){
										if( dict[a]["order"] < dict[b]["order"] ) return -1;
										if( dict[a]["order"] > dict[b]["order"] ) return  1;
										return 0;
									} );
}

function menu_build_select( key, obj ){

	html = '';
	html += '<div class="form-group">';
    html += '	<label for="'+ key +'">'+ obj['name'] +'</label>';
    html += '	<select class="form-control form-control-sm" id="'+ key + '" name="'+ key + '" onchange="update_menu(this);">';

	menu_sort_dict_keys( obj['options'] ).forEach( function( k ){
	    if( k == obj['value']){
	        html += '		<option value="'+k+'" selected>'+ obj['options'][k]['name'] +'</option>';
	    }
	    else{
	        html += '		<option value="'+k+'">'+ obj['options'][k]['name'] +'</option>';
	    }

	});
	html += '	</select>';
	html += '</div>';

	return html;

}


function build_menu_html( ){
	active_menu = extract_active_menu_items( menu_dict );
    var keys = menu_sort_dict_keys( active_menu );

	html = '';
    keys.forEach( function(k){
    	switch( active_menu[k]["type"] ){
    		case "range" : html += menu_build_range( k, active_menu[k] ); break;
    		case "checkbox" : html += menu_build_checkbox(  k, active_menu[k] ); break;
    		case "select" : html += menu_build_select(  k, active_menu[k] ); break;
    		default:
    			console.log( active_menu[k]["type"] );
    	}
    });

    doc_form.innerHTML = html;

}

function update_menu( obj ){

	var mod_key = obj.id;
	var mod_obj = active_menu[mod_key];

	switch( mod_obj["type"] ){
		case "range" :
				mod_obj["value"] = obj.value;
				break;
		case "checkbox" :
				mod_obj["value"] = obj.checked;
				break;
		case "select" :
				mod_obj["value"] = obj.value;
				build_menu_html();
				break;
		default:
			console.log( active_menu[k]["type"] );
	}

	menu_change_callback();

}


function load_menu( url, form_id, _menu_change_callback ){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
	  if (this.readyState == 4 && this.status == 200) {

        doc_form = document.getElementById(form_id);
		menu_dict = JSON.parse(this.responseText);

		init_menu_vars( menu_dict );
        build_menu_html( );

        menu_change_callback = _menu_change_callback;
        menu_change_callback();
	  }
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}


