////////////////////////////////////////////////////////////////////////////////
// SET UP //

// Define the dimensions of the visualization.

const width = 800;
const height = 600;

// Define the data for the example. In general, a force layout
// requires two data arrays. The first array, here named `nodes`,
// contains the objects that are the focal point of the visualization.
// The second array, called `links` below, identifies all the links
// between the nodes. (The more mathematical term is "edges.")

// d3.json('/get_graph_info.json', function(data){
//     console.log(data)
// });
d3.json('/get_graph_info.json', makeForceLayout);

function makeForceLayout(data){

  // In this case, data is coming from the server, and is
  // the proper format for this visualization. In general, a force layout
  // requires two data arrays. The first array, here named `nodes`,
  // contains the object that are the focal point of the visualization.
  // The second array, called `links` below, identifies all the links
  // between the nodes. (The more mathematical term is "edges.")

  let dataNodes = data.nodes;
  let links = data.links;


  // Define the dimensions of the visualization.

  const width = 800;
  const height = 600;


  ////////////////////////////////////////////////////////////////////////////////
  // D3 Visualization //

  // We start off by creating an SVG container to hold the visualization. 
  // We only need to specify the dimensions for this container.

  let svg = d3.select('body')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

  // Now we create a forceSimulation object and add several forces to
  // this simulation.

  let force = d3.forceSimulation(d3.values(dataNodes))
        .force("link", d3.forceLink(links).id(function(node, i) { return node.id; }).distance(100))
        .force("center", d3.forceCenter(width / 2, height/ 2))
        .force("charge", d3.forceManyBody().strength(-100));
//add depth value on nodes, use 

  // Next we'll add the nodes and links into the SVG container
  // The order here is important because we want the nodes to 
  // appear "on top of" the links. With this ordering, SVG will 
  // draw the lines first and then the nodes after, ensuring 
  // that nodes appear on top of links.

  // Links are just SVG lines. We're not even going to specify 
  // their coordinates. (The force layout take care of that.) 
  // Without any coordinates, the lines won't be visible until
  // the force layout adds this information.

  let link = svg.selectAll('.link') // (Empty) selection containing any '.link' elements
      .data(links) // D3 "data join". Associates links from the link array with any existing '.link' elements
      .enter()  // The "enter" selection creates a placeholder for each item in the links array.
      .append('line') // Replaces the placeholder with an actual line SVG element. Now each link corresponds to a line element.
      .attr('class', 'link');

  // Nodes are SVG groups containing SVG circles.

  let node = svg.selectAll('.node') // (Empty) selection containing any '.node' elements
      .data(force.nodes()) // D3 data join. Associates nodes from the force layout with any existing '.node' elements
      .enter() // The "enter" selection creates a placeholder for each item in the array of joined data.
      .append('g') // Replaces the placeholder with an actual g SVG element. Now each link corresponds to a g element.
      .attr('class', 'node');

  let color = d3.scaleOrdinal(d3.schemeCategory10);

  node.append("circle") // Appends a circle SVG element to each ".node" element
      .attr("r", 10)
      .style("fill", function (d) {
        return color(d.type);
      });

  node.append("text").text(function (d) { // Appends a text SVG element to each ".node" element
    return d.nodeName;
  });

  // Define a callback function stating what code to run 
  // once the force layout's simulation calculations are
  // complete.

  force.on('end', function () {

    // This function executes when the force layout
    // calculations are complete. The node and link
    // objects should now have various properties 
    // that we can use to position them within the 
    // SVG container.

    // First we set the ".node" elements' x and y coordinates
    // to match the x and y values that the force layout
    // simulation assigned to the data.

    node.attr("transform", function (d) {
      return "translate(" + d.x + "," + d.y + ")";
    });

    // We also need to update positions of the ".link" elements.
    // For those elements, the force layout specifies
    // `x` and `y` values for both the source and target properties.

    link.attr('x1', function (d) {
          return d.source.x;
        })
        .attr('y1', function (d) {
          return d.source.y;
        })
        .attr('x2', function (d) {
          return d.target.x;
        })
        .attr('y2', function (d) {
          return d.target.y;
        });

  });

}

////////////////////////////////////////////////////////////////////////////////
// Epilogue //

// By the time you've read this far in the code, the force
// layout has undoubtedly finished its work. If you have a screen
// ruler (such as [xScope](http://xscopeapp.com) handy, measure
// the distance between the centers of the two circles. It
// should be somewhere close to the `linkDistance` parameter we
// set for the force layout. That, in the most basic of all nutshells, 
// is what a force layout does. We tell it how far apart we want 
// connected nodes to be, and the layout keeps moving the nodes around
// until they get reasonably close to that value.

// Of course, there's quite a bit more than that going on
// under the hood.