// import other routes
const searchRoutes      = require('./search.js');
const patientsRoutes    = require('./patients.js');
const refundRoutes      = require('./refund.js');
const bookingRoutes     = require('./booking.js');
const helper            = require('../helper.js');
const name = "ROUTERSERVICE"

const appRouter = (app, request) => {
  
    // Home Page
    app.get("/index", (req, res) => {
        helper.log(name, "Serving Home Page to " + req.hostname);
        req.session.regenerate(function (err) {
            // will have a new session here
        })
        res.render("index.html", { hostname: app.hostname });
    });

    // Redirect to index from root
    app.get("/", (req, res) => {
        console.log("ACCESS: Redirecting to Home Page");
        res.redirect("/index");
    });

    // About this app
    app.get("/info", function (req, res) {
        console.log("ACCESS: Serving Info Page to " + req.hostname);
        res.render("info.html");
    });

    // Complaints page
    app.get("/complaint", function (req, res) {
        console.log("ACCESS: Serving Complain Page to " + req.hostname);
        res.render("complaint.html");
    });

    // Kubernetes health checks
    app.get("/healthz", function (req, res) {
        res.write("I'm fine");
        res.end();
    });

       

    // other routes
    searchRoutes(app, request);
    patientsRoutes(app, request);
    refundRoutes(app, request);
    bookingRoutes(app, request);
};

module.exports = appRouter;