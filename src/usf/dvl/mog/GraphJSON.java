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

import java.util.HashMap;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;
import usf.dvl.graph.Graph;

public class GraphJSON extends Graph {


	private HashMap<String, MultiAttributeVertex> nodeNames = new HashMap<String, MultiAttributeVertex>();

	protected GraphJSON( PApplet p, String filename ) {

		JSONObject data = p.loadJSONObject( filename );

		JSONArray n = data.getJSONArray("nodes");
		for ( int i = 0; i < n.size(); i++ ) {
			addVertex( new MultiAttributeVertex( i, n.getJSONObject(i) ) );
		}

		JSONArray e = data.getJSONArray("links");
		for ( int i = 0; i < e.size(); i++ ) {
			JSONObject ce = e.getJSONObject(i);
			if( ce.getFloat("value") == 0.0f ) continue;
			addEdge( new MEdge( ce.getString("source"), ce.getString("target"), ce.getFloat("value") ) );
		}
	
		System.out.println(filename + " read complete");
		System.out.println( "nodes: " + this.getNodeCount() + " edges: " +  this.getEdgeCount() );
	}
	
	
	public class MultiAttributeVertex extends Graph.GraphVertex { 
		private String name;
		private JSONObject json;

		public MultiAttributeVertex( int id, JSONObject j ){
			json = j;
			name = j.getString("id");
			nodeNames.put( name, this );
		}
		
		public MultiAttributeVertex( int id, String _name ){
			name = _name;
			nodeNames.put( name, this );
		}
		
		public String getName(){ return name; }
		
		public boolean hasProperty( String prop ) {
			return ( json != null && json.hasKey(prop) );
		}
		public String getPropertyString( String prop ) {
			if( json != null && json.hasKey(prop) ) 
				return json.getString(prop);
			return "";			
		}
		public float getPropertyFloat( String prop ) {
			if( json != null && json.hasKey(prop) ) 
				return json.getFloat(prop);
			return Float.NaN;			
		}

		public int getPropertyInt( String prop ) {
			if( json != null && json.hasKey(prop) ) 
				return json.getInt(prop);
			return Integer.MAX_VALUE;			
		}

		@Override public String toString(){ return name; }

	}

	
	class MEdge extends Graph.GraphEdge {
		String src, tgt;

		MEdge( String _src, String _tgt, float _w ){
			w = _w;
			src = _src;
			tgt = _tgt;
			v0 = nodeNames.get( src );
			v1 = nodeNames.get( tgt );
		}
	}
	
}
