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

import java.util.ArrayList;

import controlP5.ControlP5;
import controlP5.Controller;
import controlP5.Slider;
import processing.core.PApplet;
import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutFrame;
import usf.dvl.mog.FrameManager;
import usf.dvl.mog.GraphTXT;

public class GraphFrame extends ForceDirectedLayoutFrame {

	ControlP5 cp5;
	
	ArrayList< Controller<?> > controls = new ArrayList< Controller<?> >();
	
	public float curTimestep;
	public float curPullScaleFactor;
	public float curCoulombConstant;
	public float curSpringConstant;
	public float curRestingLength;
	
	public GraphFrame( PApplet p, Graph _g ){
		super( p, _g, true );

		FDDPoints points = new FDDPoints();
		FDDLines  lines  = new FDDLines();
		setData( points, lines );
		setColorScheme( points );
		setLineColorScheme( lines );
		
		enablePointSelection( 8 );
		
		this.curTimestep        = FrameManager.fdlTimestep;
		this.curPullScaleFactor = FrameManager.fdlPullScaleFactor;
		this.curCoulombConstant = FrameManager.fdlCoulombConstant;
		this.curSpringConstant  = FrameManager.fdlSpringConstant;
		this.curRestingLength   = FrameManager.fdlRestingLength;

		

		cp5 = new ControlP5(papplet).setColorForeground(p.color(75,75,100))
				.setColorBackground(p.color(100))
				.setColorActive(p.color(50,50,50));
		cp5.hide();

		Slider s;

		controls.add( cp5.addTextlabel("Force Label").setText("Force Parameters").setColorValue(p.color(0,0,0)) );

		controls.add(s = cp5.addSlider(this,"curTimestep").setValue(curTimestep).setRange(0.01f, 1.0f) );
		s.getCaptionLabel().setColor( p.color(0,0,0) ).toUpperCase(false).setText("Timestep");

		controls.add( s = cp5.addSlider(this,"curPullScaleFactor").setValue(curPullScaleFactor).setRange(0.01f, 50) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Pull Factor");

		controls.add( s = cp5.addSlider(this,"curRestingLength").setValue(curRestingLength).setRange(0.01f, 100) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Spring Length");

		controls.add( s = cp5.addSlider(this,"curSpringConstant").setValue(curSpringConstant).setRange(0.01f, 100) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Spring Constant");

		controls.add( s = cp5.addSlider(this,"curCoulombConstant").setValue(curCoulombConstant).setRange(0.01f, 1000) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Coulomb Constant");
		
		
	    showControls();
	}

	  void showControls(){ cp5.setVisible(true); }
	  void hideControls(){ cp5.setVisible(false); }
	  boolean controlsVisible(){ return cp5.isVisible(); }
	  void toggleControlsVisible(){ cp5.setVisible(!cp5.isVisible()); }
	  void setControlsVisible(boolean visible){ cp5.setVisible(visible); }
	  
	  @Override
	public void setPosition(int u0, int v0, int w, int h) {
		  super.setPosition(u0, v0, w, h);
		  
			int curV = v0 + h - controls.size()*15 - 10;
			for( Controller<?> c : controls ) {
				c.setPosition( u0+w-200, curV );
				curV+= 15;
			}
		  
	  }
	  
	  @Override public void draw() {
		  super.currTimestep		= this.curTimestep;
		  super.currPullScaleFactor = this.curPullScaleFactor;
		  super.currCoulombConstant = this.curCoulombConstant;
		  super.currSpringConstant  = this.curSpringConstant;
		  super.currRestingLength   = this.curRestingLength;
		  super.draw();
	  }
	  
	private class FDDPoints extends DefaultFDLPoints {

		@Override public float getPointSize(int idx) { return 2; }
		@Override public float getStrokeWeight(int idx) { return 2; }

		@Override
		public int getFill( int idx ){

			GraphVertex v = g.nodes.get(idx);
			
			
			double filterVal = (FrameManager.selectedFunction!=null) ? FrameManager.selectedFunction.filter.get(v) : Double.NaN;

			/*
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
			}*/
			
			if( v instanceof GraphTXT.MVertex ) {
				GraphTXT.MVertex mv = (GraphTXT.MVertex)v;
				if( mv.hasProperty("group") ) 
					switch( mv.getPropertyInt("group") ) {
					case 0: return papplet.color(255,0,0);
					case 1: return papplet.color(0,0,255);
					default: return papplet.color(0,0,0);
					}
			}
						

			if( FrameManager.selectedColormap!=null){
				return FrameManager.selectedColormap.getQuantizedColor((float)filterVal);
			}
			return papplet.color( 150 );
		}
		
		@Override 
		public int getStroke( int idx ) {
			
			GraphVertex v = g.nodes.get(idx);
			
			
			double filterVal = (FrameManager.selectedFunction!=null) ? FrameManager.selectedFunction.filter.get(v) : Double.NaN;
			
			if( FrameManager.selectedVertex!=null ){
				if( FrameManager.selectedVertex.cc.contains(v) ) return papplet.color(0); 
				return papplet.color( 250 );
			}
			
			if( FrameManager.selectedInterval!=null ){
				if( FrameManager.selectedInterval.inIntervalInclusive(filterVal) ) return papplet.color(0);
				return papplet.color( 250 );
			}
			
			if( FrameManager.selectedEdgeV0 != null && FrameManager.selectedEdgeV1 != null ){
				boolean in0 = FrameManager.selectedEdgeV0.cc.contains(v);
				boolean in1 = FrameManager.selectedEdgeV1.cc.contains(v);
				if( in0 && in1 ) return papplet.color(0,0,255);
				if( in0 ) return papplet.color(130,0,255);
				if( in1 ) return papplet.color(0,130,255);
				return papplet.color( 150 );
			}
			
			return papplet.color(0);
		}

	}

	private class FDDLines extends DefaultFDLLines {
		@Override public float getLineWeight( int idx ){ return 1; }
		@Override public int getStroke( int idx ){ return papplet.color(100,255); }
	}

}

