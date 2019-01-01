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
import java.util.Collection;

import processing.data.JSONArray;
import usf.dvl.common.MathX;
import usf.dvl.graph.mapper.filter.Filter;

public class Cover extends ArrayList<Interval> {

	private static final long serialVersionUID = 594763802603772305L;

	private boolean modified = false;
	

	public Cover(Filter filter, int chunksN, float eps) {

		if (chunksN<=1) {
			add( new Interval( filter.getMin(), filter.getMax()) );
			return;
		}

		for (int i=0; i<chunksN; i++) {
			double curr = MathX.lerp( filter.getMin(), filter.getMax(), (double)(i+0)/chunksN ) - eps;
			double next = MathX.lerp( filter.getMin(), filter.getMax(), (double)(i+1)/chunksN ) + eps;

			add( new Interval(	MathX.constrain( curr, filter.getMin(), filter.getMax() ),
								MathX.constrain( next, filter.getMin(), filter.getMax() )  ) );
		}
		
	}
	
	public Cover( JSONArray json ) {
		for( int i = 0; i < json.size(); i++ ) {
			add( new Interval( json.getJSONObject(i) ) );
		}
	}

	@Override public boolean add( Interval o ) {
		modified = true;
		return super.add(o);
	}

	@Override public boolean addAll( Collection<? extends Interval> o ) {
		modified = true;
		return super.addAll(o);
	}

	public String toString() {
		StringBuffer sb = new StringBuffer();
		sb.append("Cover:" );
		for( Interval i : this ) {
			sb.append( " " + i );
		}

		return sb.toString();
	}
	
	public JSONArray toJSON() {
		JSONArray ret = new JSONArray();
		for( int i = 0; i < size(); i++ ) {
			ret.append( get(i).toJSON() );
		}
		return ret;
	}
	
	public void splitInterval( Interval v, float eps ) {
		double a = v.getMin(), b = v.getMid(), c = v.getMax();
		v.setInterval(a,b+eps);
		add( new Interval( b-eps, c ) );
	}
	
	public boolean isModified() {
		if( modified ) return true;
		for( Interval ival : this ) {
			if( ival.isModified() ) return true;
		}
		return false;
	}
	
	public void clearModified() {
		modified = false;
		for( Interval ival : this ) {
			ival.clearModifed();
		}
	}

	public void setModified() {
		modified = true;
	}
	
}

