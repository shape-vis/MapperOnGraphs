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
import java.util.List;

import processing.core.PApplet;
import usf.dvl.draw.DColorScheme;
import usf.dvl.draw.DMultiFrame;
import usf.dvl.draw.DObject;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.draw.objects.CheckableBox;
import usf.dvl.draw.objects.OptionListFrame;
import usf.dvl.graph.Graph;
import usf.dvl.tda.mapper.FilterFunction;


public class MainFrame extends DMultiFrame<DObject> {

	private Graph gdata;
	private GraphFrame fdd;
	private ArrayList<MapperFrame> mapper = new ArrayList<MapperFrame>();
	private OptionListFrame selBoxes0, selBoxes1;
	private CheckableBox eqlBox0, eqlBox1;
	private CheckableBox resetBox0, resetBox1;
	
	public MainFrame( PApplet p ) {
		super(p);
	}


	public void setData( Graph _gdata, List<FilterFunction> filterFuncs, ArrayList<SequentialColormap> colmaps ) {
		gdata = _gdata;

		fdd = new GraphFrame( papplet, gdata );
		addFrame(fdd);

		mapper.clear();
		for( FilterFunction f : filterFuncs ) {
			mapper.add( new MapperFrame( papplet, gdata, f, 4, 0.15f ) );
		}
		if( filterFuncs.size() == 1 ) { 
			mapper.add( new MapperFrame( papplet, gdata, filterFuncs.get(0), 5, 0.15f ) );
		}

		for( int i = 0; i < mapper.size(); i++ ){
			mapper.get(i).setColormap( colmaps.get(i%colmaps.size()) );
			mapper.get(i).shift_controls = 200;
			mapper.get(i).hideControls();
			mapper.get(i).matchPositions = true;
		}
		
		addFrames( mapper.get(0) );
		addFrames( mapper.get(1) );

		DColorScheme selCol = DColorScheme.Default.createFillStrokeOnly( papplet.color(100),  papplet.color(0), 2 );
		DColorScheme selTxt = DColorScheme.Default.createFillStrokeOnly( papplet.color(255),  papplet.color(0), 1 );
		DColorScheme uselCol = DColorScheme.Default.createFillStrokeOnly( papplet.color(255),  papplet.color(0), 2 );
		DColorScheme uselTxt = DColorScheme.Default.createFillStrokeOnly( papplet.color(0),  papplet.color(0), 1 );
		
		selBoxes0 = new OptionListFrame(papplet);
		selBoxes0.setColorSchemeSelected( selCol, selTxt );		
		selBoxes0.setColorSchemeUnselected( uselCol, uselTxt );
		
		selBoxes1 = new OptionListFrame(papplet);
		selBoxes1.setColorSchemeSelected( selCol, selTxt );		
		selBoxes1.setColorSchemeUnselected( uselCol, uselTxt );
		
		for( int i = 0; i < mapper.size(); i++ ){
			selBoxes0.addOption( mapper.get(i).filter.getShortName(), i == 0 );
			selBoxes1.addOption( mapper.get(i).filter.getShortName(), i == 1 );
		}

		selBoxes0.disableOption( 1 );
		selBoxes1.disableOption( 0 );
		
		addFrames(selBoxes0,selBoxes1);
		
		eqlBox0 = new CheckableBox(papplet,0);
		eqlBox0.setColorSchemeSelected( selCol, selTxt );		
		eqlBox0.setColorSchemeUnselected( uselCol, uselTxt );
		eqlBox0.setText("Equalize Function");
		eqlBox0.setCallback( this, "equalizeSelected" );
		
		eqlBox1 = new CheckableBox(papplet,1);
		eqlBox1.setColorSchemeSelected( selCol, selTxt );		
		eqlBox1.setColorSchemeUnselected( uselCol, uselTxt );
		eqlBox1.setText("Equalize Function");
		eqlBox1.setCallback( this, "equalizeSelected" );
		
		addFrames( eqlBox0, eqlBox1 );

		resetBox0 = new CheckableBox(papplet,0);
		resetBox0.setColorSchemeSelected( selCol, selTxt );		
		resetBox0.setColorSchemeUnselected( uselCol, uselTxt );
		resetBox0.setText("Reset Layout");
		resetBox0.setCallback( this, "resetView" );
		
		resetBox1 = new CheckableBox(papplet,1);
		resetBox1.setColorSchemeSelected( selCol, selTxt );		
		resetBox1.setColorSchemeUnselected( uselCol, uselTxt );
		resetBox1.setText("Reset Layout");
		resetBox1.setCallback( this, "resetView" );
		
		addFrames( resetBox0, resetBox1 );
	}
	
	public void equalizeSelected( int idx, boolean val) {
		System.out.println( "eql = " + val + " " + idx );
		if( idx == 0 ) mapper.get( selBoxes0.getCurrentSelection() ).setEqualized( val );
		if( idx == 1 ) mapper.get( selBoxes1.getCurrentSelection() ).setEqualized( val );
	}

	public void resetView( int idx, boolean val) {
		System.out.println( "eql = " + val + " " + idx );
		if( idx == 0 ) mapper.get( selBoxes0.getCurrentSelection() ).resetView( );
		if( idx == 1 ) mapper.get( selBoxes1.getCurrentSelection() ).resetView( );
	}
	
	
  public void toggleControlsVisible(){ 
		fdd.toggleControlsVisible();
  }

	
	
	@Override public void update() {

		fdd.setPosition( 705, 0, getWidth()-705, h );
		
		for( int i = 0; i < mapper.size(); i++ ){
			if( fdd.controlsVisible() && (i == selBoxes0.getCurrentSelection() || i == selBoxes1.getCurrentSelection()) ) 
				mapper.get(i).showControls();
			else
				mapper.get(i).hideControls();			
		}
		MapperFrame mframe0 = mapper.get( selBoxes0.getCurrentSelection() );
		mframe0.setPosition( 5, 5, 590, h/2-10 );
		setFrame( 1, mframe0 );
		
		MapperFrame mframe1 = mapper.get( selBoxes1.getCurrentSelection() );
		mframe1.setPosition( 5, h/2+5, 590, h/2-10 );
		setFrame( 2, mframe1 );
		
		selBoxes0.enableAllOptions();
		selBoxes0.disableOption( selBoxes1.getCurrentSelection() );
		selBoxes0.setPosition( 595, 10, 105, 180 );
		eqlBox0.setPosition( 595, 200, 105, 20);
		eqlBox0.setValue( mframe0.isEqualized() );

		selBoxes1.enableAllOptions();
		selBoxes1.disableOption( selBoxes0.getCurrentSelection() );
		selBoxes1.setPosition( 595, h/2+10, 105, 180 );
		eqlBox1.setPosition( 595, h/2+200, 105, 20);
		eqlBox1.setValue( mframe1.isEqualized() );
		
		resetBox0.setValue(false);
		resetBox0.setPosition( 595, 225, 105, 20);
		resetBox1.setValue(false);
		resetBox1.setPosition( 595, h/2+225, 105, 20);
		
	}
	
}

