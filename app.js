const USER = 'wessenstam';
const PASS = 'Sas061251';
const REPO = 'github.com/wessenstam/apitest';
 
const git = require('simple-git/promise');
const remote = `https://${USER}:${PASS}@${REPO}`;

require('simple-git')()
     .outputHandler((command, stdout, stderr) => {
        stdout.pipe(process.stdout);
        stderr.pipe(process.stderr);
     })
     .checkout('https://github.com/wessenstam/apitest.git');