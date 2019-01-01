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
import usf.dvl.graph.mapper.Cover;
import usf.dvl.graph.mapper.Mapper;
import usf.dvl.graph.mapper.Mapper.MapperVertex;
import usf.dvl.graph.mapper.filter.Filter;
import usf.dvl.mog.PAppletMOG;


public class MapperFrame extends DMultiFrame<DFrame> {

	public Filter filter;

	private Mapper mapperG;
	private Cover cover;
	private SequentialColormap colormap;
	private ForceDirectedLayoutFrame fdl; 
	private CoverFrame coverD;
	private Graph graph;


	private boolean selected = false;
	private boolean resetview = false;
	
	public MapperFrame( PApplet p, Graph _graph, Filter _filter, int resolution, float eps ){
		super( p );

		graph  = _graph;
		filter = _filter;

		//filter.enableEqualize();
		filter.enableNormalize();

		cover  = new Cover( filter, resolution, eps );
		coverD = new CoverFrame(p, cover);
		coverD.setHistogram( filter.getHistogram() );
		cover.clearModified();

		mapperG = (new Mapper( graph, filter, cover )).filterGraph(3, 1);
		fdl = new FDL(p, mapperG, 100,100 );


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


	protected class FDL extends ForceDirectedLayoutFrame {

		FDL( PApplet p, Mapper _g, int w, int h ){
			super( p, _g, true );

			FDMPoints points = new FDMPoints();
			FDMLines  lines  = new FDMLines();
			setData( points, lines );
			setColorScheme( points );
			setLineColorScheme( lines );

			this.currTimestep        = PAppletMOG.fdmTimestep;
			this.currPullScaleFactor = PAppletMOG.fdmPullScaleFactor;
			this.currCoulombConstant = PAppletMOG.fdmCoulombConstant;
			this.currSpringConstant  = PAppletMOG.fdmSpringConstant;
			this.currRestingLength   = PAppletMOG.fdmRestingLength;

			enablePointSelection( 8 );
			enableLineSelection(4);
			
			for( GraphVertex v : _g.nodes) {
				fdl.setMass( v, ((MapperVertex)v).cc.size() * 10 );
			}

		}
		
		public void loadGraph( Mapper _g, boolean loadDefaultForces ) {
			super.loadGraph(_g, loadDefaultForces);
			for( GraphVertex v : _g.nodes) {
				fdl.setMass( v, ((MapperVertex)v).cc.size() * 2 );
			}		
		}


		class FDMPoints extends DefaultFDLPoints {
			//public int countPoints(){ return layout.countVertex(); }
			//public float getPointX(int idx){ return mapX( layout.getVertex(idx).getPositionX() ); }
			//public float getPointY(int idx){ return mapY( layout.getVertex(idx).getPositionY() ); }    
			public float getPointSize(int idx){
				Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);
				boolean selected = false;
				//      if( v.ival == selectedInterval ) selected = true;
				//      if( v == selectedVertex ) selected = true;
				//      
				//      if( getSelectedEdge() >= 0 ){
				//        GraphEdge e = gd.edges.get(getSelectedEdge());
				//        if( idx == gd.getVertexIndex(e.v0) ) selected = true;
				//        if( idx == gd.getVertexIndex(e.v1) ) selected = true;
				//      }      
				if( selected ) 
					return PApplet.constrain( (float)v.cc.size()*PAppletMOG.vsize*1.5f, (float)4, (float)12 ) ;
				return PApplet.constrain( (float)v.cc.size()*PAppletMOG.vsize, 2.0f, 8.0f ) ;
			}
			public int getSetID(int idx){ return 0; } 
			public int getFill( int idx ){
				Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);

				      if( v.ival == PAppletMOG.selectedInterval ) return papplet.color(0,0,255);
				      if( v == PAppletMOG.selectedVertex ) return papplet.color(0,0,255);
				      if( v == PAppletMOG.selectedEdgeV0 ) return papplet.color(130,0,255);
				      if( v == PAppletMOG.selectedEdgeV1 ) return papplet.color(0,130,255);
				    	  
				      
				      /*
				      if( fdl.getSelectedLine() >= 0 ){
				        GraphEdge e = gd.edges.get(fdl.getSelectedLine());
				        if( idx == gd.getVertexIndex(e.v0) ) return papplet.color(100,0,255);
				        if( idx == gd.getVertexIndex(e.v1) ) return papplet.color(0,100,255);
				      }
				      */

				if( idx == getSelectedPoint() ) { return 0; }
				double val = (v.ival.getMin() + v.ival.getMax())/2;  
				return colormap.getQuantizedColor((float)val);

			}
			public int getStroke( int idx ){ return papplet.color(0); }
			public int getShadow( ){ return papplet.color(200); }    
		}
		
		

		class FDMLines extends DefaultFDLLines { //DColorScheme.Default implements DLineSet {
			public int [] getLine( int idx ){
				GraphEdge e = mapperG.edges.get(idx);
				return new int[]{mapperG.getVertexIndex(e.v0),mapperG.getVertexIndex(e.v1), 1};
			}

			public int countLines(){ return mapperG.edges.size(); }

			public float getLineWeight( int idx ){
				float w = (float)mapperG.edges.get(idx).w;
				if( getSelectedLine() == idx ) return 10;
				return PApplet.constrain( w*0.5f, 1, 5 );
			}
			public int getFill( int idx ){ return 0; }
			public int getStroke( int idx ){
				if( getSelectedLine() == idx ) return papplet.color(0,0,255);
				return papplet.color(100); 
			}
			public int getShadow( ){ return papplet.color(200); }
		}  
	}




	@Override
	public void update() {
		
		if( cover.isModified() ) {
			//System.out.println("mod");
			
			HashMap<Graph.GraphVertex,ForceDirectedLayoutVertex> old_vertex_map = null, new_vertex_map = null;
			
			old_vertex_map = fdl.fdl.graph2layout;
			
			mapperG = (new Mapper( graph, filter, cover )).filterGraph(3, 1);
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
					int over = Mapper.countOverlap( v, u );
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
			mapperG = (new Mapper( graph, filter, cover )).filterGraph(3, 1);
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
		this.coverD.setColormap(colmaps);
	}

}


