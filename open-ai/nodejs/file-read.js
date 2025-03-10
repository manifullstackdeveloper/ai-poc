const fs = require('fs');

const readStream = fs.createReadStream('/Downloads/test1.pdf', 'utf8');

readStream.on('data', (chunk) => {
    console.log('Received chunk:', chunk);
});

readStream.on('end', () => {
    console.log('Finished reading file');
});

readStream.on('error', (err) => {
    console.error('Error reading file:', err);
});
