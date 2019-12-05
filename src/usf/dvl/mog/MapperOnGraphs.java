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

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphVertex;
import usf.dvl.tda.mapper.Cover;
import usf.dvl.tda.mapper.FilterFunction;
import usf.dvl.tda.mapper.Mapper;



public class MapperOnGraphs extends Mapper<GraphVertex> {
	
	
		public MapperOnGraphs( Graph _g, FilterFunction _filter, Cover _cover) {
			super(_g.nodes, _filter, _cover);
			System.out.println("mapper took " + et.getElapsedTimeMilliseconds() + " ms" );
		}
		
		public MapperOnGraphs(Collection<GraphVertex> _nodes, FilterFunction _filter, Cover _cover) {
			super(_nodes, _filter, _cover);
			System.out.println("mapper took " + et.getElapsedTimeMilliseconds() + " ms" );
		}
		
		@Override 
		protected Collection< Set<GraphVertex> > getClustersInCoverElement( Set<GraphVertex> dElem ) {
			
			ArrayList< Set<GraphVertex> > ret = new ArrayList< Set<GraphVertex> >();

			HashSet<GraphVertex> visited = new HashSet<GraphVertex>();
			
			for( GraphVertex v : dElem ) {
				if( visited.contains(v) ) continue;
				
				Set<GraphVertex> curr = getConnectedComponent(v, dElem);
				
				visited.addAll(curr);
				ret.add( curr );
			}
			
			return ret;
			
		}
		
		// finds all of the nodes connected to [start] that exist in [inVerts]
		private Set<GraphVertex> getConnectedComponent( GraphVertex curr, Set<GraphVertex> dElem ){
			HashSet<GraphVertex> ret  = new HashSet<GraphVertex>();
			Queue<GraphVertex>   proc = new LinkedList<GraphVertex>();
			
			proc.add(curr);
			while( (curr = proc.poll()) != null ) {
				if( ret.contains(curr) ) continue;
				
				ret.add(curr);
				
				for( GraphVertex n : curr.getAdjacentVertices() ) { 
					if( dElem.contains(n) ) proc.add(n);
				}
				
			}
			return ret;
		}		
	

}
