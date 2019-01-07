const simpleGit = require('simple-git');


// Git status request
async function status (workingDir) {
   const git = require('simple-git/promise');
   
   let statusSummary = null;
   try {
      statusSummary = await git(workingDir).status();
   }
   catch (e) {
      // handle the error
   }
   
   return statusSummary;
}

// Git list repos

// using the async function
status(__dirname).then(status => console.log(status));

// using async list function
require('simple-git')()
    .listRemote(['--get-url'], (err, data) => {
        if (!err) {
            console.log('Remote url for repository at ' + __dirname + ':');
            console.log(data);
        }
    });
