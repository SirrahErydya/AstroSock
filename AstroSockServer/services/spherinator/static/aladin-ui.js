
let hierarchy = 1

// URLs
const cat_url = {}
const cube_url = {}

let aladin;

// DOM Elements
const aladin_div = document.getElementById('aladin-lite-div')
const aladin_layer_radios = document.getElementsByName("aladin-layer-radio")
const coord_display = document.getElementById('coordinates-display')

// Init socket
window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:" + port + '/');
    subscribe(websocket)
    send_datapoint(websocket)
    receive(websocket)
})

function subscribe(websocket) {
    websocket.addEventListener("open", e => {
        websocket.send(JSON.stringify({type: 'subscribe'}))
    })
}

function send_datapoint(websocket) {
    document.addEventListener("choose_datapoint", e => {
        const msg = e.detail
        websocket.send(JSON.stringify(msg))
      });
}

function receive(websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        alert("I received a message!")
        if(event.type == "datacube_broadcast") {
            alert("I received a datacube!")
        }
      });
}



A.init.then(() => {
    aladin = A.aladin('#aladin-lite-div', {
        "showGotoControl": false,
        "showLayersControl": false,
        "showProjectionControl": false,
        "showFullscreenControl": false,
        "showFrame": false,
        "showCooLocation": false,
        "showFov": false,
        "fov": 360
    });
    let model_url = survey_url + '/' + 'model'
    //let model_url = "/services/spherinator/static/surveys/TNG100-99/model"
    let projection_url = survey_url  + '/' + 'projection'
    let model_survey = aladin.createImageSurvey(survey.name + '-model',
        survey.name + ' Model', model_url,
        'equatorial', 3, {imgFormat: 'jpg'})
    let projection_survey = aladin.createImageSurvey(survey.name + '-projection',
        survey.name + ' Morphology Images', projection_url,
        'equatorial', 3, {imgFormat: 'jpg'})

    let survey_to_show = document.querySelector('input[name="aladin-layer-radio"]:checked').value;
    aladin.setBaseImageLayer(survey_to_show);
    aladin.on('rightClickMove', function(e) {
        //e.preventDefault();
        return false;
    })

});

function choose_datapoint(event) {
    let order = aladin.view.wasm.getNOrder()
    let radec = aladin.pix2world(event.x, event.y)
    let theta =  Math.PI / 2. - radec[1] / 180. * Math.PI;
    let phi = radec[0] / 180. * Math.PI
    const msg = {
        type: 'pick_spherinator_cell',
        survey: survey,
        order: order,
        theta: theta,
        phi: phi
    }
    coord_display.style = "display: block;"
    coord_display.innerHTML = "<span>Theta: " + theta + "; Phi: " + phi + "</span>"
    const dp_event = new CustomEvent('choose_datapoint', { detail: msg})

    document.dispatchEvent(dp_event)
}


/** Event listeners **/
aladin_div.addEventListener("mouseup", function(ev) {
    if(ev.button === 2) {
        choose_datapoint(ev)
    }
})



// Aladin Layer change
for(let i=0; i < aladin_layer_radios.length; i++) {
    aladin_layer_radios[i].addEventListener('change', function(e) {
        let survey_id = this.value;
        aladin.setBaseImageLayer(survey_id)
    })
}





