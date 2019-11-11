/*    Mapper On Graphs: A Mapper-based Topological Data Analysis tool for graphs 
 *    Copyright (C) Paul Rosen 2018-2019
 *    Additional Authors: Mustafa Hajij
 *    
 *    This program is free software: you can redistribute it and/or modify     
 *    it under the terms of the GNU General Public License as published by 
 *    the Free Software Foundation, either version 3 of the License, or 
 *    (at your option) any later version. 
 *     
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 *    GNU General Public License for more details.
 *    
 *    You should have received a copy of the GNU General Public License
 *    along with this program.  If not, see <https://www.gnu.org/licenses/>. 
*/
package usf.dvl.mog.frames;

import java.util.HashMap;

import processing.core.PApplet;
import usf.dvl.draw.DFrame;
import usf.dvl.draw.DMultiFrame;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphEdge;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutFrame;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutVertex;
import usf.dvl.mog.MapperOnGraphs;
import usf.dvl.mog.PAppletMOG;
import usf.dvl.tda.mapper.Cover;
import usf.dvl.tda.mapper.FilterFunction;
import usf.dvl.tda.mapper.Mapper;
import usf.dvl.tda.mapper.MapperGraph;
import usf.dvl.tda.mapper.MapperGraph.MapperVertex;


public class MapperFrame extends DMultiFrame<DFrame> {

	public FilterFunction filter;

	private MapperGraph<GraphVertex> mapperG;
	private Cover cover;
	private SequentialColormap colormap;
	private MapperForceDirectedLayoutFrame fdl; 
	private CoverFrame coverD;
	private Graph graph;


	private boolean selected = false;
	private boolean resetview = false;
	
	public MapperFrame( PApplet p, Graph _graph, FilterFunction _filter, int resolution, float eps ){
		super( p );

		graph  = _graph;
		filter = _filter;

		//filter.enableEqualize();
		filter.enableNormalize();

		cover  = new Cover( filter, resolution, eps );
		coverD = new CoverFrame(p, cover);
		coverD.setHistogram( filter.getHistogram() );
		cover.clearModified();

		//mapperG = (new MapperOnGraphs( graph, filter, cover )).filterGraph(3, 1);
		mapperG = (new MapperOnGraphs( graph, filter, cover ) ).filter(3, 1);
		fdl = new MapperForceDirectedLayoutFrame(p, mapperG, 100,100 );
		


		addFrame(coverD);
		addFrame(fdl);

	}


	public void setEqualized(boolean value) {
		if( filter.isEqualized() == value ) return;
		filter.setEqualize(value);
		coverD.setHistogram( filter.getHistogram() );
		cover.setModified();
	}
	

	public boolean isEqualized() {
		return filter.isEqualized();
	}	

	public void resetView() {
		resetview = true;
	}






	@Override
	public void update() {
		
		if( cover.isModified() ) {
			//System.out.println("mod");
			
			HashMap<Graph.GraphVertex,ForceDirectedLayoutVertex> old_vertex_map = null, new_vertex_map = null;
			
			old_vertex_map = fdl.fdl.graph2layout;
			
			mapperG = (new MapperOnGraphs( graph, filter, cover )).filter(3, 1);
			fdl.loadGraph(mapperG,true);
			new_vertex_map = fdl.fdl.graph2layout;
			
			cover.clearModified();
			fdl.update();
			
			
			for( GraphVertex _v : new_vertex_map.keySet() ) {
				MapperVertex v = (MapperVertex)_v;
				MapperVertex bestMatch = null;
				int bestMatchCount = -1;
				for( GraphVertex _u : old_vertex_map.keySet() ) {
					MapperVertex u = (MapperVertex)_u;
					int over = u.intersect(v).size();
					if( bestMatchCount < over ) {
						bestMatch = u;
						bestMatchCount = over;
					}
				}
				if( bestMatch != null ) {
					System.out.println( "[" + old_vertex_map.get(bestMatch).getPositionX() + " " + old_vertex_map.get(bestMatch).getPositionY() + "] " ); 
					new_vertex_map.get(v).setPosition( old_vertex_map.get(bestMatch).getPositionX(), old_vertex_map.get(bestMatch).getPositionY() );
				}
				
			}
			
			
		}
		
		if( resetview ) {
			mapperG = (new MapperOnGraphs( graph, filter, cover )).filter(3, 1);
			fdl.loadGraph(mapperG,true);
			fdl.update();
			resetview = false;
		}
		
		
		if( selected ){
			PAppletMOG.selectedVertex = null;
			PAppletMOG.selectedEdgeV0 = null;
			PAppletMOG.selectedEdgeV1 = null;
			selected = false;
		}

		if( fdl.getSelectedPoint() >= 0){
			PAppletMOG.selectedFunction = this;
			PAppletMOG.selectedColormap = colormap;
			PAppletMOG.selectedVertex = (Mapper.MapperVertex)mapperG.nodes.get( fdl.getSelectedPoint() );
			selected = true;
		}


		if( PAppletMOG.selectedInterval != null && cover.contains(PAppletMOG.selectedInterval) ){
			PAppletMOG.selectedFunction = this;
			PAppletMOG.selectedColormap = colormap;
			selected = true;
		}


		if( fdl.getSelectedLine() >= 0 ){
			PAppletMOG.selectedFunction = this;
			PAppletMOG.selectedColormap = colormap;
			GraphEdge e = mapperG.edges.get( fdl.getSelectedLine() );
			PAppletMOG.selectedEdgeV0 = (Mapper.MapperVertex)mapperG.nodes.get( mapperG.getVertexIndex(e.v0) );
			PAppletMOG.selectedEdgeV1 = (Mapper.MapperVertex)mapperG.nodes.get( mapperG.getVertexIndex(e.v1) );
			selected = true;
		}


		coverD.setPosition( u0, v0, 100,  h );

		fdl.setPosition( u0+110, v0, w-110,  h );

	}

	
	@Override public void draw() {
		super.draw();

		papplet.stroke(0);
		papplet.fill(0);
		papplet.textAlign( PApplet.LEFT, PApplet.BOTTOM );
		papplet.text( filter.getName(), u0+105, v0+12 );
	}

	public void setColormap( SequentialColormap colmaps ) {
		this.colormap = colmaps ;
		this.fdl.setColormap( colmaps );
		this.coverD.setColormap(colmaps);
	}

}


