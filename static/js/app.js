var app = angular.module("myApp", []);

app.controller("myCtrl", function($scope, $http) {
    // Appel de l'API Flask pour récupérer les données du graph network
    $http.get("/api/data")
        .then(function(response) {
            var data = {
              nodes: new vis.DataSet(response.data.nodes),
              edges: new vis.DataSet(response.data.edges),
            };

            // Définition des options pour le graph network
            var options = {height: "900px"};

            // Création du graph network
            var container = document.getElementById("mynetwork");
            var network = new vis.Network(container, data, options);

            // ajout des évènements on_click
            network.on('click', function(params) {

                // Si on clique sur un nœud
                if (params.nodes.length > 0) {
                    const nodeId = params['nodes']['0'];

                    // Récupération des arêtes connectées au nœud cliqué
                    // On n'utilise pas network.getConnectedEdges(nodeId) parce qu'on veut que ça fonctionne à tout moment
                    const full_edges = new vis.DataSet(response.data.edges)

                    // Suppression des arêtes non connectées
                    const connectedEdges = network.getConnectedEdges(nodeId);
                    data.edges.forEach(function(edge) {
                        if (!connectedEdges.includes(edge.id)) {
                            data.edges.remove(edge.id);
                        }});

                    // Ajout des arêtes non existantes mais connectées
                    const edgesToConnect = full_edges.get({
                        filter: function (edge) {
                            return edge.from === nodeId || edge.to === nodeId;
                        }
                    });
                    edgesToConnect.forEach(function(edge) {
                        data.edges.update(edge)
                    });
                }
                // Si on clique dehors
                if (params.nodes.length === 0) {
                    full_edges = new vis.DataSet(response.data.edges)
                    full_edges.forEach(function(edge) {
                        data.edges.update(edge);
                    });
                }
            });
        });
});
