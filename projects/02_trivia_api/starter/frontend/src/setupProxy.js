const proxy = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(proxy('/questions', { target: 'http://0.0.0.0:5000/' }));
  app.use(proxy('/categories', { target: 'http://0.0.0.0:5000/' }));
};