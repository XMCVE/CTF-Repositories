const express = require('express');
const http = require('http');
const {json} = require("express");
const {mergeObjects,merge,checkValue} = require("./utils");
const cors = require('cors');
const Redis = require('ioredis');
const url = require('url');
const crypto = require('crypto');
const fs = require('fs');

const app = express();

app.use(cors());

const redis = new Redis();

var validUrls = {"urls": {}};
var liveUrls = {"urls":{}};

const secureRandom = crypto.randomBytes(32).toString('hex');

app.get("/api/server", (req, res) => {
    let responseData = {
        success : true,
        message : "Hello SCTF",
    }
    return res.json(responseData);
});

app.get("/api/server/nodes", (req, res) => {
    return res.json(liveUrls);
});


app.get('/api/server/check', (req, res) => {
    const { hostname, path } = req.query;

    const options = {
        protocol: "http:",
        hostname: hostname,
        path: path,
        port: "80",
    }

    if (!hostname ) {
        let responseData = {
            success : false,
            message : 'Hostname and port are mandatory.'
        }
        return res.json(responseData);
    }

    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        let responseData = {
            success : false,
            message : 'Access denied.'
        }
        return res.json(responseData);
    }

    if (!checkValue(validUrls,hostname)){
        let responseData = {
            success : false,
            message : 'Add the domain to the whitelist before proceeding.'
        }
        return res.json(responseData);
    }

    http.get(options, (response) => {
        if (response.statusCode !== 200) {
            let responseData = {
                success : false,
                message : 'Target url status code :'+response.statusCode,
            }
            return res.json(responseData);
        }
        mergeObjects(liveUrls,validUrls,hostname);
        console.log(`Added ${hostname} to liveUrls array.`);

        let resData = '';
        response.on('data', (chunk) => {
            resData += chunk;
        });

        response.on('end', () => {
            let responseData = {
                success : true,
                message : resData
            };
            return res.json(responseData);
        });

    }).on('error', (error) => {
        let responseData = {
            success : false,
            message : error.message
        }
        return res.json(responseData);
    });
});

app.get("/api/server/import", (req, res) => {
    const keys = Object.keys(req.query);

    keys.forEach(function(key) {
        merge(validUrls,key,req.query[key]);
    });

    console.log(validUrls);
    let responseData = {
        success : true,
        message : "Successfully added the address to the whitelist"
    };
    return res.json(responseData);
});

app.get("/api/server/admin/login", async (req, res) => {
    const { accesskey } = req.query;
    if (accesskey !== secureRandom){
        let responseData = {
            success : false,
            message : "Login fail"
        };
        return res.json(responseData);
    }
    await redis.set("IsAdminSession", "1");
    let responseData = {
        success : true,
        message : "Login success"
    };
    return res.json(responseData);
});

app.get("/api/server/getflag",async  (req, res) => {
    try {
        const value = await  redis.get("IsAdminSession");

        if (value !== null) {
            const flag = fs.readFileSync('/flag','utf8');
            const responseData = {
                success: true,
                message: flag,
            };
            return res.json(responseData);
        } else {
            return res.json({ success: false, message: "IsAdminSession not found" });
        }
    } catch (error) {
        console.error("Error:", error);
        return res.status(500).json({ success: false, message: "Internal Server Error" });
    }
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
