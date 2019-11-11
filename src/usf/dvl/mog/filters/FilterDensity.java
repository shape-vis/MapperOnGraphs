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
package usf.dvl.mog.filters;

import usf.dvl.common.DistanceMatrix;
import usf.dvl.graph.Graph;
import usf.dvl.tda.mapper.FilterFunction;

public class FilterDensity extends FilterFunction {

	public FilterDensity( Graph graph, float eps) {

		DistanceMatrix mat=graph.shortestpath_distance();

		for (int i = 0; i < graph.getNodeCount(); i++ ){
			Graph.GraphVertex v1 = graph.nodes.get(i);
			put( v1, mat.row_sum_exp_sq(i, eps) );
		}

		/*
		//normalize so that the sum of all values is one
		double sum=0;
		for (int i = 0; i < graph.getNodeCount(); i++ ) {
			Graph.GraphVertex v1 = graph.nodes.get(i);
			sum+=filter.get(v1);
		}

		//reassign the filter value  
		for (int i = 0; i < graph.getNodeCount(); i++ ) {
			Graph.GraphVertex v1 = graph.nodes.get(i);
			double oldval=get(v1); 
			put(v1, oldval/sum);
		}
		*/

		finalize_init();
	}

	public String getName() { return "Density"; }
	public String getShortName() { return "Density"; }
	
}

