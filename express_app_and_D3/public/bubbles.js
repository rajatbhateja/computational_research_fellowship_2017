(function() {
	var width = 1200;
		height = 700;

	var svg = d3.select("#chart")
		.append("svg")
		.attr("height", height)
		.attr("width", width)
		.append("g")
		.attr("transform", "translate(0,0)")

	var forceXSplit = d3.forceX(function(d){
		if(d.time === 'pre-2000') {
			return 370
		} else{
			return 970
		}
		}).strength(0.1)

	var forceXCombine =  d3.forceX(width / 2).strength(0.1)

	var forceCollide = d3.forceCollide(function(d){
			return radiusScale(d.prob) + 1;
		})

	var simulation = d3.forceSimulation()
		.force("x", forceXCombine)
		.force("y", d3.forceY(height / 2).strength(0.05))
		.force("collide", forceCollide)

	var radiusScale = d3.scaleSqrt().domain([0.5, 1]).range([5, 100])


	d3.queue()
		.defer(d3.csv, "results.csv")
		.await(ready)

	function ready (error, datapoints) {

		var circles = svg.selectAll(".artist")
			.data(datapoints)
			.enter().append("circle")
			.attr("class", "artist")
			.attr("r", function(d) {
				return radiusScale(d.prob);
			})
			.attr("fill", "#7BD7DE")
			.on("mouseover", function() {
    			tooltip.style("display", null);
  			})
  			.on("mouseout", function() {
    			tooltip.style("display", "none");
  			})
  			.on("mousemove", function(d) {
  				 tooltip.transition().duration(10)
    			.style("opacity", 0.9);
			  	tooltip.select("div").html("Word: <strong>" + d.word + "</strong><br/>Probability: <strong>" + d.prob + "</strong>")
			    .style("position", "fixed")
			    .style("left", (d3.event.pageX) + "px")
			    .style("top", (d3.event.pageY - 200) + "px")
			});

		var tooltip = d3.select("body").append("div")
			.attr("class", "tooltip")
			.style("opacity", 0.8);

		tooltip.append("rect")
		  .attr("width", 30)
		  .attr("height", 20)
		  .attr("fill", "#EAD9D5")
		  .style("opacity", 0.8);

		tooltip.append("div")
		  .attr("x", 5)
		  .attr("dy", "1.2em")
		  .style("text-anchor", "middle")
		  .attr("font-size", "1.5em")
		  .attr("font-weight", "bold");

		d3.select("#split").on('click', function(){
			simulation
				.force("x", forceXSplit)
				.alphaTarget(0.6)
				.restart()
		})

		d3.select("#combine").on('click', function(){
			simulation
				.force("x", forceXCombine)
				.alphaTarget(0.6)
				.restart()

		})

		simulation.nodes(datapoints)
			.on('tick', ticked)

		function ticked() {
			circles
				.attr("cx", function(d) {
					return d.x
				})
				.attr("cy", function(d){
					return d.y
				})
		}
	}


})();