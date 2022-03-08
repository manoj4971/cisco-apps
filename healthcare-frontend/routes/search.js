const helper = require('../helper.js');
const searchRoutes = (app, request) => {

    // InformationSearch Service
    var searchHost = process.env.SEARCH_SERVICE 
    var searchPort = process.env.SEARCH_PORT 
    var searchURL = "http://" + searchHost + ":" + searchPort + "/search";

    app.all("/search", function (req, res) {
        console.log("SEARCHROUTES: Serving Search Page to " + req.hostname);


        try {

            var options = {
                method: "get",
                url: searchURL
            };

            if (req.query.category) {
                console.log("SEARCHROUTES: Filtering request based on Categories:" + req.query.category);
                options.url += "?category=" + req.query.category
            } else if (req.body.category) {
                options.url += "?category=" + req.body.category
                var payload = {
                    category: req.body.category
                };

                helper.addAppDynamicsData(payload);
            }



            // Execute the GET request to Offers Services
            request(options, function (err, response, body) {
                if (err) {
                    console.error("SEARCHROUTES Error:", err);
                    res.render("offers.html", { service_unavailable: true });
                    return;
                }

                res.render("offers.html", {
                    offers: JSON.parse(body)
                });
            });
        } catch (err) {
            console.error(err);
        }
    });
}

module.exports = searchRoutes