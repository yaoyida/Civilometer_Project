

var cvmGraphs = function(){
    var magicRatio = 1.85;



      var temp_data= {
  "status": "success",
  "results": [
    {
      "_id": "2000-01-01T05:00:00",
      "value": {
        "Romney": 1.1208746110529344,
        "Obama": 0.00977592175310571,
        "n":5
      }
    },
    {
      "_id": "2012-08-15",
      "value": {
        "Romney": 0.7218920737863477,
        "Obama": 0.6250727456677252
      }
    },
    {
      "_id": "2012-08-14",
      "value": {
        "Romney": 1.0811321341332902,
        "Obama": 5.13124537937899
      }
    },
    {
      "_id": "2012-08-13",
      "value": {
        "Romney": 9.929891153758991,
        "Obama": 6.542602170152146
      }
    },
    {
      "_id": "2012-08-12",
      "value": {
        "Romney": 2.684285431525877,
        "Obama": 3.4711127090571416
      }
    },
    {
      "_id": "2012-08-11",
      "value": {
        "Romney": 5.066854032499735,
        "Obama": 6.918722859601897
      }
    },
    {
      "_id": "2012-08-10",
      "value": {
        "Romney": 3.185393090090333,
        "Obama": 3.476036931261095
      }
    },
    {
      "_id": "2012-08-09",
      "value": {
        "Romney": 1.9922282330419372,
        "Obama": 3.4988862807800825
      }
    },
    {
      "_id": "2012-08-08",
      "value": {
        "Romney": 1.7933512463545809,
        "Obama": 1.0386126447932231
      }
    },
    {
      "_id": "2012-08-07",
      "value": {
        "Romney": 6.708297200541059,
        "Obama": 2.729050820650525
      }
    },
    {
      "_id": "2012-08-06",
      "value": {
        "Romney": 9.54144800307115,
        "Obama": 5.646596075792844
      }
    },
    {
      "_id": "2012-08-05",
      "value": {
        "Romney": 7.439839194544252,
        "Obama": 7.503469327280029
      }
    },
    {
      "_id": "2012-08-04",
      "value": {
        "Romney": 2.2389806786210507,
        "Obama": 2.8824924019515388
      }
    },
    {
      "_id": "2012-08-03",
      "value": {
        "Romney": 5.295337627376386,
        "Obama": 4.08657056925666
      }
    },
    {
      "_id": "2012-08-02",
      "value": {
        "Romney": 9.40048353250259,
        "Obama": 9.090280268254737
      }
    },
    {
      "_id": "2012-08-01",
      "value": {
        "Romney": 4.332400033775602,
        "Obama": 8.047259282587673
      }
    },
    {
      "_id": "2012-07-31",
      "value": {
        "Romney": 2.4811425634154283,
        "Obama": 6.528507843952358
      }
    },
    {
      "_id": "2012-07-30",
      "value": {
        "Romney": 0.62895018974783,
        "Obama": 8.407442490686597
      }
    },
    {
      "_id": "2012-07-29",
      "value": {
        "Romney": 3.489896097303238,
        "Obama": 0.2773013355002074
      }
    },
    {
      "_id": "2012-07-28",
      "value": {
        "Romney": 0.3995038806258522,
        "Obama": 3.6639664482718914
      }
    },
    {
      "_id": "2012-07-27",
      "value": {
        "Romney": 1.1437334507941732,
        "Obama": 7.99249055678199
      }
    },
    {
      "_id": "2012-07-26",
      "value": {
        "Romney": 6.171126166724415,
        "Obama": 2.867018586063095
      }
    },
    {
      "_id": "2012-07-25",
      "value": {
        "Romney": 3.5586194589356945,
        "Obama": 1.3969472005496186
      }
    },
    {
      "_id": "2012-07-24",
      "value": {
        "Romney": 5.7388584466282735,
        "Obama": 9.94531422647636
      }
    },
    {
      "_id": "2012-07-23",
      "value": {
        "Romney": 7.709539718179903,
        "Obama": 0.5983568422937624
      }
    },
    {
      "_id": "2012-07-22",
      "value": {
        "Romney": 2.6054673053862687,
        "Obama": 3.4415254921179717
      }
    },
    {
      "_id": "2012-07-21",
      "value": {
        "Romney": 3.729224864334475,
        "Obama": 1.4571631990596923
      }
    },
    {
      "_id": "2012-07-20",
      "value": {
        "Romney": 4.179268939585627,
        "Obama": 0.9927770060679808
      }
    },
    {
      "_id": "2012-07-19",
      "value": {
        "Romney": 0.9322141789383087,
        "Obama": 5.478298537230195
      }
    },
    {
      "_id": "2012-07-18",
      "value": {
        "Romney": 9.134313933086032,
        "Obama": 8.901702534600947
      }
    },
    {
      "_id": "2012-07-17",
      "value": {
        "Romney": 1.1728547706880155,
        "Obama": 0.4100338897275657
      }
    },
    {
      "_id": "2012-07-16",
      "value": {
        "Romney": 0.7648555774495591,
        "Obama": 1.8739908929975324
      }
    },
    {
      "_id": "2012-07-15",
      "value": {
        "Romney": 2.2915011542932042,
        "Obama": 7.464037044038233
      }
    },
    {
      "_id": "2012-07-14",
      "value": {
        "Romney": 5.719749610066125,
        "Obama": 8.324932917760973
      }
    },
    {
      "_id": "2012-07-13",
      "value": {
        "Romney": 9.247594735452067,
        "Obama": 2.963102968753013
      }
    },
    {
      "_id": "2012-07-12",
      "value": {
        "Romney": 1.4096230459773706,
        "Obama": 8.565626610443362
      }
    },
    {
      "_id": "2012-07-11",
      "value": {
        "Romney": 3.5410721019761358,
        "Obama": 6.728932352906163
      }
    },
    {
      "_id": "2012-07-10",
      "value": {
        "Romney": 1.5943674941922004,
        "Obama": 8.10108060954558
      }
    },
    {
      "_id": "2012-07-09",
      "value": {
        "Romney": 8.625061800794247,
        "Obama": 6.237159829261163
      }
    },
    {
      "_id": "2012-07-08",
      "value": {
        "Romney": 5.658817462906782,
        "Obama": 5.9668005072930885
      }
    },
    {
      "_id": "2012-07-07",
      "value": {
        "Romney": 8.640709687119216,
        "Obama": 7.810671871881148
      }
    },
    {
      "_id": "2012-07-06",
      "value": {
        "Romney": 9.754980012504534,
        "Obama": 2.4241934734193205
      }
    },
    {
      "_id": "2012-07-05",
      "value": {
        "Romney": 0.2723834026908234,
        "Obama": 0.27809128750149736
      }
    },
    {
      "_id": "2012-07-04",
      "value": {
        "Romney": 7.624508356987528,
        "Obama": 4.136148050909181
      }
    },
    {
      "_id": "2012-07-03",
      "value": {
        "Romney": 2.522388981480115,
        "Obama": 7.053343414714174
      }
    },
    {
      "_id": "2012-07-02",
      "value": {
        "Romney": 0.37486646182816163,
        "Obama": 3.0313359574421286
      }
    },
    {
      "_id": "2012-07-01",
      "value": {
        "Romney": 7.699510586184455,
        "Obama": 1.154094003861883
      }
    },
    {
      "_id": "2012-06-30",
      "value": {
        "Romney": 7.531630465912422,
        "Obama": 8.318407594960277
      }
    },
    {
      "_id": "2012-06-29",
      "value": {
        "Romney": 9.500029311962408,
        "Obama": 2.145648584828914
      }
    },
    {
      "_id": "2012-06-28",
      "value": {
        "Romney": 7.708693922528234,
        "Obama": 3.1475144539408975
      }
    },
    {
      "_id": "2012-06-27",
      "value": {
        "Romney": 1.343245565924428,
        "Obama": 6.892028662013878
      }
    },
    {
      "_id": "2012-06-26",
      "value": {
        "Romney": 3.454936602472282,
        "Obama": 8.57595653084407
      }
    },
    {
      "_id": "2012-06-25",
      "value": {
        "Romney": 8.468382100264513,
        "Obama": 8.241399822639554
      }
    },
    {
      "_id": "2012-06-24",
      "value": {
        "Romney": 5.30901698784281,
        "Obama": 7.74058815089183
      }
    },
    {
      "_id": "2012-06-23",
      "value": {
        "Romney": 6.409411425886644,
        "Obama": 5.0332472583048045
      }
    },
    {
      "_id": "2012-08-22",
      "value": {
        "Romney": 8.345039598264844,
        "Obama": 2.264907298219214
      }
    },
    {
      "_id": "2012-06-21",
      "value": {
        "Romney": 2.9783134287299537,
        "Obama": 0.6062488933889487
      }
    },
    {
      "_id": "2012-06-20",
      "value": {
        "Romney": 1.6598426435919311,
        "Obama": 6.489389758750123
      }
    },
    {
      "_id": "2012-06-19",
      "value": {
        "Romney": 7.559916465147857,
        "Obama": 0.6031578327237075
      }
    },
    {
      "_id": "2012-06-18",
      "value": {
        "Romney": 1.2527513312475602,
        "Obama": 7.608921392889152
      }
    }
  ]
};

    this.genChart = function (object) {

        object.data = temp_data.results;
        object.width = $(object.ele).width();
        object.height = $(object.ele).width()/magicRatio;

        $.each(object.data, function(key, value){
            candidate = new Date(value._id);
            if (object.min_date === undefined || object.min_date > candidate) object.min_date = candidate;
            if (object.max_date === undefined || object.max_date < candidate) object.max_date = candidate;
            if( "n" in value.value ) delete value.value.n;
            $.each(value.value, function(k, v){
                if (object.max === undefined || object.max < v) object.max = v;
                if (object.min === undefined || object.min > v) object.min = v;
          });
        });

        //object.x =
       // object.y =

        switch (object.fn) {
            case "timeSeries": return this.timeSeries(object);
           //break;
            //case "barChart": return barChart(object);
            //break;
           // case "dotPlot": return dotPlot(obejct);
            //break;
           // case "linePlot": return linePlot(object);
            //break;
           // case "wordCloud": return wordCloud(object);
            //break;

            default: break;
        }

    };

    this.timeSeries = function (object) {
//move up to the chart object? no: scale type will be diff (unless do in switch?)
   // var x = d3.scale.ordinal().domain(d3.range(object.data.results.length+1)).rangeBands([0, object.width]);
    //var format = d3.time.format("%Y-%m_%d");
    var x = d3.time.scale().domain([object.min_date.getTime(), object.max_date.getTime()]).range([0, object.width]);
    var y = d3.scale.linear().domain([object.min-(object.max-object.min)*.15, object.max+(object.max-object.min)*.15]).range([0, object.height]);


        var line = d3.svg.line()
        .interpolate("basis")
        .x(function(data, i) { return x(new Date(data._id));})
        .y(function(data) { return y(data.value);});

var vis = d3.select(object.ele)
.append("svg:svg")
.attr("width", object.width)
.attr("height", object.height)
.append("svg:g");


vis.append("svg:path").
data(object.data)
.attr("d", line);



/*
        var line = d3.svg.line()
        .interpolate("basis")
        .x(function(object) { return x(Math.random()*200);})
        .y(function(object) {return y(6);});


/*
        d3.select(object.ele)
        .data(object.data)
        .enter().append("path")
        .attr("class", "line")
        .attr("data", line);
*/
 // var svg = d3.select(object.ele).append("svg:svg")
 /*
d3.select(object.ele)
    .append("svg")
    .attr("width", object.width)
    .attr("height",object.height)
    .selectAll("series")
        .data(object.data)
        .enter()
        .append("series")
        .attr("data", line);

/*
//d3.select(object.ele)
      d3.select(object.ele)
    .data(object.data)
  .enter().append("svg")
    .attr("class", "line")
    .attr("data", line);
*/
    };

};