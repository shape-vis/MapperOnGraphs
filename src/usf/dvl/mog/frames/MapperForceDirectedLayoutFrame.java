package usf.dvl.mog.frames;

import processing.core.PApplet;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.graph.Graph.GraphEdge;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutFrame;
import usf.dvl.mog.PAppletMOG;
import usf.dvl.tda.mapper.Mapper;
import usf.dvl.tda.mapper.MapperGraph;
import usf.dvl.tda.mapper.MapperGraph.MapperVertex;

public class MapperForceDirectedLayoutFrame  extends ForceDirectedLayoutFrame {

	private MapperGraph<GraphVertex> mapperG;
	private SequentialColormap colormap;

	MapperForceDirectedLayoutFrame( PApplet p, MapperGraph<GraphVertex> _mapperG, int w, int h ){
		super( p, _mapperG, true );

		mapperG = _mapperG;

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

		for( GraphVertex v : mapperG.nodes) {
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

		public float getPointSize(int idx){
			Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);
			return PApplet.constrain( (float)v.cc.size()*PAppletMOG.vsize, 2.0f, 8.0f ) ;
		}
		public int getSetID(int idx){ return 0; } 
		public int getFill( int idx ){
			Mapper.MapperVertex v = (Mapper.MapperVertex)mapperG.getVertex(idx);

			if( v.ival == PAppletMOG.selectedInterval ) return papplet.color(0,0,255);
			if( v == PAppletMOG.selectedVertex ) return papplet.color(0,0,255);
			if( v == PAppletMOG.selectedEdgeV0 ) return papplet.color(130,0,255);
			if( v == PAppletMOG.selectedEdgeV1 ) return papplet.color(0,130,255);


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
			return papplet.color(100); 
		}
		public int getShadow( ){ return papplet.color(200); }
	}  


	public void setColormap( SequentialColormap colmaps ) {
		this.colormap = colmaps ;
	}

}
