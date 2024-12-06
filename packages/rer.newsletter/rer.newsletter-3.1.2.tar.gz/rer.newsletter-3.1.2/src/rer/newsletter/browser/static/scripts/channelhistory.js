import $ from 'jquery';
import './datatables';

$(document).ready(function () {
  $('#delete-message-sent > span').on('click', function () {
    if (!table.row('.selected').data()) {
      // render error user deleted
      $('.portalMessage')
        .removeClass('alert-info')
        .addClass('alert')
        .addClass('alert-danger')
        .attr('role', 'alert')
        .css('display', '')
        .html('<strong>Error</strong> Prima va selezionato un messaggio.');
    } else {
      $.ajax({
        url: 'deleteMessageFromHistory',
        type: 'post',
        data: {
          message_history: table.row('.selected').data().uid,
        },
      }).done(function (data) {
        if (JSON.parse(data).ok) {
          table.row('.selected').remove().draw(false);
          $('.portalMessage')
            .removeClass('alert-danger')
            .addClass('alert')
            .addClass('alert-info')
            .attr('role', 'status')
            .css('display', '')
            .html(
              '<strong>Info</strong> Storico del messaggio eliminato con successo.',
            );
        } else {
          $('.portalMessage')
            .removeClass('alert-info')
            .addClass('alert')
            .addClass('alert-danger')
            .attr('role', 'alert')
            .css('display', '')
            .html(
              '<strong>Error</strong> Problemi con la cancellazione dello storico del messaggio.',
            );
        }
      });
    }
  });

  // inizializzazione datatables
  var table = $('#message-table').DataTable({
    language: {
      url: 'https://cdn.datatables.net/plug-ins/1.10.16/i18n/Italian.json',
    },
    ajax: {
      url: 'getMessageSentDetails',
      dataSrc: '',
    },
    ordering: false,
    columns: [
      { data: 'uid' },
      { data: 'message' },
      { data: 'subscribers' },
      { data: 'send_date_start' },
      { data: 'send_date_end' },
      {
        data: 'completed',
        render: function (data, type, row) {
          if (row.running) {
            return 'In corso';
          }
          return row.completed ? 'Inviata' : 'Errore';
        },
      },
    ],
    columnDefs: [
      {
        targets: [0],
        visible: false,
        searchable: false,
      },
    ],
  });

  $('#message-table tbody').on('click', 'tr', function () {
    if ($(this).hasClass('selected')) {
      $(this).removeClass('selected');
    } else {
      table.$('tr.selected').removeClass('selected');
      $(this).addClass('selected');
    }
  });
});
