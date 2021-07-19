

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
    d3.json( "data/datasets.json", function( dinput ) {
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



function generate_checkbox(id, label, onclick='', width=-1){

    _html = ''
    _html += '<div class="btn-group-toggle" data-toggle="buttons">';
    _html += '<label class="btn btn-outline-secondary" '
    if( width > 0 ) _html += 'style="width:' + width + 'px;" '
    _html += '>'
    _html += '<input type="checkbox" id="'+id+'" name="'+id+'" value="true" autocomplete="off" onclick="toggle_button(this);'+onclick+'">'+label+'</label><br>'
    _html += '</div>'

    return {
        getHTML : function(){return _html},
        isChecked : function(){ return document.getElementById(id).checked; }
    }
}

function generate_radiogroup(name, options, onchange='', width=-1){
    _html = ''
    _html += '<div class="btn-group-toggle" data-toggle="buttons">';
    options.forEach(L=>{
        if(('checked' in L) && L.checked)
            _html += '<label class="btn btn-primary" '
        else
            _html += '<label class="btn btn-outline-secondary" '
        if( width > 0 ) _html += 'style="width:' + width + 'px;" '
        _html += '>'
        _html += '<input type="radio" id="'+name+'" name="'+name+'" autocomplete="off" value="'+L.value+'" '
                    + ((('checked' in L) && L.checked)?'checked ':'')
                    + 'onchange="toggle_radio(this);'+onchange+'">'+L.label+'</label><br>'
    })
    _html += '</div>'

    return {
        getHTML : function(){return _html},
        getSelected : function(){
            let sel = null;
            document.getElementsByName(name).forEach( E=>{
                if( E.checked ) sel = E.value;
            })
            return sel;
        }
    };
}

function generate_slider(label, id, min_val = 0, max_val=100, step=1, default_val = 0, onchange=''){
    _html = ''
    _html += '<label for="' + id + '">' + label + '<span id="' + id + '_value">' + default_val + '</span></label>'
    _html += '<input type="range" class="custom-range"'
                + 'min="'+min_val+'" '
                + 'max="'+max_val+'" '
                + 'step="'+step+'" '
                + 'value="'+default_val+'" '
                + 'id="' + id + '" name="' + id + '" '
                + 'oninput="document.getElementById(\'' + id + '_value\').innerHTML = document.getElementById(\'' + id + '\').value;" '
                + 'onchange="'+onchange+'">';
    return {
        getHTML : function(){return _html},
        getValue : function(){
            return parseFloat(document.getElementById(id).value)
        },
        setValue : function(v){
            document.getElementById( id + '_value').innerHTML = v
            document.getElementById(id).value = v
        }

    }
}

function toggle_button(obj){
    if(obj.checked)
        obj.parentElement.className = "btn btn-primary"
    else
        obj.parentElement.className = "btn btn-outline-secondary"
}

function toggle_radio(obj){
    document.getElementsByName(obj.name).forEach( R => {
        if(R.checked)
            R.parentElement.className = "btn btn-primary"
        else
            R.parentElement.className = "btn btn-outline-secondary"
    })
}