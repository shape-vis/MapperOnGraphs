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
import java.util.HashMap;

import controlP5.Button;
import controlP5.CallbackEvent;
import controlP5.CallbackListener;
import controlP5.ControlP5;
import controlP5.Controller;
import controlP5.Slider;
import controlP5.Textlabel;
import processing.core.PApplet;
import usf.dvl.draw.DMultiFrame;
import usf.dvl.draw.DObject;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphEdge;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.graph.layout.forcedirected.ForceDirectedLayoutVertex;
import usf.dvl.mog.FrameManager;
import usf.dvl.mog.MapperOnGraphs;
import usf.dvl.tda.mapper.Cover;
import usf.dvl.tda.mapper.FilterFunction;
import usf.dvl.tda.mapper.MapperGraph;
import usf.dvl.tda.mapper.MapperGraph.MapperVertex;


public class MapperFrame extends DMultiFrame<DObject> {

	public FilterFunction filter;

	private MapperGraph<GraphVertex> fullMapperG, filteredMapperG;
	
	private Cover cover;
	private SequentialColormap colormap;
	private MapperForceDirectedLayoutFrame fdl; 
	public  CoverFrame coverD;
	private Graph graph;

	ControlP5 cp5;

	ArrayList< Controller<?> > controls = new ArrayList< Controller<?> >();

	private boolean selected = false;
	private boolean resetview = false;
	
	public float currPullScaleFactor = 0;
	public float currTimestep = 0;
	public float currRestingLength = 0;
	public float currSpringConstant = 0;
	public float currCoulombConstant = 0;	
	
	public float filterHits   = 1000;
	public float filterCCSize = 1;
	
