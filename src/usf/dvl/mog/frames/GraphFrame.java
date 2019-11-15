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
import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutFrame;
import usf.dvl.mog.FrameManager;

public class GraphFrame extends ForceDirectedLayoutFrame {

	
	public GraphFrame( PApplet p, Graph _g ){
		super( p, _g, true );

		FDDPoints points = new FDDPoints();
		FDDLines  lines  = new FDDLines();
		setData( points, lines );
		setColorScheme( points );
		setLineColorScheme( lines );
		
		enablePointSelection( 8 );
		
		this.currTimestep        = FrameManager.fdlTimestep;
		this.currPullScaleFactor = FrameManager.fdlPullScaleFactor;
		this.currCoulombConstant = FrameManager.fdlCoulombConstant;
		this.currSpringConstant  = FrameManager.fdlSpringConstant;
		this.currRestingLength   = FrameManager.fdlRestingLength;

	}

	private class FDDPoints extends DefaultFDLPoints {

		@Override public float getPointSize(int idx) { return 5; }

		@Override
		public int getFill( int idx ){

			GraphVertex v = g.nodes.get(idx);
			double filterVal = (FrameManager.selectedFunction!=null) ? FrameManager.selectedFunction.filter.get(v) : Double.NaN;

			if( FrameManager.selectedVertex!=null ){
				if( FrameManager.selectedVertex.cc.contains(v) ) return papplet.color(0,0,255); 
				return papplet.color( 150 );
			}
			
			if( FrameManager.selectedInterval!=null ){
				if( FrameManager.selectedInterval.inIntervalInclusive(filterVal) ) return papplet.color(0,0,255);
				return papplet.color( 150 );
			}
			
			if( FrameManager.selectedEdgeV0 != null && FrameManager.selectedEdgeV1 != null ){
				boolean in0 = FrameManager.selectedEdgeV0.cc.contains(v);
				boolean in1 = FrameManager.selectedEdgeV1.cc.contains(v);
				if( in0 && in1 ) return papplet.color(0,0,255);
				if( in0 ) return papplet.color(130,0,255);
				if( in1 ) return papplet.color(0,130,255);
				return papplet.color( 150 );
			}

			if( FrameManager.selectedColormap!=null){
				return FrameManager.selectedColormap.getQuantizedColor((float)filterVal);
			}
			return papplet.color( 150 );
		}

	}

	private class FDDLines extends DefaultFDLLines {
		@Override public float getLineWeight( int idx ){ return 1; }
	}

}

