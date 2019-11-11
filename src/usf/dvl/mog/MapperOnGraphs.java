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
	}
	
	public MapperOnGraphs(Collection<GraphVertex> _nodes, FilterFunction _filter, Cover _cover) {
		super(_nodes, _filter, _cover);
	}
	

	@Override 
	protected Collection< Set<GraphVertex> > getClustersInCoverElement( Set<GraphVertex> dElem ) {
		
		ArrayList< Set<GraphVertex> > ret = new ArrayList< Set<GraphVertex> >();

		while( !dElem.isEmpty() ) {
			// Select the first item from the set
			GraphVertex item = null;
			for( GraphVertex v : dElem ) { item = (GraphVertex)v; break; }

			// find connected component 
			Set<GraphVertex> cc = getConnectedComponent( item, dElem );

			// remove cc nodes from the set
			dElem.removeAll( cc );

			// create a mapper vertex
			ret.add( cc );

		}		  
		return ret;
		
	}
	
	// finds all of the nodes connected to [start] that exist in [inVerts]
	private Set<GraphVertex> getConnectedComponent( GraphVertex start, Set<GraphVertex> inVerts ){
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

}
