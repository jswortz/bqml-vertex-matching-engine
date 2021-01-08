var express = require('express');
var app = express();
var path = require('path');
app.use(express.static('dist/retail'));
app.get('/', function (req, res,next) {
    res.sendFile(path.join(__dirname+'/dist/retail','index.html'));
});
app.get('/product', function (req, res,next) {
    res.sendFile(path.join(__dirname+'/dist/retail','index.html'));
});
app.get('/product/:product_id', function (req, res,next) {
    res.sendFile(path.join(__dirname+'/dist/retail','index.html'));
});
app.get('/bag', function (req, res,next) {
    res.sendFile(path.join(__dirname+'/dist/retail','index.html'));
});
app.listen(8080)