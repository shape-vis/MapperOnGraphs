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

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import usf.dvl.graph.Graph;
import usf.dvl.tda.mapper.FilterFunction;

public class GraphFile extends Graph {

	private HashMap< Integer, IntVertex > vertexMap = new HashMap< Integer, IntVertex >();

	private HashMap< String, FilterScalar > scalars = new HashMap< String, FilterScalar >(); 

	public GraphFile( String filename ) throws IOException {

		BufferedReader reader = new BufferedReader(new FileReader( filename ));

		String line;
		while( ( line = reader.readLine() ) != null ) {
			String [] splt = line.split("\\s+");

			if( splt[0].equals("n") ) {
				IntVertex v = new IntVertex( Integer.parseInt(splt[1]) );
				vertexMap.put( v.name, v );
				addVertex( v ); 
			}
			else if( splt[0].equals("e") ) {
				IntEdge e = new IntEdge( Integer.parseInt(splt[1]), Integer.parseInt(splt[2]) );
				addEdge( e );
			}
			else {
				System.out.println(line);
			}
		}
		reader.close();

		System.out.println(filename + " read complete");
		System.out.println( "nodes: " + this.getNodeCount() + " edges: " +  this.getEdgeCount() );
		
	}
	
	public List<FilterFunction> getFilterFunctions(){
		return new ArrayList<FilterFunction>( scalars.values() );
	}
	
	public class FilterScalar extends FilterFunction {

		String name;
		FilterScalar( String _name, String filename ) throws IOException {
			name = _name;
			
			BufferedReader reader = new BufferedReader(new FileReader( filename ));

			String line;
			while( ( line = reader.readLine() ) != null ) {
				String [] splt = line.split("\\s+");

				if( splt[0].equals("n") ) {
					double val = Double.parseDouble(splt[2]);
					if( val > 0 ) val = Math.log(val);
					this.put( vertexMap.get(Integer.parseInt(splt[1])), val );
				}
				else {
					System.out.println(line);
				}
			}
			reader.close();
			
			finalize_init();
		}
		
		@Override public String getName() { return "Scalar: " + name; }
		@Override public String getShortName() { return name; }

	}


	public void loadScalar( String name, String filename ) throws IOException {
		System.out.println(filename);
		scalars.put( name, new FilterScalar( name, filename ) );
	}



	class IntEdge extends Graph.GraphEdge {
		int src, tgt;

		IntEdge( int _src, int _tgt ){
			w = 1;
			src = _src;
			tgt = _tgt;
			v0 = vertexMap.get( src );
			v1 = vertexMap.get( tgt );
		}
	}


	class IntVertex extends Graph.GraphVertex {
		int name;
		IntVertex( int _name ){
			name = _name;
		}

		public double getScalar( String fieldName ) {
			if( !scalars.containsKey( fieldName ) ) 
				return Double.NaN;
			return scalars.get(fieldName).get(name);
		}
	}


}
