
// Load the required modules
var https = require('https');
var jp = require('jsonpath');

// Create the URL to get the JSON list
var options = {
    host: 'api.github.com',
    path: '/users/nutanixworkshops/repos',
    headers: {
        'User-Agent': 'MY IPHINE 7s'}

}

// Get the JSON from the URL
var request = https.request(options, function (res) {
    var data = '';
    res.on('data', function (chunk) {
        data += chunk;
    });

    // Get the full_names from the returned data
    res.on('end', function () {
        console.log(data);
        var names= JSON.parse(data);
        var Repos = jp.query(names,'$.._name');
        //var Repos_URL = jp.query(names,'$..name');
        console.log(Repos);
            
    });
});
request.on('error', function (e) {
    console.log(e.message);
});
request.end();