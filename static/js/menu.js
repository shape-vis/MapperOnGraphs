
var datasets = {};

function construct_options_array( arr, selected=null ){
    tmp = {};
    arr.forEach( function(d){
        tmp[d] = d;
    });
    return construct_options_dict(tmp,selected);
}

function construct_options_dict( obj, selected=null ){
    let html = "";
    let arr = Object.keys(obj);
    arr.sort();
    arr.forEach( function(d){
        html += '<option value="'+ d +'"' + (( d == selected )?"selected":"") + '>'+ obj[d] +'</option>';
    });
    return html;
}

function load_datasets( callback=null ){
    d3.json( "datasets", function( dinput ) {
        datasets = dinput;
        console.log(datasets)
        document.getElementById("dataset").innerHTML = construct_options_array( Object.keys(datasets) );
        update_datafiles();
        if( callback ){ callback(); }
    });
}

function update_datafiles(){
    var ds = get_selected_dataset();
    //console.log(ds)
    if( document.getElementById("datafile") != null ){
        document.getElementById("datafile").innerHTML = construct_options_array( Object.keys(datasets[ds]) );
    }
    update_filter_functions();
}

function update_filter_functions(){
    var ds = get_selected_dataset();
    var df = get_selected_datafile();
    if( document.getElementById("filter_func") != null ){
        document.getElementById("filter_func").innerHTML = construct_options_dict(datasets[ds][df]);
    }
}


function get_selected_option( elementID ){
    var e = document.getElementById(elementID);
    if( e == null ) return null;
    return e.options[e.selectedIndex].value;
}
function get_selected_value( elementID ){
    var e = document.getElementById(elementID);
    if( e == null ) return null;
    return e.value;
}
function get_checked_value( elementID ){
    var e = document.getElementById(elementID);
    if( e == null ) return null;
    if( e.checked ) return e.value;
    return "false";
}
function get_selected_dataset(){ return get_selected_option("dataset"); }
function get_selected_datafile(){ return get_selected_option("datafile"); }
function get_selected_filter_func(){ return get_selected_option("filter_func"); }



















