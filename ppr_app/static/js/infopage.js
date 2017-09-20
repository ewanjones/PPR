$(document).ready(function () {

    // Get status update using AJAX
    let getStatus = function(row, pid, callback) {
      $.ajax({
        type: 'GET',
        url: 'http://46.101.47.45/PPR/api/status',
        data: {'pid': pid},
        success: function(data) {
          var response = JSON.parse(data);
          callback(row, response);
        }
      });
    }

    // Get project details using AJAX
    let getProject = function(pid, callback) {
      $.ajax({
        type: 'GET',
        url: 'http://46.101.47.45/PPR/api/project',
        data: {'pid': pid},
        success: function(data) {
          var response = JSON.parse(data);
          callback(response);
        }
      });
    }

    // Colour status icons in table
    $('tbody').children().each(function() {
      let row = $(this)
      let pid = $(this).find('#pid').text();
      getStatus(row, pid, function(row, response) {
        row.find('#statusColumn').children().each(function(){
          let stage = $(this).attr('id')
          if (response[stage] == 'Unallocated') {
            stateColor = 'red'
          } else if (repsonse[stage] == 'Allocated') {
            stateColor = 'green'
          } else if (repsonse[stage] == 'Complete') {
            stateColor = 'blue'
          }
          $(this).css('color', stateColor);
        })
      })
    })

    // Bring up modal when row clicked and populate
    $('tbody').children().each(function() {
      $(this).on('click', function() {
        let pid = $(this).find('#pid').text();
        // get project details and insert into modal
        getProject(pid, function(response) {
          $('#editModal').find('#pid').text(response.pid);
          $('#editModal').find('#title').text(response.title);
          $('#editModal').find('#type').text(response.type);
          $('#editModal').find('#product').text(response.product);
          $('#editModal').find('#activity').text(response.activity);
          $('#editModal').find('#exchange').text(response.exchange);
          $('#editModal').find('#pcp').text(response.pcp);
          $('#editModal').find('#dps').text(response.dps);
          $('#editModal').find('#dateReceived').text(response.dateReceived);
          $('#editModal').find('#dateRequired').text(response.dateRequired);
          $('#editModal').find('#priority').text(response.priority);
          $('#editModal').find('#requestedBy').text(response.requestedBy);
          $('#editModal').find('#thp').text(response.thp);
          $('#editModal').find('#other').text(response.other);
        });
        $('#editModal').modal('show');
      })
    })

});
