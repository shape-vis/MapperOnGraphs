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

import processing.core.PApplet;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.graph.Graph.GraphEdge;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutFrame;
import usf.dvl.mog.FrameManager;
import usf.dvl.tda.mapper.Mapper;
import usf.dvl.tda.mapper.MapperGraph;
import usf.dvl.tda.mapper.MapperGraph.MapperVertex;

public class MapperForceDirectedLayoutFrame  extends ForceDirectedLayoutFrame {

	private MapperGraph<GraphVertex> mapperG;
	private SequentialColormap colormap;

	@SuppressWarnings("rawtypes")
	MapperForceDirectedLayoutFrame( PApplet p, MapperGraph<GraphVertex> _mapperG, int w, int h ){
		super( p, _mapperG, true );

		mapperG = _mapperG;

		FDMPoints points = new FDMPoints();
		FDMLines  lines  = new FDMLines();
		setData( points, lines );
		setColorScheme( points );
		setLineColorScheme( lines );

		this.currTimestep        = FrameManager.fdmTimestep;
		this.currPullScaleFactor = FrameManager.fdmPullScaleFactor;
		this.currCoulombConstant = FrameManager.fdmCoulombConstant;
		this.currSpringConstant  = FrameManager.fdmSpringConstant;
		this.currRestingLength   = FrameManager.fdmRestingLength;

		enablePointSelection( 8 );
		enableLineSelection(4);

		for( GraphVertex v : mapperG.nodes) {
			fdl.setMass( v, ((MapperVertex)v).cc.size() * 2 );
		}

	}

	@SuppressWarnings("rawtypes")
	public void loadGraph( MapperGraph<GraphVertex> _g, boolean loadDefaultForces ) {
		mapperG = _g;
		super.loadGraph(mapperG, loadDefaultForces);
		for( GraphVertex v : mapperG.nodes) {
			fdl.setMass( v, ((MapperVertex)v).cc.size() * 2 );
		}		
	}


	
	class FDMPoints extends DefaultFDLPoints {

		@SuppressWarnings("unchecked")
		public float getPointSize(int idx){
			if( idx >= mapperG.getNodeCount() ) return 0;
			Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);
			return PApplet.constrain( (float)v.cc.size()*FrameManager.vsize, 2.0f, 8.0f ) ;
			//return PApplet.constrain( (float)v.cc.size()*FrameManager.vsize, 2.0f, 16.0f ) ;
		}
		public int getSetID(int idx){ return 0; }
		
		@SuppressWarnings("unchecked")
		public int getFill( int idx ){
			if( idx >= mapperG.getNodeCount() ) return 0;
			
			Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);

			if( v.ival == FrameManager.selectedInterval ) return papplet.color(0,0,255);
			if( v == FrameManager.selectedVertex ) return papplet.color(0,0,255);
			if( v == FrameManager.selectedEdgeV0 ) return papplet.color(130,0,255);
			if( v == FrameManager.selectedEdgeV1 ) return papplet.color(0,130,255);


			if( idx == getSelectedPoint() ) { return 0; }
			double val = (v.ival.getMin() + v.ival.getMax())/2;  
			return colormap.getQuantizedColor((float)val);

		}
		public int getStroke( int idx ){ return papplet.color(0); }
		public int getShadow( ){ return papplet.color(200); }    
	}



	class FDMLines extends DefaultFDLLines { 
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
			return papplet.color(100,50); 
		}
		public int getShadow( ){ return papplet.color(200); }
	}  


	public void setColormap( SequentialColormap colmaps ) {
		this.colormap = colmaps ;
	}

}
