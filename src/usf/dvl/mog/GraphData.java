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

import java.io.IOException;
import java.util.HashMap;
import java.util.Set;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;
import usf.dvl.common.SystemX;
import usf.dvl.graph.Graph;


public class GraphData extends Graph {

	private HashMap<String,Integer> nodeNames = new HashMap<String,Integer>();

	protected GraphData() {	}
	
	protected void addVertex( int i, String id ) {
		addVertex( new MVertex( i, id ) );
	}
	
	protected void addVertex( int i ) {
		addVertex( new MVertex( i, Integer.toString(i) ) );
	}
	
	protected void addEdge( String n0, String n1, float w ) {
		addEdge( new MEdge( n0, n1, w ) );
	}
	
	
	public static GraphData parseJSON( PApplet p, String filename ) {

		GraphData ret = new GraphData();
		JSONObject data = p.loadJSONObject( filename );

		JSONArray n = data.getJSONArray("nodes");
		for ( int i = 0; i < n.size(); i++ ) {
			ret.addVertex( i, n.getJSONObject(i).getString("id") );
		}

		JSONArray e = data.getJSONArray("links");
		for ( int i = 0; i < e.size(); i++ ) {
			JSONObject ce = e.getJSONObject(i);
			if( ce.getFloat("value") == 0.0f ) continue;
			ret.addEdge( ce.getString("source"), ce.getString("target"), ce.getFloat("value") );
		}
		return ret;
	}
	
	public static GraphData parseTXT( PApplet p, String filename ) {

		GraphData ret = new GraphData();
		String [] lines =  p.loadStrings(filename);
		for ( int i = 1; i < lines.length; i++ ) {
			String [] parts = lines[i].split("\\s+");
			if ( parts.length >= 2 ) {
				int v0 = Integer.parseInt(parts[0]);
				int v1 = Integer.parseInt(parts[1]);

				while ( ret.getNodeCount() <= PApplet.max(v0, v1) ) {
					ret.addVertex( ret.getNodeCount() );
				}
				ret.addEdge( Integer.toString(v0), Integer.toString(v1), 1.0f );
			}
		}
		return ret;
	}
	

	public static GraphData parseTXT2( String filename ) throws IOException{

		GraphData ret = new GraphData();
		String lines[] = SystemX.readFileContents(filename);
		
		for( String s : lines ){
			if( s.length() == 0 ) continue;
			String [] parts = s.split(" ");
			if( parts[0].equals("n") ){
				while( ret.getNodeCount() <= Integer.parseInt(parts[1]) ){
					ret.addVertex( ret.getNodeCount() );
				}
			}
			else if( parts[0].equals("e") ){
				ret.addEdge( parts[1], parts[2], Float.parseFloat(parts[3]) );
			}
			else{
				if( parts.length == 1 ){
					while( ret.getNodeCount() <= Integer.parseInt(parts[0]) ){
						ret.addVertex( ret.getNodeCount() );
					}
				}
				else if( parts.length == 3 ){
					int n0 = Integer.parseInt(parts[0]), n1 = Integer.parseInt(parts[1]);
					while( ret.getNodeCount() <= Math.max(n0, n1) ){
						ret.addVertex( ret.getNodeCount() );
					}
					ret.addEdge( Integer.toString(n0), Integer.toString(n1), Float.parseFloat(parts[2]) );
				}
				else {
					System.out.println( "Unknown type (" + filename + "): " + s );
				}
			}
		}

		return ret;
	}
	

	
	
	class MVertex extends Graph.GraphVertex { 
		private String name;
		private HashMap<String,Object> properties = new HashMap<String,Object>(); 
		
		public MVertex( int id, String _name ){
			name = _name;
			nodeNames.put( name, id );
		}
		
		public void setProperty( String prop_name, Object value ) {
			properties.put(prop_name, value);
		}
		
		public Object getProperty( String prop_name ) {
			if( !properties.containsKey(prop_name) ) return null;
			return properties.get(prop_name);
		}
		
		public Set<String> listProperties( ) {
			return properties.keySet();
		}

		public String getName(){ return name; }

		@Override public String toString(){ return name; }

	}

	
	class MEdge extends Graph.GraphEdge {
		String src, tgt;

		MEdge( String _src, String _tgt, float _w ){
			w = _w;
			src = _src;
			tgt = _tgt;
			v0 = getVertex(nodeNames.get( src ));
			v1 = getVertex(nodeNames.get( tgt ));
		}
	}
	
}

