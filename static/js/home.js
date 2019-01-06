/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'aus': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/led',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
        },
        ein: function(minutes, passw) {
            let ajax_options = {
                type: 'POST',
                url: 'api/led',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'minutes': minutes,
                    'passw': passw
                })
            };
            $.ajax(ajax_options)
        },
        'howlong': function() {
          let ajax_options = {
              type: 'GET',
              url: 'api/stats',
              accepts: 'application/json',
              dataType: 'json'
          };
          $.ajax(ajax_options)
          .done(function(data) {
              $event_pump.trigger('model_uptime_read_success', [data]);
          })
      },
    };
}());


// Create the view instance
ns.view = (function() {
  'use strict';

  // return the API
  return {
      build_uptime: function(x) {
          if (x) {
              var paragraph = document.getElementById("uptime");
              var text = document.createTextNode(x[0].uptime);
              paragraph.appendChild(text);
          }
      }
  };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $minutes = $('#minutes'),
        $passw = $('#passw');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.howlong();
    }, 100)

    // Validate input
    function validate(minutes, passw) {
        return minutes !== "" && passw !== "";
    }

    // Create our event handlers
    $('#ein').click(function(e) {
        let minutes = $minutes.val(),
            passw = $passw.val();

        e.preventDefault();
        if (minutes !== "" && passw !== "" && minutes<21 && minutes.length<3 && passw.length < 10) {
            model.ein(minutes, passw)
        } else {
            alert('Eingabe war falsch.');
        }

    });

    $('#aus').click(function(e) {
        e.preventDefault();
        model.aus()
    });

    // Handle the model events
    $event_pump.on('model_uptime_read_success', function(e, data) {
      view.build_uptime(data);
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
