const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const DIR = __dirname;

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  let file = reqPath === '/' ? '/index.html' : reqPath;
  let filePath = path.join(DIR, file);

  fs.readFile(filePath, (err, data) => {
    if (err) {
      filePath = path.join(DIR, 'index.html');
      fs.readFile(filePath, (err2, data2) => {
        if (err2) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('404 Not Found');
        } else {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(data2);
        }
      });
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const mime = {
      '.html': 'text/html; charset=utf-8',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.js': 'application/javascript',
      '.css': 'text/css'
    }[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': mime,
      'Access-Control-Allow-Origin': '*'
    });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`Node server listening on port ${PORT} (dual-stack IPv4/IPv6)`);
});

