
/*
Modal Functionalitiy
*/

function openCustomModal(url) {
  $('#custom-modal').load(url, function() {
    $(this).modal('show');
  });
  return false;
}

function closeCustomModal() {
  $('#custom-modal').modal('hide');
  return false;
}

$('#id_region').on('change', function() {

  console.log("cambia la comunidad autonoma");
  $("#id_province").empty();

  loadElements(function(data) {
    //console.log(data);
    var opts = showElements(data);
    $("#id_province").append(opts);
  });

})

/*
---------- Dynamic Regions ----------
*/

function loadElements(callback) {

  console.log("cargar elementos");

  var region = $('#id_region').val();
  console.log(region);

  $.ajax({
    method: "GET",
    url: '/checkout/cargar_elementos/',
    dataType: 'json',
    data: {
      region: region,
    },
    success: function(data) {
      console.log("SUCCESS");
      callback(data);
    },
    error: function(response) {
      console.log("ERROR");
      callback(response);
    }
  });
}

function showElements(param) {

  console.log("mostrar elementos");
  console.log(param);

  var values = "";

  for (var i = 0; i < param.length; i++) {
    console.log(param[i]);
    values += "<option value='" + param[i].pk + "'>" + param[i].fields.name + "</option>";
  }
  return values;
}




//
