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
import java.util.ArrayList;

import processing.core.PApplet;
import usf.dvl.draw.color.SequentialColormap;
import usf.dvl.mog.frames.MainFrame;
import usf.dvl.mog.frames.MapperFrame;
import usf.dvl.processing.PFrameApplet;
import usf.dvl.tda.mapper.CoverElement;
import usf.dvl.tda.mapper.Mapper;

public class PAppletMOG extends PFrameApplet<MainFrame> {

	public static void main(String args[]) {
		PApplet.main(new String[] { "usf.dvl.mog.PAppletMOG" });
	}

 

	// adjust these
	public static float fdlRestingLength = 20;
	public static float fdlPointScale = 0.05f;
	public static float fdlTimestep = 0.1f;
	public static float fdlEdgeScale = 0.3f;
	public static float fdlSpringConstant = 50f; // this controls compactness
	public static float fdlPullScaleFactor = 1;
	public static float fdlCoulombConstant = 100; // this controls resistence (changed 100 to airports)


	public static float vsize=0.4f;
	public static float fdmRestingLength = 50;
	public static float fdmCoulombConstant = 500;
	public static float fdmSpringConstant = 7.5f;
	public static float fdmPullScaleFactor = 10;
	public static float fdmTimestep = 0.1f;


	String datapath = "/Users/prosen/Code/MapperOnGraphs/testData/.";
	//String filename = "karate.json";
	//String filename = "miserables.json";
	//String filename = "USair97_out.JSON";
	//String filename = "movies_out.JSON";
	//String filename = "circle_of_science_out.JSON";
	//String filename = "train_bombing_out.JSON";


	public static SequentialColormap selectedColormap = null;
	public static MapperFrame selectedFunction = null;
	public static Mapper.MapperVertex selectedVertex = null;
	public static Mapper.MapperVertex selectedEdgeV0 = null;
	public static Mapper.MapperVertex selectedEdgeV1 = null;
	public static CoverElement selectedInterval = null;

	public static ArrayList<SequentialColormap> colmaps = new ArrayList<SequentialColormap>();


	public PAppletMOG() {
		super( 1600, 900, 8, true );

		colmaps.add(new SequentialColormap(this, 0xfff7fbff,0xffdeebf7,0xffc6dbef,0xff9ecae1,0xff6baed6,0xff4292c6,0xff2171b5,0xff08519c,0xff08306b));
		colmaps.add(new SequentialColormap(this, 0xfff7fcf5,0xffe5f5e0,0xffc7e9c0,0xffa1d99b,0xff74c476,0xff41ab5d,0xff238b45,0xff006d2c,0xff00441b));
		colmaps.add(new SequentialColormap(this, 0xfffff5eb,0xfffee6ce,0xfffdd0a2,0xfffdae6b,0xfffd8d3c,0xfff16913,0xffd94801,0xffa63603,0xff7f2704));
		colmaps.add(new SequentialColormap(this, 0xfffcfbfd,0xffefedf5,0xffdadaeb,0xffbcbddc,0xff9e9ac8,0xff807dba,0xff6a51a3,0xff54278f,0xff3f007d));
		colmaps.add(new SequentialColormap(this, 0xfffff5f0,0xfffee0d2,0xfffcbba1,0xfffc9272,0xfffb6a4a,0xffef3b2c,0xffcb181d,0xffa50f15,0xff67000d));
		colmaps.add(new SequentialColormap(this, 0xfff7fcfd,0xffe5f5f9,0xffccece6,0xff99d8c9,0xff66c2a4,0xff41ae76,0xff238b45,0xff006d2c,0xff00441b));
		colmaps.add(new SequentialColormap(this, 0xfff7fcfd,0xffe0ecf4,0xffbfd3e6,0xff9ebcda,0xff8c96c6,0xff8c6bb1,0xff88419d,0xff810f7c,0xff4d004b));
		colmaps.add(new SequentialColormap(this, 0xfff7fcf0,0xffe0f3db,0xffccebc5,0xffa8ddb5,0xff7bccc4,0xff4eb3d3,0xff2b8cbe,0xff0868ac,0xff084081));
		colmaps.add(new SequentialColormap(this, 0xfffff7ec,0xfffee8c8,0xfffdd49e,0xfffdbb84,0xfffc8d59,0xffef6548,0xffd7301f,0xffb30000,0xff7f0000));
		colmaps.add(new SequentialColormap(this, 0xfffff7fb,0xffece7f2,0xffd0d1e6,0xffa6bddb,0xff74a9cf,0xff3690c0,0xff0570b0,0xff045a8d,0xff023858));
		colmaps.add(new SequentialColormap(this, 0xfffff7fb,0xffece2f0,0xffd0d1e6,0xffa6bddb,0xff67a9cf,0xff3690c0,0xff02818a,0xff016c59,0xff014636));
		colmaps.add(new SequentialColormap(this, 0xfff7f4f9,0xffe7e1ef,0xffd4b9da,0xffc994c7,0xffdf65b0,0xffe7298a,0xffce1256,0xff980043,0xff67001f));
		colmaps.add(new SequentialColormap(this, 0xfffff7f3,0xfffde0dd,0xfffcc5c0,0xfffa9fb5,0xfff768a1,0xffdd3497,0xffae017e,0xff7a0177,0xff49006a));
		colmaps.add(new SequentialColormap(this, 0xffffffe5,0xfff7fcb9,0xffd9f0a3,0xffaddd8e,0xff78c679,0xff41ab5d,0xff238443,0xff006837,0xff004529));
		colmaps.add(new SequentialColormap(this, 0xffffffd9,0xffedf8b1,0xffc7e9b4,0xff7fcdbb,0xff41b6c4,0xff1d91c0,0xff225ea8,0xff253494,0xff081d58));
		colmaps.add(new SequentialColormap(this, 0xffffffe5,0xfffff7bc,0xfffee391,0xfffec44f,0xfffe9929,0xffec7014,0xffcc4c02,0xff993404,0xff662506));
		colmaps.add(new SequentialColormap(this, 0xffffffcc,0xffffeda0,0xfffed976,0xfffeb24c,0xfffd8d3c,0xfffc4e2a,0xffe31a1c,0xffbd0026,0xff800026));
	}


	@Override public void setup() {
		super.setup();

		selectInput( "Select Graph", "fileSelected", new File(datapath) );
	}

	public void fileSelected(File selection) {
		String filename = selection.getAbsolutePath();
		MainFrame mv = new MainFrame(this);
		if( filename.toLowerCase().endsWith(".json") ){
			mv.setData( GraphData.parseJSON( this, filename ) );
		}
		else{
			mv.setData( GraphData.parseTXT( this, filename ) );
		}
		setFrame( mv );			
	}

}

