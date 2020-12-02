function startLocalSimulation(websocket_address) {
	var websocket_docker = new WebSocket("ws://" + websocket_address + ":8765/");

	websocket_docker.onopen = function (event) {
		console.log("Conectado al docker manegr");
		websocket_docker.send("open");
	}
	websocket_docker.onclose = function (event) {
		if (event.wasClean) {
			alert(`[close] Connection closed cleanly manager, code=${event.code} reason=${event.reason}`);
		} else {
			alert("[close] Connection closed! manager");
		}
	}

}