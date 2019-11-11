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

public class FilterEccentricity extends FilterFunction {

	public FilterEccentricity(Graph graph, float p) {

		DistanceMatrix mat = graph.shortestpath_distance();

		for (int i = 0; i < graph.getNodeCount(); i++ ) {
			put( graph.nodes.get(i), mat.row_max(i) );
		}

		finalize_init();
	}

	public String getName() { return "Eccentricity"; }
	public String getShortName() { return "Eccentricity"; }
}
