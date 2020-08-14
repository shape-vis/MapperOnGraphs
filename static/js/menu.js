




var datasets = {};


function construct_options_array( arr, selected=null ){
    let html = "";
    arr.sort();
    arr.forEach( function(d){
        if( d == selected )
            html += '<option value="'+ d +'" selected>'+ d +'</option>';
        else
            html += '<option value="'+ d +'">'+ d +'</option>';
    });
    return html;
}

function construct_options_dict( obj, selected=null ){
    let html = "";
    let arr = Object.keys(obj);
    arr.sort();
    arr.forEach( function(d){
        if( d == selected )
            html += '<option value="'+ obj[d] +'" selected>'+ d +'</option>';
        else
            html += '<option value="'+ obj[d] +'">'+ d +'</option>';
    });
    return html;
}

function load_datasets( ){
    d3.json( "datasets", function( dinput ) {
        datasets = dinput;
        document.getElementById("dataset").innerHTML = construct_options_array( Object.keys(datasets) );
        update_datafiles();
    });
}


function update_datafiles(){
    var ds = get_selected_dataset();
    console.log(ds)
    if( document.getElementById("datafile") != null ){
        document.getElementById("datafile").innerHTML = construct_options_array( Object.keys(datasets[ds]) );
    }
//    change_datafile();
}

function update_filter_functions(ff_list){
    var ds = get_selected_dataset();
    var df = get_selected_datafile();
    if( document.getElementById("filter_func") != null ){
        document.getElementById("filter_func").innerHTML = construct_options_dict(ff_list);
    }
//    reload_data();
}


function get_selected_option( elementID ){
    var e = document.getElementById(elementID);
    if( e == null ) return null;
    return e.options[e.selectedIndex].value;
}
function get_selected_dataset(){ return get_selected_option("dataset"); }
function get_selected_datafile(){ return get_selected_option("datafile"); }
function get_selected_filter_func(){ return get_selected_option("filter_func"); }



















