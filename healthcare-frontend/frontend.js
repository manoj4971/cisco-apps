// V2 // App requires
const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const nunjucks = require("nunjucks");
const path = require("path");
const app = express();
const appPort = 5000;
const session = require('express-session')


// App Use Section
app.use(session({
    secret: 'keyboard cat',
    name: 'hcSessionID',
    resave: false,
    saveUninitialized: true,
    cookie: {
        secure: false
    }
}))

app.use(express.static(path.join(__dirname, "/static")));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

// Route Definition
const routes = require('./routes/routes.js')(app, request);



// Handle 404
app.use(function(req, res) {
    res.status(400);
    res.render("404.html", {
        title: "404: File Not Found"
    });
});

// Handle 500
app.use(function(error, req, res, next) {
    console.log("ERROR: " + error);
    res.status(500);
    res.render("500.html");
});

// Logging
require("console-stamp")(console, "ddd mmm dd yyyy HH:MM:ss");

nunjucks.configure("templates", {
    autoescape: true,
    express: app
});







app.listen(appPort, err => {
    if (err) {
        return console.log("CRITICAL: Something bad happened", err);
    }
    console.log(`NodeJS server is listening on TCP port ${appPort}`);
});
module.exports = app;