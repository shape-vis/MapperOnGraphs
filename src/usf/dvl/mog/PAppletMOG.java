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
package usf.dvl.mog;

import java.io.File;
import processing.core.PApplet;
import processing.event.MouseEvent;

public class PAppletMOG extends PApplet {

	public static void main(String args[]) {
		PApplet.main(new String[] { "usf.dvl.mog.PAppletMOG" });
	}

	FrameManager frameMgr;

	public PAppletMOG() {
		
		frameMgr = new FrameManager( this );
	}

	@Override public void settings() {
		size(1600, 900, P3D);
		smooth(4);
	}
	

	@Override public void setup() {
		frameMgr.setup();
	}

	public void fileSelected(File selection) {
		frameMgr.fileSelected(selection);
	}
	
	@Override public void draw() { frameMgr.draw(); }
	
	@Override public void keyPressed( ) { frameMgr.keyPressed(); } 
	@Override public void mousePressed( ) { frameMgr.mousePressed(); }
	@Override public void mouseReleased( ) { frameMgr.mouseReleased(); }
	@Override public void mouseDragged( ) { frameMgr.mouseDragged(); }
	@Override public void mouseWheel( MouseEvent e ) { frameMgr.mouseWheel(e); }	

}

