
let hierarchy = 1

// URLs
const cat_url = {}
const cube_url = {}

let aladin;

// DOM Elements
const aladin_div = document.getElementById('aladin-lite-div')
const aladin_layer_radios = document.getElementsByName("aladin-layer-radio")


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
    for(let survey_name in surveys) {
        alert(surveys[survey_name])
        let model_url = surveys[survey_name] + '/' + 'model'
        //let model_url = "/services/spherinator/static/surveys/TNG100-99/model"
        let projection_url = surveys[survey_name]  + '/' + 'projection'
        let model_survey = aladin.createImageSurvey(survey_name + '-model',
            survey_name + ' Model', model_url,
            'equatorial', 3, {imgFormat: 'jpg'})
        let projection_survey = aladin.createImageSurvey(survey_name + '-projection',
            survey_name + ' Morphology Images', projection_url,
            'equatorial', 3, {imgFormat: 'jpg'})
    }

    let survey_to_show = document.querySelector('input[name="aladin-layer-radio"]:checked').value;
    aladin.setBaseImageLayer(survey_to_show);
    /*
    aladin.on('mouseMove', function (e) {
        let order = aladin.view.wasm.getNOrder()
        let radec = aladin.pix2world(e.x, e.y)
        update_hp_index(radec[0], radec[1], 2**order)
    })*/
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
    let top_index = new HealpixIndex(2**order)
    top_index.init()
    let top_pixel = top_index.ang2pix_nest(theta, phi)
    let csv_idx;
    if(hierarchy > 0) {
        let nested_index = new HealpixIndex(2**(order+hierarchy))
        nested_index.init()
        csv_idx = nested_index.ang2pix_nest(theta, phi) - 4*top_pixel
        //alert("Order: " + order + "; Top Pixel: " + top_pixel + "; CSV Idx: " + csv_idx)
    }
    let csv_url = cat_url + '/Norder'+ order + '/Dir0/Npix' + top_pixel + '.tsv';
    return {
        "csv_url": csv_url,
        "csv_idx": csv_idx
    }
}


/** Event listeners **/
/* aladin_div.addEventListener("mouseup", function(ev) {
    if(ev.button === 2) {
        let data = choose_datapoint(ev)
        if (!jasmine_window || !jasmine_window.opener || jasmine_window.opener.closed ||
            window_mode == "multi-modal" ) {
            jasmine_window = window.open(
                'http://localhost:5173/modals/jasmine-viewer.html', '_blank',
                'location=yes,height=1000,width=1000,top=0,left=1500,scrollbars=no');
            jasmine_window.addEventListener('load', e => jasmine_window.postMessage(data));
        } else {
            // Just JavaScript being JavaScript I guess...
            jasmine_window.postMessage(data);
        }

    }
})
*/

// Aladin Layer change
for(let i=0; i < aladin_layer_radios.length; i++) {
    aladin_layer_radios[i].addEventListener('change', function(e) {
        let survey_id = this.value;
        aladin.setBaseImageLayer(survey_id)
    })
}



