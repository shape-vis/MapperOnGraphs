//layeredGraph.js - a js file which implements a layered graphing layout method
//By Curtis Davis

//Helper function for LG_graph_Vis
var LG_Graph_Vis_Helper = function( graph_data ) {

//Turns input JSON into manipulatable data
let data = JSON.parse(JSON.stringify(graph_data));

///////////////////////////////////////////////////////////////
//Graph layout attributes
var links, nodes;
var centeredBool = 1; //If graph is centered or not
var curvedEdges = 1; //Curve the midpoints of links or not
var bundleEdges = 1; //Bundle the midpoints of links or not

//////////////////////////////////////////////////////////////
//Heuristic bools for enabling type of crossings minimizations
var forwardsCrossingBool = 0;
var backwardsCrossingBool = 1;
var sidewaysCrossingBool = 1;

var swappingEnabled = 1; //General overall swapping function
var centerHeavyLinksUser = 1;
var debugging = 0; //Shows which links cross which

///////////////////////////////////////////
// Initial graph to hold node information
var layeredNodesGraph = new Array();

///////////////////////////////////////////
//svg formatting/styling
var myColors = d3.scaleOrdinal().domain(data)
	.range(["red","orange","olive","green","indigo","blue","#3cb"]);
	
d3.selectAll("#graphSVG > *").remove(); //Clear the graph each time
var svg = d3.select("#lgSVG")
	.call(d3.zoom().on("zoom", function () {
		// svg.attr("transform", d3.event.transform)
	})),
	width = +svg.attr("width"),
	height = +svg.attr("height"),
	g = svg.append("g").attr("transform", "translate(" + (600*(1 - centeredBool)) + "," + 100*(2 - centeredBool) + ")");

//////////////////////////////////////////////////////////////
//Graph formatting
var centerOfGraph = width / 2;

//Loading svg when constructing graph
var loading = svg.append("text")
	.attr("y", (height / 2)+"px")
	.attr("x", (width / 2)-60+"px")
	.attr("text-anchor", "right")
	.attr("font-family", "Arial, Helvetica, sans-serif")
	.attr("font-size", 14)
	.text("The layered graph is being constructed, please wait...");

//Function to remove loading animations when done
function removeProgress() {
	loading.remove();
}


//////////////////////////////////////////////////////////////
//d3 data importing and algorithms
d3.json(graph_data, function() {

	//Gets Nodes and Links from data
	nodes = data.nodes;
	links = data.links;

	//Filters according to slider on webpage
	let filterValue = document.getElementById('lg_node_amount_filter_value').innerHTML;

	//Freezes simulation of a force simulation, to give us a static graph
	var simulation = d3.forceSimulation(nodes)
		.force("charge", d3.forceManyBody().strength(-80))
		.force("link", d3.forceLink(links).distance(50).id(function(d) {
		return d.id;
		}))
		.force("x", d3.forceX())
		.force("y", d3.forceY())
		.stop();


	/////////////////////////////////////////////////////////////////////////////////
	//Condense graph to filterValue size by removing lesser important nodes and links
	function reduceLG() {
		//If no reduction, do nothing
		if(filterValue == 1.0) {
			console.log("Skipped reducing");
			return;
		}

		//Get target size of graph
		var maxSize = Math.floor(filterValue * nodes.length);
		console.log("filtered maxSize: ", maxSize);

		//Assign highest link connected to node
		for(node in nodes) { nodes[node].maxLinkValue = 0; }
		for(link = 0 ; link < links.length ; link++) {
			var linkSrcPos = nodes.map(function(e) { return e.id; }).indexOf(links[link].source.id);
			var linkTgtPos = nodes.map(function(e) { return e.id; }).indexOf(links[link].target.id);
			if(links[link].value > nodes[linkSrcPos].maxLinkValue) {
				nodes[linkSrcPos].maxLinkValue = links[link].value;
			}
			if(links[link].value > nodes[linkTgtPos].maxLinkValue) {
				nodes[linkTgtPos].maxLinkValue = links[link].value;
			}
		}

		//Sort links by their value (smallest to largest)
		//Initial sort by link weight
		links.sort((a, b) => {
			return (a.value > b.value) ? 1 : -1;
		})
		nodes.sort((a, b) => {
			return (a.maxLinkValue > b.maxLinkValue) ? 1 : -1;
		})

		//Remove smaller links's nodes, and those nodes' links
		console.log(nodes.length)
		console.log("initial node length", nodes.length)
		while(nodes.length > maxSize) {
			//Pick the current first node of the sorted list
			var nodeToRemove = nodes[0];

			//Priority to remove node with no links first
			if(nodeToRemove.maxLinkValue == 0) {
				nodes.shift();
				continue;
			}

			//Remove the node's links from the 'links' array
			for(j = 0; j < links.length; j++) {
				if(links[j].source.id == nodeToRemove.id || links[j].target.id == nodeToRemove.id) {
					links.splice(j, 1);
					j = 0;
				}
			}

			//Remove the node from the list of nodes
			nodes.shift();

		}
		console.log("final nodes length: ", nodes.length);
	}

	///////////////////////////////////////////////////////////////////
	/* Function: ColorLinks */
	//Color for links - prevents intermediate nodes changing link color
	function colorLinks() {
		for(i = 0; i < links.length; i++) {
			links[i].colorCode = ( (links[i].value * Math.random())) % 1.0;
		}
	}

	///////////////////////////////////////////////////////////////////
	/* Function: addTo2DArrayCoverLevel */
	//Builds the 2D graph into 2D array 'LayeredNodesGraph'
	function addTo2DArrayCoverLevel() {

		/* Set layer for each node in nodes and each node in links */
		for(i = 0; i < nodes.length; i++) {
			nodes[i].layer = nodes[i].cover.level;
		}
		for(i = 0; i < links.length; i++) {
			links[i].source.layer = links[i].source.cover.level;
			links[i].target.layer = links[i].target.cover.level;
		}
		
		/********************************************/
		/* Add nodes to graph layers */
		//Get largest layer
		let maxLayer = 0;
		for(i = 0; i < nodes.length; i++) {
			if(nodes[i].cover.level > maxLayer) {
				maxLayer = nodes[i].cover.level;
			}
		}

		//Setup all empty layers for graph
		for(i = 0; i <= maxLayer; i++) {
			layeredNodesGraph.push([]);
		}
		console.log(layeredNodesGraph)

		//Add nodes to graph
		for(i = 0; i < nodes.length; i++) {
			nodes[i].layer = nodes[i].cover.level;
			layeredNodesGraph[nodes[i].cover.level].push(nodes[i]);
		}
		/* End adding nodes to levels */
		/********************************************/

		//Go through links and find crossings
		for(q = 0; q < links.length; q++) {
			
			//If a link spans multiple layers
			var numbOfLayersCrossed = links[q].target.layer - links[q].source.layer;
			if(numbOfLayersCrossed > 1) {

				//For each layer in between these two nodes (source and target), add an intermediate node
				for(currLayer = (parseInt(links[q].source.layer) + 1); currLayer < links[q].target.layer; currLayer++ ) {
					//attempting to add an intermediate node to currLayer

					//Only add to layers in between
					if(currLayer < links[q].target.layer) {
						//Gets an arbitrary node from curr layer layer
						for(getLayerNode = 0; getLayerNode < nodes.length; getLayerNode++) {

							//Assigns a node
							if(nodes[getLayerNode].layer == currLayer) {
								var newInterNode = JSON.parse(JSON.stringify(nodes[getLayerNode]));
								newInterNode.y = nodes[getLayerNode].y;

								//Set interm node link to near-middle of graph
								newInterNode.x = (width / 2) - (widthPerNode / 4);
								newInterNode.id = "intermNode for " + links[q].source.id + "->" + links[q].target.id;

								newInterNode.linksIndices = []; newInterNode.linksIndices.push(links.length); //Keep link indices

								layeredNodesGraph[currLayer].unshift(newInterNode);
								nodes.push(newInterNode);
								console.log("added an interm node")

								//Changes link target to new node, add a new link from new node to original target
								var newLinkIntTgt = JSON.parse(JSON.stringify(links[0]));

								//New link intermediateNode-->originalTarget
								newLinkIntTgt.source = newInterNode;
								newLinkIntTgt.target = links[q].target;

								newLinkIntTgt.value = links[q].value; //Keep value/thickness the same
								newLinkIntTgt.colorCode = links[q].colorCode; //Keep color the same
								
								//Change old link to point originalSource-->intermediateNode
								links[q].target = newInterNode;

								links.push(newLinkIntTgt);
								break; //Have satisfied splitting the link
							}
						}
					}
				}
			}
		}

		/* Sort nodes in heaviest link order */
		//Sort node arrays in 'bell curve'-esque distribution
		for(i = 0; i < layeredNodesGraph.length; i++) {
			
			//Initial sort by link weight
			layeredNodesGraph[i].sort((a, b) => {
				//Get heaviest node 'a' link weight
				let aLinkWeight = 0;
				for(y = 0; y < links.length; y++) {
					if( links[y].source.id == a.id || links[y].target.id == a.id) {
						if(links[y].value > aLinkWeight) {
							aLinkWeight = links[y].value;
						}
					}
				}
				//Get heaviest node 'b' link weight
				let bLinkWeight = 0;
				for(y = 0; y < links.length; y++) {
					if( links[y].source.id == b.id || links[y].target.id == b.id) {
						if(links[y].value > bLinkWeight) {
							bLinkWeight = links[y].value;
						}
					}
				}

				if(aLinkWeight < bLinkWeight) {
					return 1;
				} else {
					return -1;
				}
			})


			let newLayer = [];
			//Left, right, left, right...
			for(j = 0; j < layeredNodesGraph[i].length; j++) {
				if(j % 2 === 0) {
					newLayer.push( layeredNodesGraph[i][j] );
				} else {
					newLayer.unshift( layeredNodesGraph[i][j] );
				}
			}
			layeredNodesGraph[i] = newLayer;
		}
		/* End Bell Curve Distribution */
		/*******************************/

	}

	///////////////////////////////////////////////////////////////////////////////////////////////
	/* Function: Update Nodes and Links */
	/* As 'LayeredNodesGraph' is modified, this function is used to update the actual data, 
	the 'links' & 'nodes', which will be used to construct the graph when all calculations are finished.
	This function transfers data from 'LayeredNodesGraph' to 'nodes' & 'links' */
	//Adds layer element to link source nodes
	//Adds layer element to link target nodes
	//Adds indexInLayer element to link source nodes
	//Adds indexInLayer element to link target nodes
	//Adds linkeWeightProduct to links
	function updateNodesAndLinks() {

		//Links
		for (i = 0; i < links.length; i++) { //For each link

			for(j = 0; j < layeredNodesGraph.length; j++) { //For each layer
				var pos = layeredNodesGraph[j].map(function(e) { return e.id; }).indexOf(links[i].source.id);
				if(pos > -1 ) {
					//j being the layer of the source node in the link - ( link[i] )
					links[i].source.layer = j;
					links[i].source.indexInLayer = pos;
				}

				//Skip this part for last layer
				if(j != layeredNodesGraph.length - 1) {
					//Check if target of link is in the next layer and set layer as such
					var targetPos = layeredNodesGraph[j+1].map(function(e) { return e.id; }).indexOf(links[i].target.id);
					if(targetPos > -1) {
						//j being the layer of the source node in the link - ( link[i] )
						links[i].target.layer = j+1;
						links[i].target.indexInLayer = targetPos;
					}
				}				
			}
		}

		//Nodes
		for(i = 0; i < nodes.length; i++) { //For each node in array
			for(j = 0; j < layeredNodesGraph.length; j++) { //For each layer
				let pos = links.map(function(e) { return e.source.id; }).indexOf(nodes[i].id);
				if(pos > -1 ) {
					var newLayer = links[pos].source.layer;
					nodes[i].layer = newLayer;
					nodes[i].indexInLayer = links[pos].source.indexInLayer;
				}
			}
		}

		//Transfer layeredNodesGraph info to nodes data array
		for(i in layeredNodesGraph) { //For each layer
			for(j in layeredNodesGraph[i]) { //For each node
				for(k in nodes) { //for each of the nodes in the nodes data array
					if(layeredNodesGraph[i][j].id == nodes[k].id) {
						nodes[k].x = layeredNodesGraph[i][j].x;
						nodes[k].y = layeredNodesGraph[i][j].y;
						nodes[k].layer = i;
						nodes[k].indexInLayer = j;
					} else {
						// nodes.push(layeredNodesGraph[i][j]);
					}
				}
			}
		}

		//Transfer layeredNodesGraph info to links data array
		for(i in layeredNodesGraph) { //For each layer
			for(j in layeredNodesGraph[i]) {
				for(k in links) { //for each of the links in the links data array
					//Transfers source data
					if(layeredNodesGraph[i][j].id == links[k].source.id) {
						links[k].source.x = layeredNodesGraph[i][j].x;
						links[k].source.y = layeredNodesGraph[i][j].y;
					}
					//Transfers target data
					if(layeredNodesGraph[i][j].id == links[k].target.id) {
						links[k].target.x = layeredNodesGraph[i][j].x;
						links[k].target.y = layeredNodesGraph[i][j].y;
					}
				}
			}
		}
	}
	
	
	////////////////////////////////////////////////////////////////
	var treeDepth = 0, treeWidth = 0, widthPerNode = 0, heightPerNode = 0;
	function computeTreeCharacteristics() {

		/********************Find max tree depth/layers****************/
		treeDepth = layeredNodesGraph.length;

		/***********************Find max layer width*******************/
		treeWidth = 0;
		for(i in layeredNodesGraph) { //Goes through each node
			if(layeredNodesGraph[i].length > treeWidth) {
				treeWidth = layeredNodesGraph[i].length;
			}
		}

		/**************** Structure as a layered graph ****************/
		widthPerNode = (width / treeWidth) ; //Condense graph
		heightPerNode = (height - 100) / (treeDepth + 1);

		/**************** Structure as a layered graph ****************/
		for(i = 0; i < layeredNodesGraph.length; i++) { //For each layer
			for(j = 0; j < layeredNodesGraph[i].length; j++) { //For each node
				layeredNodesGraph[i][j].x = j * widthPerNode; //Sets x-coordinate for level
				layeredNodesGraph[i][j].y = (-1 * i * heightPerNode); //Sets y-coordinate for level
			}
		}
	}


	















	/////////////////////////////////////////////////////////////////////////////////////
	/*********************************Swapping Code*************************************/
	/*************************************Below*****************************************/
	/////////////////////////////////////////////////////////////////////////////////////
	/* 
	Function mainSwappingDriver: 
	This function houses the call of all main functions and computations for this program 
	*/
	mainSwappingDriver();
	function mainSwappingDriver() {


		//Reduce graph if specified by the user
		reduceLG();

		//Color links of the graph
		colorLinks();

		//Construct 'LayeredNodesGraph' using levels passed from MOG graph
		addTo2DArrayCoverLevel();

		//Compute things such as treeDepth, width, etc.
		computeTreeCharacteristics();

		//Shortens longer names for reading improvement
		shortenNodeNames(); 

		//Centers the graph
		centerGraph(); //Lastly, center the graph

		//Update link and node arrays with layeredNodesGraph data
		updateNodesAndLinks(); 

		//Initially puts heaviest links in the center of the graph, helps cetner overall
		centerHeavyLinks(); 


		var breaker = false; //To break/stop the code in certain conditions
		var numIterations = 0; //Number of swapping-driver iterations
		var improvingCounter = 0; //Counts the number of swapping-driver iterations passed without improving


		let overallWeight = getLinkWeights(); //Holds weight of graph
		var initialWeight = overallWeight; //Gets initial weight
		var pastWeights = new Array(); //Holds past crossing amounts
		var minWeight = overallWeight; //Holds initial minimum wight product


		/********************************************************************************************/
		/********************************************************************************************/
		/********************************************************************************************/
		/********************************************************************************************/

		let bestGraphClone = JSON.parse(JSON.stringify(layeredNodesGraph));

		/* Swapping Driver Code */
		swappingDriver(swappingEnabled);
		function swappingDriver(swappingEnabledBool) {
			let start = new Date(); //Used for timing

			while(getLinkWeights() != 0 && swappingEnabledBool == true) {
				console.log('iter')

				//Functions for swapping of crossings and nodes
				MinimizeCrossingsForwards(forwardsCrossingBool);
				//Heurtistic for swapping backwards every so often
				if(numIterations % 3 == 0) {
					MinimizeCrossingsBackwards(backwardsCrossingBool);
				}
				MinimizeCrossingsSideways(sidewaysCrossingBool);

				pastWeights.push(overallWeight); //Holds previous amount of crossings
				overallWeight = getLinkWeights(); //Update number of crossings after swap

				//Change new minimum if necessary
				if(overallWeight < minWeight) {
					minWeight = overallWeight;
					improvingCounter = 0; //Reset counter
					bestGraphClone = JSON.parse(JSON.stringify(layeredNodesGraph));
				}

				//If it goes 100 loops without improving, break
				if(improvingCounter > 100 && breaker == false) {
					breaker = true;
					console.log("mininmum weight has not improved for 100 loops, breaker switched to true");
				}

				//End crossing swapping when we find minimum again
				//Increments comparison number so it will eventually end
				if(overallWeight <= (minWeight + (numIterations * 10) ) && breaker == true) {
					console.log("loop broken @ iteration #" + numIterations + " w/ weight = " + overallWeight);
					break;
				}

				improvingCounter++; //Holds number of loops thus far (without a new minimum)
				numIterations++;

				let end = new Date(); //Used for timing
				//Prevent code from running forever (10000 (ms) = 10 seconds)
				if(numIterations > 200 || end - start > 7000) {
					console.log("ending due to timing");
					break;
				}
			}
		}
		/////////////////////////////////////////////////////////////////////////////////////
		/*********************************Swapping Code*************************************/
		/*************************************Above*****************************************/
		
		
		//Swaps to best graph found
		layeredNodesGraph = JSON.parse(JSON.stringify(bestGraphClone));

		//Updates 'nodes' and 'links' to match
		updateNodesAndLinks();
		getLinkWeights();

		//Final operations
		resortLayeredNodesGraph(); //Updates nodes and link indices, etc (for visual mouseovers and such)

		//Records final weight counting
		pastWeights.push(getLinkWeights());
		
		//If the final weight turns out to be wrose than the initial graph, revert back
		if(initialWeight <= pastWeights.pop() && swappingEnabled) {
			console.log("Final weight is larger than initial weight, swapping back to orignal and centering heavy links...");
			
			//Go back to original graph
			let lengthX = layeredNodesGraph.length
			for(k = 0; k < lengthX; k++) {
				layeredNodesGraph.pop();
			}
			for(k = 0; k < bestGraphClone.length; k++) {
				layeredNodesGraph.push(bestGraphClone[k]);
			} //end copying

			updateNodesAndLinks(); //Update link and node arrays with layeredNodesGraph data

			pastWeights.push(getLinkWeights()); //Pushes overall weight to array

		} //swappingDriver ended


		//Calculate final weight products and output final data
		var finalW = getLinkWeights();
		console.log("--------_______FINAL________---------");
		console.log("initial weight: " + initialWeight);
		console.log("overall weight after swapping graph: " + finalW);
		console.log("Iterations it took: " + numIterations);
		console.log(pastWeights);
	} //main Driver code ended
	/***********************************************************************************/
	/***********************************************************************************/
	/***********************************************************************************/
	/***********************************************************************************/

	
























	/////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////
	//Minimizes crossings in a top-to-bottom manner
	function MinimizeCrossingsForwards (edgeSwappingEnabled = true) {
		//Don't do anything if no crossings
		if(getLinkWeights() == 0) {
			console.log("No crossings")
			return; 
		}

		//Go through links and find crossings
		for(i = 0; i < links.length; i++) {
			for(j = i + 1; j < links.length; j++) {

				if( links[i].source.layer == links[j].source.layer ) { //If sources are on same level, we can possibly swap them
					
					//Check if the links are crossing
					if( (links[j].target.x < links[i].target.x && links[j].source.x > links[i].source.x) || 
					(links[j].target.x > links[i].target.x && links[j].source.x < links[i].source.x) ) 
					{
						
						//Swap nodes
						if(edgeSwappingEnabled) {
							if(debugging) {		
								console.log("Swapping " + links[i].source.id + " and " + links[j].source.id)
							}					
							//Get the weightProduct of the crossing links
							var crossingValueSum = links[i].linkWeightProduct + links[j].linkWeightProduct;

							var srcLayer = links[i].source.layer;

							var aX = layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].x;
							layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].x = layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].x;
							layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].x = aX;

							/////////////////////////////////////////////////////////////////////////////////////////
							//Predicts new weights, swaps back if not a good swap
							getLinkWeights(layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].linksIndices, 
								layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].linksIndices); //Get new weight products of crossing links

							var newCrossingValueSum = links[i].linkWeightProduct + links[j].linkWeightProduct;

							//Swap back if weightProduct increased
							if(newCrossingValueSum > crossingValueSum) {
								var aX = layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].x;
								layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].x = layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].x;
								layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].x = aX;
								getLinkWeights(layeredNodesGraph[srcLayer][ links[i].source.indexInLayer ].linksIndices, 
									layeredNodesGraph[srcLayer][ links[j].source.indexInLayer ].linksIndices);
							}
						}
					}			
				}		
			}
		}
		updateNodesAndLinks(); //Update arrays
	} //MinimizeCrossingsForwards

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////
	//Minimizes crossings in a bottom-to-top manner
	function MinimizeCrossingsBackwards (edgeSwappingEnabled = true) {
		//Don't do anything if no crossings
		if(getLinkWeights() == 0){
			return; //Don't do anything if no crossings
		}

		//Go through links and find crossings
		for(i = links.length - 1; i > 0; i--) {
			for(j = i - 1; j > 0; j--) {

				if( links[i].target.layer == links[j].target.layer ) { //If sources are on same level
								
					//Check if the links are crossing
					if( (links[j].target.x < links[i].target.x && links[j].source.x > links[i].source.x) || 
					(links[j].target.x > links[i].target.x && links[j].source.x < links[i].source.x) ) 
					{
						//Swap nodes
						if(edgeSwappingEnabled) {		
							if(debugging) {		
								console.log("Swapping " + links[i].target.id + " and " + links[j].target.id)
							}		
							//Get the weightProductof the crossing links
							var crossingValueSum = links[i].linkWeightProduct + links[j].linkWeightProduct;

							var tgtLayer = links[i].target.layer; //Layer of nodes to swap

							var aX = layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].x;
							layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].x = layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].x;
							layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].x = aX;

							/////////////////////////////////////////////////////////////////////////////////////////
							//Gets new weights, swaps back if not a good swap
							getLinkWeights(layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].linksIndices, 
								layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].linksIndices); //Get new weight products of crossing links

							var newCrossingValueSum = links[i].linkWeightProduct + links[j].linkWeightProduct;

							//Swap back if weightProduct increased
							if(newCrossingValueSum > crossingValueSum) {

								var aX = layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].x;
								layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].x = layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].x;
								layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].x = aX;

								//Update links after reswapping
								getLinkWeights(layeredNodesGraph[tgtLayer][ links[i].target.indexInLayer ].linksIndices, 
									layeredNodesGraph[tgtLayer][ links[j].target.indexInLayer ].linksIndices); //Get new weight products of crossing links
							}
						}
					}	
				}
			}
		}
		updateNodesAndLinks(); //Update arrays
	} //MinimizeCrossingsBackwards

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////
	//Minimizes crossings in a sideways manner, per layer
	function MinimizeCrossingsSideways (edgeSwappingEnabled = true) {
		//Don't do anything if no crossings
		if(getLinkWeights() == 0){
			return; 
		}

		for(i = 0; i < layeredNodesGraph.length; i++) { //For each layer of the graph
			
			for(j = 0; j < layeredNodesGraph[i].length - 1; j++) { //For each node in said layer

				if(layeredNodesGraph[i][j].layer == layeredNodesGraph[i][j+1].layer) { //Looks at pairs of nodes

					//Compare the links between these nodes
					for(y in layeredNodesGraph[i][j].linksIndices) { //For all links of the first node
						for(z in layeredNodesGraph[i][j+1].linksIndices) { //For all links of the second node 

							var jIndex = -1, jPlusOneindex = -1;
							jIndex = layeredNodesGraph[i][j].linksIndices[y]; //Index in links array, of first node in pair
							jPlusOneIndex = layeredNodesGraph[i][j+1].linksIndices[z]; //Index in links array, of second node in pair

							//Swap nodes in pair if crossing
							if( (links[jPlusOneIndex].target.x < links[jIndex].target.x && links[jPlusOneIndex].source.x > links[jIndex].source.x) 
							|| (links[jPlusOneIndex].target.x > links[jIndex].target.x && links[jPlusOneIndex].source.x < links[jIndex].source.x) )
							{

								//Get the weight/value of the crossing links
								var crossingValueSum = links[jIndex].linkWeightProduct + links[jPlusOneIndex].linkWeightProduct;
								
								//Swap nodes with these crossing links
								var aX = layeredNodesGraph[i][j].x;
								layeredNodesGraph[i][j].x = layeredNodesGraph[i][ j+1 ].x;
								layeredNodesGraph[i][ j+1 ].x = aX;
								
								/////////////////////////////////////////////////////////////////////////////////////////
								//Gets new weights, swaps back if not a good swap
								getLinkWeights(layeredNodesGraph[i][j].linksIndices, layeredNodesGraph[i][ j+1 ].linksIndices); //Get new weight products of crossing links
								
								var newCrossingValueSum = links[jIndex].linkWeightProduct + links[jPlusOneIndex].linkWeightProduct;

								//Swap back if weightProduct increased
								if(newCrossingValueSum > crossingValueSum) {
									var aX = layeredNodesGraph[i][ j+1 ].x;
									layeredNodesGraph[i][ j+1 ].x = layeredNodesGraph[i][j].x;
									layeredNodesGraph[i][j].x = aX;
								}
							}
						}
					}
				}
			}
			//Continues to next layer
		}
		updateNodesAndLinks(); //Update arrays
	} //MinimizeCrossingsSideways

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////
	//Resort layeredNodesGraph depending on x values - updates indices
	function resortLayeredNodesGraph() {
		return;
		for(i in layeredNodesGraph) { //Per layer
			//Sort the layers based on their new x coordinates
			layeredNodesGraph[i].sort(function(a, b) {
				return a.x - b.x;
			});

			//Update indexInLayer
			for(j = 0; j < layeredNodesGraph[i].length; j++) {
				layeredNodesGraph[i][j].indexInLayer = j;
			}
		}
		updateNodesAndLinks();
		getLinkWeights();
	}

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////
	// Center heavier weighted links
	function centerHeavyLinks() {
		if(centerHeavyLinksUser != true) {
			return;
		}

		resortLayeredNodesGraph(); //Updates indices and such

		for(i = 0; i < layeredNodesGraph.length; i++) {

			//Initial sort by link weight
			layeredNodesGraph[i].sort((a, b) => {
				//Get heaviest node 'a' link weight
				let aLinkWeight = 0;
				for(y = 0; y < links.length; y++) {
					if( links[y].source.id == a.id || links[y].target.id == a.id) {
						if(links[y].value > aLinkWeight) {
							aLinkWeight = links[y].value;
						}
					}
				}
				//Get heaviest node 'b' link weight
				let bLinkWeight = 0;
				for(y = 0; y < links.length; y++) {
					if( links[y].source.id == b.id || links[y].target.id == b.id) {
						if(links[y].value > bLinkWeight) {
							bLinkWeight = links[y].value;
						}
					}
				}
				// console.log(i, ' ', a.id, ':', aLinkWeight, ' ', b.id, ':', bLinkWeight)
				if(aLinkWeight < bLinkWeight) {
					return 1;
				} else {
					return -1;
				}
			})
		}


		updateNodesAndLinks(); //Update arrays

		//Update linkWeights after this
		getLinkWeights();
		resortLayeredNodesGraph();
	} //centerheavyLinks


	//////////////////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////////////////
	//Gets weight of crossings, given some links' indices to update
	//If given no link parameters, update the entire graph
	function getLinkWeights(aLinksIndices = new Array(), bLinksIndices = new Array()) {

		//'Reset' some specific links and tag them to be updated
		if(aLinksIndices.length) {			
			//First node's links
			for(indxA in aLinksIndices) {
				links[ aLinksIndices[indxA] ].linkWeightProduct = 0;
				links[ aLinksIndices[indxA] ].taggedToBeUpdated = 1;
			}
			//Second node's links
			for(indxB in bLinksIndices) {
				links[ bLinksIndices[indxB] ].linkWeightProduct = 0;
				links[ bLinksIndices[indxB] ].taggedToBeUpdated = 1;
				
			}
		}
		//Else, reset all links and tag all links to be updated
		else {
			//Reset link weight products
			for(n = 0; n < links.length; n++) {
				links[n].linkWeightProduct = 0;
				links[n].taggedToBeUpdated = 1;
			}
		} 

		//Get current weight products of links that need to be updated
		for(n = 0; n < links.length; n++) { //for each link
			
			for(k = n + 1; k < links.length; k++) { //for every link after it

				//Only update newly reset links, or entire graph if no parameters are passed
				if( links[n].taggedToBeUpdated == 1 || links[k].taggedToBeUpdated == 1 || true) { 

					if(links[n].source.layer == links[k].source.layer) {

						//Links headed for same target and/or with same source should not be crossing
						if( (links[n].source.id != links[k].source.id) && (links[n].target.id != links[k].target.id) ) {
							let boolCross = true; //If these links need to be swapped


							//line from p0p1(a,b)->(c,d) intersects with (p,q)->(r,s)
							let a = (links[k].source.x), b = (links[k].source.y), c = (links[k].target.x), d = (links[k].target.y);
							let p = (links[n].source.x), q = (links[n].source.y), r = (links[n].target.x), s = (links[n].target.y);

							var det, gamma, lambda;
							det = (c - a) * (s - q) - (r - p) * (d - b);
							if (det === 0) {
								boolCross = false;
							} else {
								lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
								gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
								boolCross = (0 < lambda && lambda < 1) && (0 < gamma && gamma < 1);
							}
							
							//Cross products
							// let other = links[k]
							// let thiss = links[n]
							// let vector1 = [ (other.source.x - thiss.source.x), (other.source.y - thiss.source.y)]
							// let vector2 = [ (thiss.target.x - thiss.source.x), (thiss.target.y - thiss.source.y)]
							// let vector3 = [ (other.target.x - thiss.source.x), (other.target.y - thiss.source.y)]

							// let z1 = (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])
							// let z2 = (vector2[0] * vector3[1]) - (vector2[1] * vector3[0])
							
							// if(z1 * z2 < 0) {
							// 	boolCross = false;
							// } else {
							// 	let vector4 = [ (thiss.source.x - other.source.x), (thiss.source.y - other.source.y)]
							// 	let vector5 = [ (other.target.x - other.source.x), (other.target.y - other.source.y)]
							// 	let vector6 = [ (thiss.target.x - other.source.x), (thiss.target.y - other.source.y)]

							// 	let z3 = (vector4[0] * vector5[1]) - (vector4[1] * vector5[0])
							// 	let z4 = (vector5[0] * vector6[1]) - (vector5[1] * vector6[0])

							// 	if(z3 * z4 < 0) {
							// 		boolCross = false;
							// 	}
							// }

							//Links crossing should be in the same layer
							if(boolCross) {
								//Links are crossing
								links[n].linkWeightProduct += links[n].value; 
								links[k].linkWeightProduct += links[k].value; 
							} 
						}
					}
				}
			}
		}

		//Gets overall graph weight to return
		var overallgraphWeight = 0;
		for(n in links) {
			overallgraphWeight += links[n].linkWeightProduct
			links[n].taggedToBeUpdated = 0; //Updating done
		}

		return overallgraphWeight;
	} //getLinkWeights()


	//Exits program (debugging purposes)
	function exit() {
		throw new Error("Process stopped");
	}






	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/*************************************** Rendering/graphing code below ********************************************/
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	/////////////////////////////////////////////////////////////////////////////
	//Shorten labels if string is long
	function shortenNodeNames() {
		for(i in nodes) {
			var curLabel = nodes[i].id;
			if(curLabel.length > 3 && !curLabel.includes("intermNode") ) {

				var newLabel = ""; //Label for the new node
				
				//Only add number at end of a mapper node
				var indexNum = curLabel.lastIndexOf("_")
				var numSubstr = curLabel.substring(indexNum+1, curLabel.length)

				newLabel += numSubstr

				nodes[i].newId = newLabel
			} 
			//Intermediate nodes
			else if(curLabel.length > 3 && curLabel.includes("intermNode")) {
				nodes[i].newId = curLabel;
				var n = curLabel.indexOf("->");
				var m = curLabel.lastIndexOf("_");

				var newLabel = ""; //Label for the new node
				newLabel += "i";
				newLabel += curLabel[n-2];
				newLabel += curLabel[n-1];
				newLabel += ",";
				newLabel += curLabel[m+1];
				newLabel += curLabel[m+2];

				nodes[i].newId = newLabel
			} 
			//Anything else
			else {
				var newLabel = ""; //Label for the new node
				newLabel += (curLabel[0]) 
				newLabel += (curLabel[1]) 
				newLabel += (curLabel[2]) 
				nodes[i].newId = newLabel
			}
		}
	}

	///////////////////////////////////////////////////////////////////////////////////////////
	/************************************ Graph Centering ************************************/
	/************************************ and formatting ************************************/
	//Centers the graph
	function centerGraph() {

		if(!centeredBool) {
			return;
		}
		//Graph Centering data

		//Center the graph
		for(i = 0; i < layeredNodesGraph.length; i++) { //For each layer
			var spacingBetweenNodes = width / layeredNodesGraph[i].length;
			if(layeredNodesGraph[i].length < 10) {
				spacingBetweenNodes /= layeredNodesGraph[i].length;
			}

			var centerNodeIndexA, centerNodeIndexB, centerNodeIndex;

			////////////////////////////////////////////////
			//Sets center nodes for even or odd length layers
			
			//Even num of nodes in layer
			if(layeredNodesGraph[i].length % 2 == 0 && layeredNodesGraph[i].length != 0) { 
				//Two nodes surround center
				centerNodeIndexA = (layeredNodesGraph[i].length / 2 ) - 1; //Center node index A (one to the left of center)
				centerNodeIndexB = layeredNodesGraph[i].length / 2; //Center node index A (one to the left of center)

				//Sets the coordinates of the center nodes
				layeredNodesGraph[i][centerNodeIndexA].x = centerOfGraph - (spacingBetweenNodes / 2);
				layeredNodesGraph[i][centerNodeIndexB].x = centerOfGraph + (spacingBetweenNodes / 2);

				//Center the remaining nodes
				for(j = 0; j < layeredNodesGraph[i].length; j++) { //For each node in the EVEN layer
					if(j != centerNodeIndexA && j != centerNodeIndexB) { //Only modify nodes that are not center nodes
						if(j < centerNodeIndexA) { //Place to the left of center
							layeredNodesGraph[i][j].x = centerOfGraph - (spacingBetweenNodes * ( (centerNodeIndexA - j) + 1)) + (spacingBetweenNodes / 2);
						}
						if(j > centerNodeIndexB) { //Place to the right of center
							layeredNodesGraph[i][j].x = centerOfGraph + (spacingBetweenNodes * ( (j - centerNodeIndexB) + 1)) - (spacingBetweenNodes / 2);
						}
					}
				}

			} 
			//Odd number of nodes in layer
			else if(layeredNodesGraph[i].length % 2 == 1) { 
				//Place center node in center
				centerNodeIndex = Math.ceil(layeredNodesGraph[i].length / 2) - 1; //Center node index (-1 needed)
				layeredNodesGraph[i][centerNodeIndex].x = centerOfGraph;

				//Center the remaining nodes
				for(j = 0; j < layeredNodesGraph[i].length; j++) { //For each node in the ODD layer

					if(j != centerNodeIndex) { //Only modify nodes that are not center nodes
						if(layeredNodesGraph[i][j].x < centerOfGraph) { //Place to the left of center
							layeredNodesGraph[i][j].x = centerOfGraph - (spacingBetweenNodes * (centerNodeIndex - j));
						}
						if(layeredNodesGraph[i][j].x > centerOfGraph) { //Place to the right of center
							layeredNodesGraph[i][j].x = centerOfGraph + (spacingBetweenNodes * (j - centerNodeIndex));
						}
					}
				}
			}
		}
		updateNodesAndLinks(); //Transfer layeredNodesGraph array data to nodes for d3 usage

		//Append single nodes to top of graph (formatting)
		for(i = 0; i < layeredNodesGraph[0].length; i++) {
			// layeredNodesGraph[0][i].y -= 20 * (i % 6);

			layeredNodesGraph[0][i].x /= 2;
			layeredNodesGraph[0][i].x += (width / 4);

		}
		updateNodesAndLinks();
	}

	///////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////////////////////////////////
	//d3 graphing code	

	//Run the FDEB algorithm using default values on the data
	const curve = d3.line().curve(d3.curveBasis);

	//Tooltip for nodes
	var tooltipNode = d3.select("body").append("div")
		.attr("class", "tooltipNode")
		.style("opacity", 0)
		.style("background-color", "rgba(255,255,255,0.7)")
		.style("border", "2px solid blue")
		.style("border-radius", "1px");

	//Tooltip for nodes
	var tooltipLink = d3.select("body").append("div")
		.attr("class", "tooltipLink")
		.style("background-color", "rgba(255,255,255,0.7)")
		.style("border-radius", "1px");

	// Use a timeout to allow graph to load first
	d3.timeout(function() {
		removeProgress();


		/////////////////////////////////////////////////
		//Edges
		links.forEach(function(d) {
			//Points for the curved edge
			var midPoint_1 = [(d.source.x + d.target.x) / 2, (d.source.y + d.target.y) / -2];
			var midPoint_2 = [(d.source.x + d.target.x) / 2, (d.source.y + d.target.y) / -2];
			if(curvedEdges) {
				midPoint_1[0] += 15; //Change the edge curve x-coord slightly
				midPoint_2[0] += 10; //Change the edge curve x-coord slightly
			}
			if(bundleEdges) {
				midPoint_1 = [d.source.x, (-1 * d.source.y) + (heightPerNode / 2)];
				midPoint_2 = [d.target.x, (-1 * d.source.y) + (heightPerNode / 2)];
			}
			var points = [ 
				[d.source.x, (-1 * d.source.y)],
				midPoint_1, //Midpoint to curve edge slightly
				midPoint_2, //Second midpoint to curve edge in s-shape
				[d.target.x, (-1 * d.target.y)] 
			];

			//Append edges
			g.append("g")
				.append('path')
				.attr("stroke", myColors(d.colorCode))
				.attr('fill', 'none')
				.attr("stroke-width",  Math.log(d.value) + 0.5)
				.attr("d", curve(points) )
			
			//////////////////////////////////////////////
			//Append areas around edges for selection ease
			g.append("g")
				// .data(links)
				.append('path')
				.attr("stroke", function (d) { 
					return "gray";
				})
				.attr('fill', 'none')
				.style("opacity", 0.05)
				.attr("stroke-width", Math.log(d.value) + 2)
				.attr("d", curve(points) )
				.data(links)
			.on('mouseover', function (i) {
				tooltipLink.transition()
					.style("opacity", 1);
				tooltipLink.html(d.source.id + "[" + d.source.layer + "][" + d.source.indexInLayer + "]" +
								"==>" + d.target.id + "[" + d.target.layer + "][" + d.target.indexInLayer + "]" +
								"</br> (" + d.source.x +", " + d.source.y + ") -> (" + d.target.x + ", " + d.target.y + ")</br>" + 
								"Value/Weight: " + d.value + "</br>" +
								"Weight Product: " + d.linkWeightProduct)
						.style("position", "absolute")
						.style("left",  (d3.event.pageX + 30) + "px")
						.style("top", (d3.event.pageY + 30) + "px");
			})
			.on('mouseout', function (i) {
				tooltipLink.transition()
					.style("opacity", 0);
			})
			.on("mousemove", function(d) {
				tooltipLink
					.style("position", "absolute")
					.style("left",  (d3.event.pageX + 30) + "px")
					.style("top", (d3.event.pageY + 30) + "px");
			})

		} ) //forEach

		////////////////////////////////
		//Nodes, append a group 'g' of nodes
		g.append("g")
			.attr("stroke", "#fff")
			.attr("stroke-width", 0.5)
		.selectAll("circle")
			.data(nodes)
		.enter().append("circle")
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return -1 * d.y; })
			.attr("fill", "#ADD8E6")
			.attr("stroke", "black")
			.attr("r", function(d) { 
				if(d.id.includes("intermNode")) {
					return 0
				}
				return ((Math.sqrt(d.components.length)) / 3) + 2; 
			})
			//Tooltip of nodes
			.on('mouseover', function (d, i) {
				d3.select(this).transition()
					.duration(50)
					.attr('fill', '#45b7dc')
					.attr("r", function(d) { return (Math.sqrt(d.components.length)) / 3 + 1 });
				tooltipNode.transition()
					.duration(200)
					.style("opacity", .9);
				tooltipNode.html(d.id + "<br/> (" + 
								Math.round(d.x) + ", " + d.y + ") <br/>" +
								"Layer: " + d.layer + "<br/>" +
								"Index in Layer: " + d.indexInLayer + "<br/>" +
								"Num of Components: " + d.components.length)
					.style("position", "absolute")
					.style("left",  (d3.event.pageX + 30) + "px")
					.style("top", (d3.event.pageY + 30) + "px");

			})
			.on("mouseout", function(d) {	
				d3.select(this).transition()
					.duration(50)
					.attr('fill', '#ADD8E6')
					.attr("r", function(d) { 
						return ((Math.sqrt(d.components.length)) / 3) + 2; 
					});
				tooltipNode.transition()
					.duration(200)
					.style("opacity", 0);
			})
			.on("mousemove", function(d) {
				tooltipNode
					.style("position", "absolute")
					.style("left",  (d3.event.pageX + 30) + "px")
					.style("top", (d3.event.pageY + 30) + "px");
			})
	
		//////////////////////////////////	
		// Labels
		g.append("g")
		.selectAll("text")
			.data(nodes)
		.enter().append("text")
			.attr("font-size", "2px")
			.style("fill", 'black')
			.attr("dx", function(d) { 

				return d.x - 6; 
			})
			.attr("dy", function(d) { return -1 * d.y + 5; })
			.text(function (d) {
				if(d.id.includes("intermNode")) {
					return "";
				} else if(d.newId.length < 5) {
					return d.newId;
				} else {
					return "m";
				}
			})
			//Tooltip of nodes
			.on('mouseover', function (d, i) {
				d3.select(this).transition()
					.duration(50)
					.attr('fill', '#45b7dc')
					.attr("r", function(d) { return (Math.sqrt(d.components.length)) / 3 + 1 });
				tooltipNode.transition()
					.duration(200)
					.style("opacity", .9);
				tooltipNode.html(d.id + "<br/> (" + 
								Math.round(d.x) + ", " + d.y + ") <br/>" +
								"Layer: " + d.layer + "<br/>" +
								"Index in Layer: " + d.indexInLayer + "<br/>" +
								"Num of Components: " + d.components.length)
					.style("position", "absolute")
					.style("left",  (d3.event.pageX + 30) + "px")
					.style("top", (d3.event.pageY + 30) + "px");

			})
			.on("mouseout", function(d) {	
				d3.select(this).transition()
					.duration(50)
					.attr('fill', '#ADD8E6')
					.attr("r", function(d) { return (Math.sqrt(d.components.length)) / 3});
				tooltipNode.transition()
					.duration(200)
					.style("opacity", 0);
			})
			.on("mousemove", function(d) {
				tooltipNode
					.style("position", "absolute")
					.style("left",  (d3.event.pageX + 30) + "px")
					.style("top", (d3.event.pageY + 30) + "px");
			})

	});
});

