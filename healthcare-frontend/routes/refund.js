const db = require('../db.js');
const refundRoutes = (app, request) => {
    // Refund Service
    var refundHost = process.env.REFUND_SERVICE
    var refundPort = process.env.REFUND_PORT
    var refundUrl = "http://" + refundHost + ":" + refundPort + "/refund";

    // Reset the refunded passenger list
    app.get("/refreset", function (req, res) {
        db.del("refunded", function (err, reply) {
            console.log("REFUNDROUTE: Client requested refunded passenger list reset.");
            res.render("refunded.html");
        });
    });

    // Ask for a refund
    app.post("/refund", function (req, res) {
        console.log("REFUNDROUTE: Refund Requested: " + req.body.pToRefund);

        try {
            // Build Payload
            payload = req.body;

            // Build Refund POST options
            var options = {
                method: "post",
                body: payload,
                json: true,
                timeout: 2000,
                url: refundUrl
            };

            // Execute POST to Refund
            request(options, function (err, response) {
                if (err) {
                    console.error("REFUNDROUTE: ERROR:", err);
                    res.render("refunded.html", { service_unavailable: true });
                    return;
                }
                var refundRes = response.body;
                console.log("REFUNDROUTE: Requesting refund to " + refundHost);
                console.log("REFUNDROUTE: Refund service returned: " + JSON.stringify(response.body));
                console.log("REFUNDROUTE: Passenger will be refunded with amount: " + refundRes.amount);

                res.render("patients.html", {
                    refunded: true,
                    amount: refundRes.amount,
                    hostname: refundRes.hostname,
                    refundVer: refundRes.refundVer
                });
            });
        } catch (err) {
            console.error("REFUNDROUTE: Error: " + err);
        }
    });

    // Get refunded customer list
    app.get("/refunded", function (req, res) {
        console.log("REFUNDROUTE: Serving Refunded passenger page to " + req.hostname);
        // Create empty refunded passenger list
        refund_table = [];

        // If redis client is ready dump all transactions into the refund table as JSON

        db.lrange("refunded", 0, -1, function (err, reply) {
            reply.forEach(function (reply, i) {
                refund_table.push(JSON.parse(reply));
            });
            res.render("refunded.html", { refund_table: refund_table });
        });



    });

}
module.exports = refundRoutes