	public int resolution;
	public float eps;

	
	public MapperFrame( PApplet p, Graph _graph, FilterFunction _filter, int _resolution, float _eps ){
		super( p );

		graph  = _graph;
		filter = _filter;
		resolution = _resolution;
		eps = _eps;

		//filter.enableEqualize();
		filter.enableNormalize();

		cover  = new Cover( filter, resolution, eps );
		coverD = new CoverFrame(p, cover);
		coverD.setHistogram( filter.getHistogram() );
		cover.clearModified();

		fullMapperG	    = new MapperOnGraphs( graph, filter, cover );
		filteredMapperG = fullMapperG.filterTopHits( (int)Math.round(filterHits) )
									 .filterConnectedComponents( (int)Math.round(filterCCSize) );
		fdl				= new MapperForceDirectedLayoutFrame(p, filteredMapperG, 100,100 );



		addFrame(coverD);
		addFrame(fdl);
		
		cp5 = new ControlP5(papplet).setColorForeground(p.color(75,75,100))
				.setColorBackground(p.color(100))
				.setColorActive(p.color(50,50,50));
		cp5.hide();

		Slider s;

		
		
		controls.add( cp5.addTextlabel("Force Label").setText("Force Parameters").setColorValue(p.color(0,0,0)) );

		controls.add(s = cp5.addSlider(this,"currTimestep").setValue(fdl.currTimestep).setRange(0.01f, 1.0f) );
		s.getCaptionLabel().setColor( p.color(0,0,0) ).toUpperCase(false).setText("Timestep");

		controls.add( s = cp5.addSlider(this,"currPullScaleFactor").setValue(fdl.currPullScaleFactor).setRange(0.01f, 50) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Pull Factor");

		controls.add( s = cp5.addSlider(this,"currRestingLength").setValue(fdl.currRestingLength).setRange(0.01f, 100) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Spring Length");

		controls.add( s = cp5.addSlider(this,"currSpringConstant").setValue(fdl.currSpringConstant).setRange(0.01f, 100) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Spring Constant");

		controls.add( s = cp5.addSlider(this,"currCoulombConstant").setValue(fdl.currCoulombConstant).setRange(0.01f, 1000) );
		s.getCaptionLabel().setColor(p.color(0,0,0) ).toUpperCase(false).setText("Coulomb Constant");

		
		controls.add( cp5.addTextlabel("MapperLabel").setText("Mapper Parameters").setColorValue(p.color(0,0,0)) );
		
		controls.add(s = cp5.addSlider(this, "filterHits").setValue( filterHits ).setRange(1, 2000) );
		s.getCaptionLabel().setColor( p.color(0,0,0) ).toUpperCase(false).setText("Number of Hits");
		s.onRelease( new FilterHits() );

		controls.add(s = cp5.addSlider(this, "filterCCSize").setValue( filterCCSize ).setRange(1, 10) );
		s.getCaptionLabel().setColor( p.color(0,0,0) ).toUpperCase(false).setText("Min CC Size");
		s.onRelease( new FilterCCSize() );
		
		
		//Button b;
		intervalMinus = cp5.addButton("interval -").onRelease( new IntervalMinus() ).setSize(15, 10); 
		intervalMinus.getCaptionLabel().setColor(p.color(255,255,255) ).toUpperCase(false).setText("-");
		
		intervalPlus = cp5.addButton("interval +").onRelease( new IntervalPlus() ).setSize(15, 10);
		intervalPlus.getCaptionLabel().setColor(p.color(255,255,255) ).toUpperCase(false).setText("+");
		
		intervalCount = cp5.addTextlabel("Interval Count").setText( Integer.toString(resolution) ).setColorValue(p.color(0,0,0));
		intervalLabel = cp5.addTextlabel("Interval Label").setText( "# of cover elements" ).setColorValue(p.color(0,0,0));

		epsilonMinus = cp5.addButton("epsilon -").onRelease( new EpsilonMinus() ).setSize(15, 10); 
		epsilonMinus.getCaptionLabel().setColor(p.color(255,255,255) ).toUpperCase(false).setText("-");
		
		epsilonPlus = cp5.addButton("epsilon +").onRelease( new EpsilonPlus() ).setSize(15, 10);
		epsilonPlus.getCaptionLabel().setColor(p.color(255,255,255) ).toUpperCase(false).setText("+");
		
		epsilonCount = cp5.addTextlabel("epsilon Count").setText( Float.toString(eps) ).setColorValue(p.color(0,0,0));
		epsilonLabel = cp5.addTextlabel("epsilon Label").setText( "Interval Overlap" ).setColorValue(p.color(0,0,0));
		
		
		showControls();
		
	}
	
	Button intervalPlus, intervalMinus;
	Textlabel intervalCount, intervalLabel;

	Button epsilonPlus, epsilonMinus;
	Textlabel epsilonCount, epsilonLabel;

	public int shift_controls = 0;

	@Override
	public void setPosition(int u0, int v0, int w, int h) {
		super.setPosition(u0, v0, w, h);

		int curV = v0 + h - controls.size()*15 - 40;
		for( Controller<?> c : controls ) {
			c.setPosition( u0+w-200+shift_controls, curV );
			curV+= 15;
		}
		
		intervalMinus.setPosition( u0+w-190+shift_controls, curV );
		intervalPlus.setPosition(  u0+w-130+shift_controls, curV );
		intervalCount.setPosition( u0+w-165+shift_controls, curV );
		intervalLabel.setPosition( u0+w-100+shift_controls, curV );
		curV+=15;
		
		epsilonMinus.setPosition( u0+w-190+shift_controls, curV );
		epsilonPlus.setPosition(  u0+w-130+shift_controls, curV );
		epsilonCount.setPosition( u0+w-165+shift_controls, curV );
		epsilonLabel.setPosition( u0+w-100+shift_controls, curV );
		curV+=15;
		
	}

	
	
	public void showControls(){ cp5.setVisible(true); }
	public void hideControls(){ cp5.setVisible(false); }
	public boolean controlsVisible(){ return cp5.isVisible(); }
	public void toggleControlsVisible(){ cp5.setVisible(!cp5.isVisible()); }
	public void setControlsVisible(boolean visible){ cp5.setVisible(visible); }
	

	
	private class FilterHits implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			calcNewMapper( false );
		}
	}
	
	private class FilterCCSize implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			calcNewMapper( false );
		}
	}	
	
	private class IntervalMinus implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			resolution--;
			intervalCount.setText( Integer.toString(resolution) );
			calcNewMapper( true );
		}
	}

	private class IntervalPlus implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			resolution++;
			intervalCount.setText( Integer.toString(resolution) );
			calcNewMapper( true );
		}
	}
	
	private class EpsilonMinus implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			eps= Math.max(0,eps-0.0125f);
			String epsStr = Float.toString(eps);
			epsilonCount.setText( epsStr.substring(0,Math.min(5,epsStr.length() ) ) );
			calcNewMapper( true );
		}
	}

	private class EpsilonPlus implements CallbackListener {
		@Override public void controlEvent(CallbackEvent theEvent) {
			eps= Math.min(1,eps+0.0125f);
			String epsStr = Float.toString(eps);
			epsilonCount.setText( epsStr.substring(0,Math.min(5,epsStr.length() ) ) );
			calcNewMapper( true );
		}
	}	
	
	
	
	
	
	@SuppressWarnings({ "rawtypes", "unchecked" })
	private void calcNewMapper( boolean newCover  ) {
		
		HashMap<Graph.GraphVertex,ForceDirectedLayoutVertex> old_vertex_map = null, new_vertex_map = null;

		if( matchPositions ) {
			old_vertex_map = fdl.fdl.graph2layout;
		}

		if( newCover ) {
			cover  			= new Cover( filter, resolution, eps );
			fullMapperG	    = new MapperOnGraphs( graph, filter, cover );
			coverD.updateCover( cover );
		}
		filteredMapperG = fullMapperG.filterTopHits( (int)Math.round(filterHits) )
									 .filterConnectedComponents( (int)Math.round(filterCCSize) );
		fdl.loadGraph(filteredMapperG,true);
		
		fdl.currPullScaleFactor	 = currPullScaleFactor;
		fdl.currTimestep		 = currTimestep;
		fdl.currRestingLength	 = currRestingLength;
		fdl.currSpringConstant	 = currSpringConstant;
		fdl.currCoulombConstant	 = currCoulombConstant;	
		
		fdl.update();				

		if( matchPositions ) {
			new_vertex_map = fdl.fdl.graph2layout;

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
	}
	
	
	public boolean matchPositions = false;



	public void setEqualized(boolean value) {
		if( filter.isEqualized() == value ) return;
		filter.setEqualize(value);
		coverD.setHistogram( filter.getHistogram() );
		cover.setModified();
		calcNewMapper( true );
	}


	public boolean isEqualized() {
		return filter.isEqualized();
	}	

	public void resetView() {
		resetview = true;
	}






	@SuppressWarnings({ "unchecked" })
	@Override
	public void update() {

		fdl.currPullScaleFactor	 = currPullScaleFactor;
		fdl.currTimestep		 = currTimestep;
		fdl.currRestingLength	 = currRestingLength;
		fdl.currSpringConstant	 = currSpringConstant;
		fdl.currCoulombConstant	 = currCoulombConstant;	
		
		/*
		if( cover.isModified() ) {
			calcNewMapper(true,true);
			cover.clearModified();
		}
		*/

		if( resetview ) {
			filteredMapperG = (new MapperOnGraphs( graph, filter, cover )).filterTopHits(1000).filterConnectedComponents(3);
			fdl.loadGraph(filteredMapperG,true);
			fdl.update();
			resetview = false;
		}


		if( selected ){
			FrameManager.selectedVertex = null;
			FrameManager.selectedEdgeV0 = null;
			FrameManager.selectedEdgeV1 = null;
			selected = false;
		}

		if( fdl.getSelectedPoint() >= 0){
			FrameManager.selectedFunction = this;
			FrameManager.selectedColormap = colormap;
			FrameManager.selectedVertex = (MapperOnGraphs.MapperVertex)filteredMapperG.nodes.get( fdl.getSelectedPoint() );
			selected = true;
		}


		if( FrameManager.selectedInterval != null && cover.contains(FrameManager.selectedInterval) ){
			FrameManager.selectedFunction = this;
			FrameManager.selectedColormap = colormap;
			selected = true;
		}


		if( fdl.getSelectedLine() >= 0 ){
			FrameManager.selectedFunction = this;
			FrameManager.selectedColormap = colormap;
			GraphEdge e = filteredMapperG.edges.get( fdl.getSelectedLine() );
			FrameManager.selectedEdgeV0 = (MapperOnGraphs.MapperVertex)filteredMapperG.nodes.get( filteredMapperG.getVertexIndex(e.v0) );
			FrameManager.selectedEdgeV1 = (MapperOnGraphs.MapperVertex)filteredMapperG.nodes.get( filteredMapperG.getVertexIndex(e.v1) );
			selected = true;
		}


		coverD.setPosition( u0, v0, (int)(w*0.125f),  h );

		fdl.setPosition( u0+coverD.getWidth()+10, v0, w-coverD.getWidth()-10,  h );

	}


	/*
	@Override public void draw() {
		super.draw();
		papplet.stroke(0);
		papplet.fill(0);
		papplet.textAlign( PApplet.LEFT, PApplet.BOTTOM );
		papplet.text( filter.getName(), u0+105, v0+12 );
	}
	 */
	
	
	public void setColormap( SequentialColormap colmaps ) {
		this.colormap = colmaps ;
		this.fdl.setColormap( colmaps );
		this.coverD.setColormap(colmaps);
	}

}


