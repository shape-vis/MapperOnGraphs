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
package usf.dvl.graph.mapper;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import usf.dvl.graph.Graph;
import usf.dvl.graph.mapper.filter.Filter;


public class Mapper extends Graph {


	protected Filter filter;
	protected Graph graph;
	protected Cover cover;

	protected HashMap<Interval, ArrayList<MapperVertex>> iverts;


	//Mapper on graph data
	public Mapper( Graph _graph, Filter _filter, Cover _cover ) {
		filter = _filter;
		graph = _graph;
		cover = _cover;

		iverts = new HashMap<Interval, ArrayList<MapperVertex>>();
		for( Interval i : cover ) {
			iverts.put( i, calculateIntervalMapperNodes( i ) );
		}

		Set<Interval> visited = new HashSet<Interval>();
		for( Interval i : iverts.keySet() ) {
			visited.add(i);
			for( Interval j : iverts.keySet() ) {
				if( visited.contains(j) ) continue;
				for( MapperEdge e : calculateIntervalEdges(i,j) ) {
					addEdge(e);
				}
			}
		}
	}
	
	private Mapper( Mapper from ) { 
		filter = from.filter;
		graph  = from.graph;
		cover  = from.cover;
		iverts = from.iverts;
	}
	
	
	public Mapper filterGraph( int minCCSize, int minValance ) {
		Mapper ret = new Mapper( this );
		
		HashMap<MapperVertex,MapperVertex> nodeMap = new HashMap<MapperVertex,MapperVertex>(); 
		for( GraphVertex _v : nodes ) {
			MapperVertex v = (MapperVertex)_v;
			if( v.cc.size() < minCCSize && v.getAdjacentCount() < minValance ) continue;
			MapperVertex newV = new MapperVertex( v.cc, v.ival );
			nodeMap.put( v,  newV );
			ret.addVertex( newV );
		}
		
		for( GraphEdge _e : edges ) {
			MapperEdge e = (MapperEdge)_e;
			if( nodeMap.containsKey(e.v0) && nodeMap.containsKey(e.v1) ) {
				ret.addEdge( new MapperEdge( nodeMap.get(e.v0) , nodeMap.get(e.v1), (int)e.w ) );
			}
		}
		
		return ret;
	}


	// calculates all of the mapper nodes for a given interval 
	protected ArrayList<MapperVertex> calculateIntervalMapperNodes( Interval ival ) {
		ArrayList<MapperVertex> ret = calculateIntervalConnectedComponents( ival );
		for (MapperVertex newV : ret) {
			this.addVertex(newV);
		} 
		return ret;
	}


	// calculates the edges between mapper nodes on 2 different intervals
	protected ArrayList<MapperEdge> calculateIntervalEdges(Interval i, Interval j) {
		ArrayList<MapperEdge> ret = new ArrayList<MapperEdge>();

		// don't add edges within the same interval
		if( i == j ) return ret;

		// skip if the intervals don't overlap
		if( !i.overlaps(j) )  return ret;

		// go through every mapper vertex on the 2 intervals
		for( MapperVertex cci : iverts.get(i) ) {
			for( MapperVertex ccj : iverts.get(j) ) {

				// if there is any overlap (i.e. the same graph node in each), add an edge
				int overlap = countOverlap(cci,ccj);
				if( overlap == cci.cc.size() && overlap == ccj.cc.size() ) continue; 

				if( overlap > 0 ) {
					ret.add( new MapperEdge(cci,ccj, overlap) );
				}
			}			
		}
		return ret;
	}


	protected ArrayList<MapperVertex> calculateIntervalConnectedComponents( Interval ival ) {
		Set<GraphVertex> verts = getIntervalGraphNodes( ival );
		ArrayList<MapperVertex> ret = new ArrayList<MapperVertex>();

		while( !verts.isEmpty() ) {
			// Select the first item from the set
			GraphVertex item = null;
			for( GraphVertex v : verts ) { item = v; break; }

			// find connected component 
			Set<GraphVertex> cc = getConnectedComponent( item, verts );

			// remove cc nodes from the set
			verts.removeAll( cc );

			// create a mapper vertex
			ret.add( new MapperVertex(cc, ival) );

		}		  
		return ret;
	}



	// gets the nodes from the original graph that belong to a given interval
	protected Set<GraphVertex> getIntervalGraphNodes( Interval ival ){
		HashSet<GraphVertex> ret = new HashSet<GraphVertex>();
		for( int i = 0; i < graph.getNodeCount(); i++ ) {
			double f = filter.get( graph.getVertex(i) );
			if( ival.inIntervalInclusive(f) ){
				ret.add(graph.getVertex(i));
			}
		}
		return ret;
	}

	// finds all of the nodes connected to [start] that exist in [inVerts]
	protected Set<GraphVertex> getConnectedComponent( GraphVertex start, Set<GraphVertex> inVerts ){
		HashSet<GraphVertex> ret  = new HashSet<GraphVertex>();
		Queue<GraphVertex>   proc = new LinkedList<GraphVertex>();
		proc.add(start);
		while( !proc.isEmpty() ) {
			GraphVertex curr = proc.poll();
			if( ret.contains(curr) ) continue;
			ret.add(curr);
			for( GraphVertex n : curr.getAdjacentVertices() ) { 
				if( inVerts.contains(n) ) proc.add(n);
			}
		}
		return ret;
	}


	// Checks to see if 2 mapper vertices have any overlap (and how much)
	public static int countOverlap(MapperVertex cci, MapperVertex ccj) {
		int cnt= 0;
		for( GraphVertex v : cci.cc ) {
			if( ccj.cc.contains(v) ) 
				cnt++;
		}
		return cnt;
	}






	// special Vertex type for mapper nodes
	public class MapperVertex extends GraphVertex {
		public Set<GraphVertex> cc;
		public Interval ival;
		MapperVertex(Set<GraphVertex> _cc,  Interval _ival){
			cc = _cc;
			ival = _ival;
		}
		@Override public String toString() { return ""; }
	}

	// special Edge type for mapper edges
	public class MapperEdge extends GraphEdge {
		MapperEdge( MapperVertex v0, MapperVertex v1, int overlap ){
			super(v0,v1,overlap);
		}
	}


}