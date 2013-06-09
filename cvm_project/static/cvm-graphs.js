var cvmGraphs = {
    genFakeSequence : function( n ){
        var a = Math.random()*100-10;
        var b = Math.random()*100-10;
        var d_min = Math.min(a,b);
        var delta = Math.max(a,b)-d_min;
        var c = Math.random()*(delta/5)-(delta/10);

        d = []
        for( i=0; i<n; i++ ){
//            d.push( [i, Math.round(d_min+Math.random()*delta+c*i)] );
            d.push( Math.round(d_min+Math.random()*delta+c*i) );

            if( Math.random()>.95 ){
                var a = Math.random()*100-10;
                var b = Math.random()*100-10;
                var d_min = Math.min(a,b);
                var delta = Math.max(a,b)-d_min;
                var c = Math.random()*(delta/5)-(delta/10);
            }

        }
        return d;        
    },
    
	genFakeData : function(n, k){
        //var fake_labels = ["lorem","ipsum","gelva","minaimgt","infomd","pratingl","quarmia","stucko","shubbil"];
        var data = [];
        for( j=0; j<k; j++ ){
            d = cvmGraphs.genFakeSequence(n);
            data.push({
                //label: fake_labels[Math.floor(Math.random()*fake_labels.length)],
                data: d
            });
        }
        return( data );
    },
    
	randomPlot : function( obj_id ){
		
		switch( Math.floor(Math.random()*3) ){
			case 0:
				var k = 2+Math.random()*6;
                var seq = cvmGraphs.genFakeSequence(k);
                var v = Math.random();
  				var data = d3.range(k).map(function(i){ return {
					'p' : seq[i],
					's' : Math.random()*(d3.max(seq)-d3.min(seq))*(v+.1)
				}});

				cvmGraphs.dotPlot( obj_id, data );
				break;
				
			case 1:
				var k = 3+Math.random()*10;
				var data = d3.range(k).map(function(){ return Math.random()*10 });

				cvmGraphs.barChart( obj_id, data );			
				break;
				
			case 2:
				var k = 7*Math.floor(1+Math.random()*4);
				var data = d3.range(k).map(function(){ return Math.random()*10 });

				cvmGraphs.linePlot( obj_id, data );

		}
	},
	
	dotPlot : function( obj_id, data ){
		var $obj = $(obj_id);

        var data_p = data.map(function(e){ return e.p });

		var left_m = 30,
            w = $obj.width(),//-left_m,
			h = $obj.width()/1.85,
            max = d3.max( data_p ),
            min = d3.min( data_p ),
			x = d3.scale.ordinal().domain(d3.range(data.length)).rangeBands([0, w]),
			y = d3.scale.linear().domain([min-(max-min), max+(max-min)]).range([0, h]);

		var vis = d3.select(obj_id)
            .append("svg:svg")
                .attr("width", w )
                .attr("height", h );
        
        // Axes
        var rules = vis.append("svg:g").classed("rules", true);

        function make_y_axis() {
          return d3.svg.axis()
              .scale(y)
              .orient("left")
//              .ticks(data.length)
              .ticks(5)
        }

        rules.append("svg:g").classed("grid y_grid", true)
            .call(make_y_axis()
              .tickSize(-w,-5,0)
              .tickSubdivide(1)
              .tickFormat("")
            )

		var groups = vis.selectAll("g.group")
			.data(data)
		  .enter().append("svg:g");
//            .attr("transform", "translate("+left_m+", 0)");
  
		//Error bars
		groups.append("svg:line")
			.attr("class", "dotplot-error-bar")
			.attr("x1", function(d, i) { return x.rangeBand()*i+x.rangeBand()/2 })
			.attr("y1", function(d) { return y(d.p - d.s) } )
			.attr("x2", function(d, i) { return x.rangeBand()*i+x.rangeBand()/2 })
			.attr("y2", function(d, i) { return y(d.p + d.s) } );

		//Dots
		groups.append("svg:circle")
			.attr("class", "dotplot-dot")
			.attr("cx", function(d, i) { return x.rangeBand()*i+x.rangeBand()/2 })
			.attr("cy", function(d) { return y(d.p) } )
			.attr("r", 6);
			
		//! Labels
	},
	
	barChart : function( obj_id, data ){
		var $obj = $(obj_id);

		var w = $obj.width(),
			h = $obj.width()/1.85,
			colors = ["#d84614", "#ec744b", "#ec9476", "#8c2906"],
            max = d3.max( data ),
            min = d3.min( data ),
			x = d3.scale.ordinal().domain(d3.range(data.length)).rangeBands([0, w]),
			y = d3.scale.linear().domain([0, max+(max-min)]).range([0, h]);

//			x = d3.scale.ordinal().domain(d3.range(data.length)).rangeBands([0, w]),
//			y = d3.scale.linear().domain([-2, 12]).range([0, h]);

		var vis = d3.select(obj_id)
		  .append("svg:svg")
			.attr("width", w )
			.attr("height", h )
		  .append("svg:g");

        var rules = vis.append("svg:g").classed("rules", true);

        function make_y_axis() {
          return d3.svg.axis()
              .scale(y)
              .orient("left")
              .ticks(5)
        }

        rules.append("svg:g").classed("grid y_grid", true)
            .call(make_y_axis()
              .tickSize(-w,-5,0)
              .tickSubdivide(1)
              .tickFormat("")
            )


		var groups = vis.selectAll("g.group")
			.data(data)
		  .enter().append("svg:g");
		  
		//Bars
		groups.append("svg:rect")
			.attr("fill", function(d, i){ return colors[i%colors.length] })//"#772953")   //Alternate colors
			.attr("x", function(d, i) { return x.rangeBand()*i })
			.attr("y", function(d, i) { return h-y(d) } )
			.attr("width", x.rangeBand()*.9)
			.attr("height", y);

		//Axes

	},
	
		
	linePlot : function( obj_id, data ){
		var $obj = $(obj_id);

		var w = $obj.width(),
//			h = $obj.width()/1.85//,1.61803399,
			h = $obj.width()/1.85//,1.61803399,
//        var h = $obj.height(),
//            w = Math.min(h*1.5, $obj.width()),
            max = d3.max( data ),
            min = d3.min( data ),
			x = d3.scale.ordinal().domain(d3.range(data.length+1)).rangeBands([0, w]),
			y = d3.scale.linear().domain([min-(max-min)*.15, max+(max-min)*.15]).range([0, h]);

		var vis = d3.select(obj_id)
		  .append("svg:svg")
			.attr("width", w )
			.attr("height", h )
		  .append("svg:g");

        var rules = vis.append("svg:g").classed("rules", true);

        function make_x_axis() {
          return d3.svg.axis()
              .scale(x)
              .orient("bottom")
              .ticks(8)
        }

        function make_y_axis() {
          return d3.svg.axis()
              .scale(y)
              .orient("left")
              .ticks(6)
        }

        rules.append("svg:g").classed("grid y_grid", true)
            .call(make_y_axis()
              .tickSize(-w,-5,0)
              .tickSubdivide(3)
              .tickFormat("")
            )

        rules.append("svg:g").classed("grid x_grid", true)
            .attr("transform", "translate(0,"+(h-1)+")")
            .call(make_x_axis()
              .tickSize(-5,0,0)
              .tickFormat("")
            )



		var line = d3.svg.line()
			.x( function(d,i){ return x(i+1) })
			.y( function(d,i){ return y(d) });

		var groups = vis.selectAll("g.group")
			.data([data])
		  .enter()
			.append("svg:path")
			.attr("class", "lineplot-line")
//			.datum(data)
			.attr("d", line(data) );
			
//		console.log($("g.lineplot-line"))

		//Axes

	},

	wordCloud : function( obj_id, data ){
		var $obj = $(obj_id);

        var data_p = data.map(function(e){ return e.p });

		var left_m = 30,
            w = $obj.width(),//-left_m,
			h = $obj.width()/1.85,
            max = d3.max( data_p ),
            min = d3.min( data_p ),
			x = d3.scale.ordinal().domain(d3.range(data.length)).rangeBands([0, w]),
			y = d3.scale.linear().domain([min-(max-min), max+(max-min)]).range([0, h]);

		var vis = d3.select(obj_id)
            .append("svg:svg")
                .attr("width", w )
                .attr("height", h );
        
        //! Doesn't work yet.  Need to move on for now.
        var layout = d3.layout.cloud()
            .size([w, h])
            //.size([960, 600])
            .timeInterval(10)
            .text(function(d) { return d.key; })
//            .font("Impact")
//            .fontSize(function(d) { return fontSize(+d.value); })
            .rotate(function(d) { return ~~(Math.random() * 5) * 30 - 60; })
            .padding(1)
//            .on("word", progress)
            .on("end", draw)
            .words(['A','B','C'])
            .start();

	},

};


