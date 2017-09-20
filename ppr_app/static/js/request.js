$(document).ready(function() {
  $('#selectedquestions').children().hide();

  $('#type_select').on('change', function() {
      let type = $('#proj_type').find(":selected").text();
      let questions = [];

      if (type == 'CEO escalation') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'thp', 'wfmt', 'notes'];
      } else if (type == 'Community funded project') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'thp', 'wfmt', 'cfp', 'notes'];
      } else if (type == 'Ethernet tails') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'onea', 'notes'];
      } else if (type == 'FTTP tails') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'ogea', 'notes'];
      } else if (type == 'Spine') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'notes'];
      } else if (type == 'Whitespace') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'thp', 'wfmt', 'notes'];
      } else if (type == 'Commissioning') {
        questions = ['title', 'activity', 'exchange', 'pcp', 'dps', 'datereceived', 'daterequired', 'priority', 'requestedby', 'thp', 'wfmt', 'notes'];
      } else if (type == '') {
        questions = [];
      }

      $('#selectedquestions').children().each(function() {
        let id = $(this).attr('id');
        let index = questions.indexOf(id);

        if (index > -1) {
          $('#' + id).show();
        } else if (index == -1) {
          $('#' + id).hide();
        }
      })
  });
})
