var card_object = document.getElementById('id_card')


// READING OF JSON FILE
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4 && rawFile.status === "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}


// MAIN
width = window.innerWidth || document.documentElement.clientWidth;
height = window.innerHeight || document.documentElement.clientHeight;

var svg = d3.select("svg");

d3.select("svg").attr("height", height)
d3.select("svg").attr("width", width)

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        return d.id;
    }).distance(100).strength(0.001))
    .force("charge", d3.forceManyBody().strength(-200).distanceMax(500).distanceMin(50))
    .force("center", d3.forceCenter(width / 3.5, height / 2))
    .force("collision", d3.forceCollide().radius(35));

// ######################################
// # Read graph.json and draw SVG graph #
// ######################################
d3.json(graph_data_path, function (error, graph) {
    if (error) throw error;


    var link = svg.append("g")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke", "#547cf5")
        .attr("stroke-width", function (d) {
            return Math.sqrt(parseInt(d.value) / 2);
        });


    var node = svg.append("g")
        .attr("class", "nodes")
        .attr("id", "nodes")
        .selectAll("a")
        .data(graph.nodes).enter()
        .append("a")
        .attr("xlink:href", "#")


    node.on("click", function (d) {
        var data = {
            'device_id': d.object_id,
            'device_name': d.id
        }
        GetDeviceNeighbors(data)
    })


    node.call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    node.append("image")
        .attr("xlink:href", function (d) {
            return (image_path + d.group + ".png");
        })
        .attr("width", 64)
        .attr("height", 64)
        .attr("x", -16)
        .attr("y", -25)
        .attr("fill", function (d) {
            return color(d.group);
        });

    node.append("text")
        .attr("font-size", "1.2em")
        .attr("fill", "#ba54f5")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .attr("x", -125)
        .attr("y", -12)
        .text(function (d) {
            return d.id
        });


    node.append("title")
        .text(function (d) {
            return d.id;
        });

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")"
            });
    }
});

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function GetDeviceNeighbors(initial_data) {
    console.log(initial_data)
    $.ajax({
        type: 'GET',
        url: ajax_device_neighbors_url,
        data: {
            'device_id': initial_data['device_id'],
        },
        dataType: 'json',
        success: function (received_data) {

            var card_header = document.getElementById('id_card_header')
            var card_body_out = document.getElementById('id_card_body_out')


            if (card_header !== null && card_body_out !== null) {
                card_header.remove()
                card_body_out.remove()
            }


            card_header = document.createElement('div')
            card_header.setAttribute('class', 'card-header')
            card_header.setAttribute('id', 'id_card_header')

            card_body_out = document.createElement('div')
            card_body_out.setAttribute('class', 'card-body')
            card_body_out.setAttribute('id', 'id_card_body_out')


            var card_tittle = document.createElement('h1')
            card_tittle.setAttribute('class', 'card-title')


            var card_colored_tittle = document.createElement('b')
            card_colored_tittle.setAttribute('class', 'text-info')
            card_colored_tittle.innerHTML = initial_data['device_name'] + ' #' + initial_data['device_id']
            card_tittle.innerHTML = 'Device Neighbors - '
            card_tittle.appendChild(card_colored_tittle)
            card_header.appendChild(card_tittle)

            var content = ''
            for (var i = 0; i < received_data.length; i++) {
                content += `
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <p><b class="text-info">Remote Device Type : </b>${received_data[i]['device_type']}</p>
                            <p><b class="text-info">Remote Name : </b>${received_data[i]['system_name']}</p>
                            <p><b class="text-info">Remote Interface</b>: ${received_data[i]['lldp_neighbor_interface']}</p>
                            <p><b class="text-info">Local Interface</b> : ${received_data[i]['interface_description']}</p>
                            <p><b class="text-info">Remote IP Address: </b>${received_data[i]['hostname']}</p>
                        </div>
                    </div>
                </div>`
                console.log(content)

            }
            card_body_out.innerHTML = content
            console.log(received_data)

            console.log(card_body_out)
            card_object.appendChild(card_header)
            card_object.appendChild(card_body_out)


        }
    })

}
