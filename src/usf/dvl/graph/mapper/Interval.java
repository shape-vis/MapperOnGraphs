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

import processing.data.JSONObject;

//simple interval class. The domain of a filteraton f:V->R is covered by such intervals
public class Interval {

	private double minV; 
	private double maxV;
	private boolean modified = true;
	
	public Interval(double a_, double b_ ) {
		minV=Math.min(a_, b_);
		maxV=Math.max(a_, b_);
	}
	
	public Interval(JSONObject json) {
		minV = json.getDouble("a");
		maxV = json.getDouble("b");
	}

	
	public double getMin() { return minV; }
	public double getMax() { return maxV; }
	public double getMid() { return (minV+maxV)/2; }

	
	void setInterval( Interval inter ) {
		modified = !( minV==inter.minV && maxV==inter.maxV );
		this.minV = inter.minV;
		this.maxV = inter.maxV;
	}

	public void setInterval( double _a, double _b ) {
		double newMin = Math.min(_a, _b);
		double newMax = Math.max(_a, _b);
		
		modified = !( minV==newMin && maxV==newMax );
		
		minV = newMin;
		maxV = newMax;
	}

	public boolean isModified() { return modified; }
	public void clearModifed() { modified = false; }
	
	
	public boolean inIntervalInclusive( double v ) {
		return minV <= v && v <= maxV;
	}
	public boolean inIntervalExclusive( double v ) {
		return minV < v && v < maxV;
	}
	
	public boolean overlaps(Interval j) {
		return inIntervalInclusive(j.minV) || inIntervalInclusive(j.maxV) 
				|| j.inIntervalInclusive(minV) || j.inIntervalInclusive(maxV);
	}
	

	public String toString() {
		return "[" + minV + ", " + maxV + "]";
	}

	public JSONObject toJSON() {
		JSONObject ret = new JSONObject();
		ret.setDouble("a", minV);
		ret.setDouble("b", maxV);
		return ret;
	}

}
