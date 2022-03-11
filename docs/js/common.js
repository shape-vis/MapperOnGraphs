
var colorSchemes = {
    'agd': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateGnBu),
    'den_0_5': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateOranges),
    'ecc': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateBuGn),
    'ev_1': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateBuPu),
    'ev_norm_1': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateBuPu),
    'fv': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateBuPu),
    'fv_norm': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateBuPu),
    'pr_0_85': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateYlOrRd),
    'default': d3.scaleSequential().domain([0,1]).interpolator(d3.interpolateGreys)
}


var colorSchemeImages = {
    'agd': 'static/img/GnBu.png',
    'den_0_5': 'static/img/Oranges.png',
    'ecc': 'static/img/BuGn.png',
    'ev_1': 'static/img/BuPu.png',
    'ev_norm_1': 'static/img/BuPu.png',
    'fv': 'static/img/BuPu.png',
    'fv_norm': 'static/img/BuPu.png',
    'pr_0_85': '`static/img/YlOrRd.png`',
    'default': 'static/img/Greys.png'
}

function clear_chart( chart_name ){
	$(chart_name).empty();
}

var pages = ["small_multiples.html","figures.html", "interactive.html", "user_study.html"];
var page_titles = {"small_multiples.html": "Small Multiple Parameter Explorer",
                    "figures.html": "Paper Figures",
                    "interactive.html": "Interactive",
                    "user_study.html": "User Study"};


function insert_page_header(){
    html = `<div class="page" style="padding: 15px;">
                <h2 style="margin: 0; font-weight: bold;">Homology-Preserving Graph Skeletonization Using Mapper on Graphs</h2>
                <!-- <h3 style="padding-left: 5px; padding-top: 10px;">Paul Rosen; Mustafa Hajij; and Bei Wang</h3>-->`;

	// if( new Date() > new Date(2020, 9, 14) )
	// 	html += '<h3 style="padding-left: 5px; padding-top: 10px;">Under submission to Transactions on Visualization and Computer Graphics</h3>';
	html += '<h3 style="padding-left: 5px; padding-top: 10px;">IEEE VIS Submission #</h3>';

	html += '</div>';

    document.write(html);
}



function insert_navbar( curpage ){
    html = `<nav class="navbar navbar-expand-lg navbar-light bg-light">
              <a class="navbar-brand" href="index.html">MOG</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">`;

    pages.forEach(function(key){
        if( curpage == key ){
            html += '<li class="nav-item active">';
        }
        else{
            html += '<li class="nav-item">';
        }
        html += '<a class="nav-link" href="' + key + '">' + page_titles[key] + '</a>';
        html += '</li>';
    });

    html += `    </ul>
               </div>
             </nav>`;
    document.write(html);
}



function downloadText(text, filename) {
    var a = document.createElement('a');
    a.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    a.setAttribute('download', filename);
    a.click()
}

function downloadJson(obj, filename) {
    downloadText(JSON.stringify(obj), filename);
}


function saveSVG( plotID, name='' ){
    if( name === '' ) name = plotID.substring(1)
    let svgData = $(plotID)[0].outerHTML;
    let svgBlob = new Blob([svgData], {type:"image/svg+xml;charset=utf-8"});
    let svgUrl = URL.createObjectURL(svgBlob);
    let downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = name + ".svg";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

