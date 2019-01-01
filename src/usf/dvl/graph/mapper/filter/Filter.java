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
package usf.dvl.graph.mapper.filter;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;

import usf.dvl.common.Histogram1D;
import usf.dvl.graph.Graph;
import usf.dvl.graph.Graph.GraphVertex;


public abstract class Filter {

	private double max_f_value = Double.NaN;  //filter value max
	private double min_f_value = Double.NaN;  //filter value min

	private boolean normalize = false;
	private boolean equalize  = false;
	
	
	private HashMap<Graph.GraphVertex, Double> filter = new HashMap<Graph.GraphVertex, Double>();
	private HashMap<Graph.GraphVertex, Integer> rankFilter = new HashMap<Graph.GraphVertex, Integer>();
	private int maxRank;
	
	protected void finalize() {
		min_f_value = Collections.min( filter.values() );
		max_f_value = Collections.max( filter.values() );
		
		List<GraphVertex> entries = new ArrayList<GraphVertex>(filter.keySet());
		entries.sort( new Comparator<GraphVertex>(){
			@Override public int compare(GraphVertex o1, GraphVertex o2) {
				if( filter.get(o1) < filter.get(o2) ) return -1;
				if( filter.get(o1) > filter.get(o2) ) return  1;
				return 0;
			}
		});
		maxRank = 0;
		rankFilter.put( entries.get(0), maxRank );
		for( int i = 1; i < entries.size(); i++ ) {
			if( entries.get(i-1) != entries.get(i) ) maxRank++;
			rankFilter.put( entries.get(i), maxRank );
		}
		
	}
	
	protected void put( GraphVertex v, double val ) {
		filter.put( v, val );
	}
	
	public double get( GraphVertex v ) { 
		if( !filter.containsKey(v) ) return Double.NaN;
		if( equalize ) {
			if( normalize ) 
				return (double)rankFilter.get(v)/(double)maxRank;
			return rankFilter.get(v);
		}
		if( normalize ) {
			return (filter.get(v)-min_f_value)/(max_f_value-min_f_value);
		}
		return filter.get(v);
	}

	public double getMax() { 
		if( normalize ) return 1.0;
		if( equalize )  return maxRank; 
		return this.max_f_value; 
	}
	
	public double getMin() { 
		if( normalize || equalize ) return 0.0;
		return this.min_f_value; 
	}
	
	public void enableNormalize() { this.normalize = true; }
	public void disableNormalize() { this.normalize = false; }
	public boolean isNormalized() { return normalize; }
	public void setNormalize(boolean v) { this.normalize = v; }
	
	public void enableEqualize() { this.equalize = true; }
	public void disableEqualize() { this.equalize = false; }
	public boolean isEqualized() { return equalize; }
	public void setEqualize(boolean v) { this.equalize = v; }
	

	public abstract String getName();
	public abstract String getShortName();

	public Histogram1D getHistogram(){
		Histogram1D hist = new Histogram1D( 25, (float)getMin(), (float)getMax() );
		for( GraphVertex v : filter.keySet() ) {
			hist.add( (float)get(v) );
		}
		return hist;
	}


}