//End LG_vis
}




///////////////////////////////////////////////////////////////////////////////////////
//Prevent loading if large graph; user can select to load or not
var LG_Graph_Vis = function( graph_data ) {

    let svg = d3.select(lgSVG);
	let filterValue = document.getElementById('lg_node_amount_filter_value').innerHTML;
	

	if( (filterValue * graph_data.nodes.length) < 500 && (filterValue * graph_data.links.length) < 500 ) {
		d3.selectAll("#lgSVG > *").remove();
		LG_Graph_Vis_Helper(graph_data);
	} else {
		d3.selectAll("#lgSVG > *").remove();

		let svg_txt = svg.append("g");
		let svg_width  = $(lgSVG).width();
		let svg_height = $(lgSVG).height();

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
					setTimeout( ()=>LG_Graph_Vis_Helper(graph_data), 10);
				});

		tmp_text.append("tspan").text("Large Graph")
			.attr("dy","-1.2em")
			.attr("x",svg_width/2)
		tmp_text.append("tspan").text("(n: " + Math.floor(filterValue * graph_data.nodes.length) +
									 ", e: " + Math.floor(filterValue * graph_data.links.length) + ")")
			.attr("dy","1.2em")
			.attr("x",svg_width/2)
		tmp_text.append("tspan").text("Click To Load Layered Graph")
			.attr("dy","1.2em")
			.attr("x",svg_width/2)
	}
}