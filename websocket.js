// initialise variable
var ws,names = document.getElementById("selectNames"),
	rarity = document.getElementById("selectRarity"),
	skills = document.getElementById("selectSkills"),
 	main = document.getElementById("tblMain");
function connect(){
	alert("Page is loaded");
	if ("WebSocket" in window) {
		ws = new WebSocket("ws://localhost:5001");
		ws.binaryType = 'arraybuffer'; // using serialisation
		ws.onopen=function(e){
			console.log("connected");
 			// on successful connection, we want to create an initial subscription to load all the data into the page
			ws.send(serialize(['loadPage',[]]));
		};
		ws.onclose=function(e){console.log("disconnected");};
		ws.onmessage=function(e){
 			// deserialise incoming messages
 			var d = deserialize(e.data);
 			console.log(d);
			// messages should have format [‘function’,params]
 			// call the function name with the parameters
 			window[d.shift()](d[0]);
		};
		ws.onerror=function(e){console.log(e.data);};
 	} else alert("WebSockets not supported on your browser.");
}
function filterNames() {
	// get the values of checkboxes that are ticked and convert into an array of strings
	var t = [], s = names.children;
	for (var i = 0; i < s.length ; i++) {
		if (s[i].checked) { t.push(s[i].value); };
 	};
	// call the filterSyms function over the WebSocket
	ws.send(serialize(['filterNames',t]));
}
function filtering() {
	// get the values of checkboxes that are ticked and convert into an array of strings
	var t = [], s = rarity.children;
	for (var i = 0; i < s.length ; i++) {
		if (s[i].checked) { t.push(s[i].value); };
 	};
 	var u = [], v = skills.children;
	for (var i = 0; i < v.length ; i++) {
		if (v[i].checked) { u.push(v[i].value); };
 	};
	// call the filterSyms function over the WebSocket
	ws.send(serialize(['trimNames',t,u]));
}

function getSkills(data) {getValues(data,skills); }
function getRarity(data) {getValues(data,rarity); }
function getNames(data) {getValues(data,names); }
function getValues(data,t) {
	// parse an array of strings into checkboxes
	t.innerHTML = '';
	for (var i = 0 ; i<data.length ; i++) {
		t.innerHTML += '<input type="checkbox" name="sym" value="' +
	data[i] + '">' + data[i] + '</input>';
	};
}
function getMain(data) { main.innerHTML = tableBuilder(data); }
function tableBuilder(data) {
 // parse array of objects into HTML table
 var t = '<tr>'
 for (var x in data[0]) {
t += '<th>' + x + '</th>';
 }
  t += '</tr>';
 for (var i = 0; i < data.length; i++) {
t += '<tr>';
for (var x in data[0]) {
 t += '<td>' + (("time" === x) ?
data[i][x].toLocaleTimeString().slice(0,-3) : ("number" == typeof
data[i][x]) ? data[i][x].toFixed(2) : data[i][x]) + '</td>';
}
t += '</tr>';
 }
 return t ;
}