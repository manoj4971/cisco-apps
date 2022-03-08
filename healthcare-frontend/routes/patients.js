const helper = require('../helper.js');
const db = require('../db.js');


const patientsRoutes = (app, request) => {
    // Get the patients list
    app.get("/patients", function (req, res) {
        console.log("patientsRoutes: Serving patients Page to " + req.hostname);
        // Create empty passenger list
        history_table = [];
        console.log("----[patientsRoutes: ready to get information from redis client")
        try {
            db.lrange("transactions", 0, -1, function (err, reply) {
                reply.forEach(function (reply, i) {
                    history_table.push(JSON.parse(reply));
                    console.log("Patient in Redis:" + reply);
                });
                  res.render("patients.html", { history_table: history_table });
            });
            console.log("----[patientsRoutes: done")
        } catch (error) {
            console.error("DB is not responding: Error is " + error);
            res.render("patients.html", { service_unavailable: true });
        }
        
    });

    // Reset the passenger list
    app.get("/reset", function (req, res) {
        db.del("transactions", function (err, reply) {
            console.log("PATIENTSROUTE: Client requested passenger list reset.");
            res.render("patients.html");
        });
        
    });
}
module.exports = patientsRoutes