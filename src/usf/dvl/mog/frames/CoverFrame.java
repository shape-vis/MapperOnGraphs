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
import java.util.Arrays;

import processing.core.PApplet;
import usf.dvl.common.Histogram1D;
import usf.dvl.draw.DColorScheme;
import usf.dvl.draw.DFrame;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.draw.frames.DHistogram;
import usf.dvl.draw.objects.DragableResizeableBox;
import usf.dvl.graph.mapper.Cover;
import usf.dvl.graph.mapper.Interval;
import usf.dvl.mog.PAppletMOG;

public class CoverFrame extends DFrame {

	private ArrayList<DCover> dcovers = new ArrayList<DCover>();
	private DHistogram hist;

	private SequentialColormap colormap;

	
	public CoverFrame( PApplet p, Cover cover ){
		super( p );
		hist = new DHistogram(p);
		hist.setOrientationVerticalRight();
		
		for( int i = 0; i < cover.size(); i++){
			DCover newD = new DCover( papplet, i, cover.get(i) );
			dcovers.add(newD);
		}
	}


	public void setColormap( SequentialColormap cm ) {
		colormap = cm;
	}
	
	public void setHistogram( Histogram1D _hist ){
		hist.setData(_hist);
	}

	@Override public void setPosition( int u0, int v0, int w, int h ){
		boolean changed = (this.u0!=u0 || this.v0!=v0 || this.w!=w || this.h!=h);

		super.setPosition(u0,v0,w,h);

		if( changed ){
			hist.setPosition( u0+2, v0+2, w/2-5, h-4);

			for( int i = 0; i < dcovers.size(); i++ ){
				DCover c = dcovers.get(i);
				float cv0 = PApplet.map( (float)c.ival.getMin(), 0, 1, v0+h, v0 );
				float cv1 = PApplet.map( (float)c.ival.getMax(), 0, 1, v0+h, v0 );
				c.setPosition( (int)u0+w/2+5, (int)cv1, (int)10, (int)(cv0-cv1) );
				c.lockX();
				c.setConstraintsY(v0,v0+h);
			}     
		}

		int numCol = 0;
		int [] column = new int[dcovers.size()];
		float [] colCover = new float[dcovers.size()];
		Arrays.fill(colCover,v0);
		for( int i = dcovers.size()-1; i >= 0; i-- ){
			DCover c = dcovers.get(i);
			int col = 0;
			while( colCover[col] > c.getV0() ){ col++; }
			colCover[col] = c.getV0() + c.getHeight() + 4;
			column[i] = col;
			numCol = PApplet.max(numCol,col+1);
		}

		float cw = PApplet.min( 15, (w/2-5)/numCol );
		for( int i = 0; i < dcovers.size(); i++ ){
			DCover c = dcovers.get(i);
			float cu = u0+column[i]*cw + w*1/2+5;
			c.setPosition( (int)cu, (int)c.getV0(), (int)cw-2, (int)c.getHeight() );
		}           
	}


	@Override public void draw(){
		drawFrame( papplet.color(100), 1 );
		hist.draw();
		for( DCover c : dcovers ) c.draw();
	}


	@Override public boolean mousePressed( ){
		if( !mouseInside() ) return false;
		for( DCover c : dcovers ){
			if( c.mousePressed() ) {
				return true;
			}
		}
		return true;
	}

	@Override public boolean mouseReleased( ){
		for( DCover c : dcovers ){
			c.mouseReleased();
		}
		PAppletMOG.selectedInterval = null;
		return false;
	}  


	private float mapPositionToValue( int v ){
		return PApplet.map( v, v0, v0+h, 1, 0 );
	}



	private class DCover extends DragableResizeableBox {

		private Interval ival;

		public DCover( PApplet p, int idx, Interval _ival ){
			super(p,idx);
			ival = _ival;
			this.setColorScheme( new CScheme() );
		}
		
		@Override public boolean mousePressed( ){
			if( super.mousePressed() ){
				PAppletMOG.selectedInterval = ival;
				return true;   
			}
			return false;
		}

		@Override public void draw() {
			super.draw();
			if( PAppletMOG.selectedInterval == ival ) ival.setInterval( mapPositionToValue( v0+h ), mapPositionToValue( v0 ) );
		}

		class CScheme extends DColorScheme.Default {
			CScheme(){
				setStroke( true, papplet.color(0), 1 );
				setShadow( false, 0 );
				setFill( true, 0 );
			}
			@Override public int getFill( int idx ){
				int col = colormap.getQuantizedColor( (float)ival.getMid() );
				if( PAppletMOG.selectedVertex!=null && PAppletMOG.selectedVertex.ival == ival )
					col = papplet.color(0,0,255);
				if( PAppletMOG.selectedInterval == ival )
					col = papplet.color(0,0,255);
				if( PAppletMOG.selectedEdgeV0 !=null && PAppletMOG.selectedEdgeV0.ival == ival )
					col = papplet.color(130,0,255);
				if( PAppletMOG.selectedEdgeV1 !=null && PAppletMOG.selectedEdgeV1.ival == ival )
					col = papplet.color(0,130,255);
				return col;
			}
			
		}

		
	}  
}

