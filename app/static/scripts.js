function post_json(path, data) {
    return post(path, data).then((response) => {
        return response.json()
    })
}

function post(path, data) {
    return window.fetch(path, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(data)
    });
}

function post_multipart_json(path, data) {
    return post_multipart(path, data).then((response) => {
        return response.json()
    })
}

function post_multipart(path, data) {
    return window.fetch(path, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
        body: data
    });
}


var btn = document.getElementById('button');
var file = document.getElementById('file');
var name = document.getElementById('name');
var convert = document.getElementById('convert');
var download = document.getElementById('download');
var audio_player = document.getElementById('audio_player');
var audio_player_no_voice = document.getElementById('audio_player_no_voice');
var audio_source = document.getElementById('audio_source');
var audio_source_no_voice = document.getElementById('audio_source_no_voice');


btn.addEventListener("click", function(evt){
	file.click()
	evt.preventDefault();
});
convert.addEventListener("click", function(evt){
	post_multipart_json("/predict",new FormData(document.getElementById("form"))).then(data => {
		convert.style.display = "none";
		download.style.display = "inline-block";
		download.href = data["voice"]
        audio_source.src = data["voice"]
        audio_source_no_voice.src = data["no_voice"]
        audio_player.load()
        audio_player_no_voice.load()
	}).catch(err => {
	    console.log({ err })
	})
	evt.preventDefault();
});
file.onchange = function(e) {
  download.style.display = "none";
  convert.style.display = "inline-block";
  var file = e.target.files[0];
  document.getElementById('name').innerHTML = "Description: </br>name: "+ file.name+" </br>size: "+file.size;
};