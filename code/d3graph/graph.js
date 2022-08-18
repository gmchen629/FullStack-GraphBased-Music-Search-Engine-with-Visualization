// const backendUrl = 'http://127.0.0.1:5000/info';
// let searchContent = "Lemon Tree";
// const queryUrl = `${backendUrl}/${searchContent}`
// console.log(queryUrl)
//
// fetch(queryUrl)
//     .then((data) => data.json())
//     .then((response) => {
//         response.info = response.children
//         response.type = 'music'
//         console.log(response)
//         info_tree(response)
//     }).catch((e) => {console.error('ERROR: d3tree: http request error while start the tree', e)})

window.addEventListener(
    'message', (event) => {
        if (typeof event.data != 'object') {
            console.error(`Error: postMessage() did not pass a valid event.data object, event.data: ${event.data}`)
        }
        if (event.data.call == 'reloadD3Graph') {
            const backend_url = 'http://127.0.0.1:5000/info';
            let search_content = event.data.value.searchContent;
            console.log("graph searchContent")
            console.log(search_content)
            const queryUrl = `${backend_url}/${search_content}`
            console.log(queryUrl)
            fetch(queryUrl)
                .then((data) => data.json())
                .then((response) => {
                    response.info = response.children
                    response.type = 'music'
                    d3.selectAll('svg').remove();
                    info_tree(response)
                }).catch((e) => {
                console.error('ERROR: d3tree: http request error while start the tree', e)})
        }
    },
    false)

function info_tree(data) {
    // var links = arrayOfObjects;
    var links = data.children;
    var nodes = {};
    // compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, value: link.value});
    });

    var width = 800,
        height = 600;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(250))
        .force('center', d3.forceCenter(width / 4.5, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-250))
        .alphaTarget(1)
        .on("tick", tick);

    var svg = d3.select("body")
        .append("svg")
        .attr("id", "svg-graph")
        .attr("width", width)
        .attr("height", height);

    // add the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", function(d) { return "link " + d.type; })

    path.attr("class", "link")
        .style("stroke", 'green')
        .style("stroke-width", 1)
        .style("stroke-dasharray", 4)

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
        .on("dblclick", doubleClick)
        .on("click", singleClick);

    // add the nodes
    node.append("circle")
        .attr("id", function(d){return (d.name.replace(/\s+/g,'').toLowerCase());})
        .attr("r", function(d) {
            d.weight = path.filter(function(l) {return l.source.index == d.index || l.target.index == d.index;}).size();
            var minRadius = 10;
            return minRadius + (d.weight + 4);})
        .style("fill", function(d) {
            d.weight = path.filter(function(l) {
                return l.source.index == d.index || l.target.index == d.index;
            }).size();
            let check_List = ['danceability', 'energy', 'liveness', 'popularity'];
            if (check_List.includes(d.name.replace(/\s+/g,'').toLowerCase())) {
                d.weight = 3;
            }
            if (d.name === 'Click to Try') {
                d.weight = 4;
            }
            if (d.weight <= 1) {return '#e0ecf4';}
            else if (d.weight <= 3) {return '#e0bbf4';}
            else if (d.weight <= 4) {return '#dd1be4';}
            else {return '#dd1c77';}
        })

    node.append("text")
        .attr("x", function (d){return 15;})
        .attr("y", function (d){return -15;})
        .style("font-size", '15px')
        .text(function(d) {
            if (d.name === 'Click to Try' || d.weight > 5) {
                return d.name;
            }
            return d.name + ": " + d.value;
        })

    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }

    function dragstarted(d) {
        if (!d3.event.active) force.alphaTarget(0.3).restart();
        if (d.name != "Click to Try") {
            d.fixed = true;
            d.fx = d.x;
            d.fy = d.y;
            d3.select(this).select("circle").style("fill", '#feb24c')
        }

    }

    function dragged(d) {
        d.fx = d3.event.x
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) force.alphaTarget(0);
        if (d.fixed == true) {
            d.fx = d.x;
            d.fy = d.y;
        }
        else {
            d.fx = null;
            d.fy = null;
        }
    }

    function doubleClick(d){
        d.fx = null;
        d.fy = null;
        svg.selectAll("circle")
            .attr("r", function(d) {
                d.weight = path.filter(function(l) {
                    return l.source.index == d.index || l.target.index == d.index;
                }).size();
                var minRadius = 10;
                return minRadius + (d.weight + 4);
            })
            .style("fill", function(d) {
                d.weight = path.filter(function(l) {
                    return l.source.index == d.index || l.target.index == d.index;
                }).size();
                let check_List = ['danceability', 'energy', 'liveness', 'popularity'];
                if (check_List.includes(d.name.replace(/\s+/g,'').toLowerCase())) {
                    d.weight = 3;
                }
                if (d.name === 'Click to Try') {
                    d.weight = 4;
                }
                if (d.weight <= 1) {return '#e0ecf4';}
                else if (d.weight <= 3) {return '#e0bbf4';}
                else if (d.weight <= 4) {return '#dd1be4';}
                else {return '#dd1c77';}
            });
    }

    function singleClick(d) {
        if (d.name === 'Click to Try') {
            let url = "https://open.spotify.com/track/";
            url += d.value;
            window.open(url,'_blank');
        }
    }
}
