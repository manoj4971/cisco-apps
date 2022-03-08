const redis = require("redis");

 // DB Connection. In this case is Redis Client 
 const redisHost = process.env.REDIS_SERVICE 
 const redisPort = process.env.REDIS_PORT 

 const dbConnection = redis.createClient(redisPort, redisHost);
 
 dbConnection.on("connect", function () {
     redisReachable = true;
     console.log("DBService: Redis is reachable" )
 });

 dbConnection.on("error", function (err) {
     redisReachable = false;
     console.log("DBService: Redis is not reachable")
 });

 module.exports = dbConnection