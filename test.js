var https = require('https');
var jsonQuery = require('json-query');

var options = {
    host: 'api.github.com',
    path: '/users/wessenstam/repos',
    headers: {
        'User-Agent': 'MY IPHINE 7s'}

}
var request = https.request(options, function (res) {
    var data = '';
    res.on('data', function (chunk) {
        data += chunk;
    });
    res.on('end', function () {
        // Only show the name of the repos
        jsonQuery('name', {
            data: data
        });
        console.log(data);
    });
});
request.on('error', function (e) {
    console.log(e.message);
});
request.end();