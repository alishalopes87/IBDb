import * as d3 from "d3-collection";
let data = d3.json('/get_graph_info.json', function(data){
    console.log(data)
    // data.forEach(function(d){
    //     console.log(data)
    // })
});
var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = 960 - margin.right - margin.left,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

let tree = d3.layout.tree()
    .size([height, width-160]);

let stratify = d3.stratify()
    .parentId(function(d){ return d.id.substring(0, d.id.lastIndexOf(".")); });
    console.log(stratify(data))
var root = stratify(data)
    console.log("i am root",root)
      .sort(function(a, b) { return (a.height - b.height) || a.id.localeCompare(b.id); });
