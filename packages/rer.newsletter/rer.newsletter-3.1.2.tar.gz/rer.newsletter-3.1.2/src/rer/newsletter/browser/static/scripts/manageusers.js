import $ from 'jquery';
import Modal from '@plone/mockup/src/pat/modal/modal';
import './datatables';

function render_error(message) {
  $('.portalMessage')
    .removeClass('alert-info')
    .addClass('alert-danger')
    .addClass('alert')
    .attr('role', 'alert')
    .css('display', '')
    .html('<strong>Error</strong> ' + message);
}

function render_info(message) {
  $('.portalMessage')
    .removeClass('alert-danger')
    .addClass('alert-info')
    .addClass('alert')
    .attr('role', 'status')
    .css('display', '')
    .html('<strong>Info</strong> ' + message);
}

$(document).ready(function () {

  // triggero l'apertura delle modal
  $('#users-export > span').on('click', function () {
    $.ajax({
      url: 'exportUsersListAsFile',
    }).done(function (data) {
      var blob = new Blob(['\ufeff', data]);
      var url = URL.createObjectURL(blob);

      var downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'data.csv';

      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    });
  });

  $('#delete-user > span').on('click', function () {
    if (!user_table.row('.selected').data()) {
      render_error('Prima va selezionato un utente.');
    } else {
      $.ajax({
        url: 'deleteUser',
        type: 'post',
        data: {
          email: user_table.row('.selected').data().email,
        },
      }).done(function (data) {
        if (JSON.parse(data).ok) {
          user_table.row('.selected').remove().draw(false);
          render_info('Utente eliminato con successo.');
        } else {
          render_error("Problemi con la cancellazione dell'utente");
        }
      });
    }
  });

  new Modal($('#button-add-user'), {
    backdropOptions: {
      closeOnEsc: false,
      closeOnClick: false,
    },
    actionOptions: {
      onSuccess: reload_table,
      timeout: 15000,
    },
  });
  new Modal($('#button-import-users'), {
    backdropOptions: {
      closeOnEsc: false,
      closeOnClick: false,
    },
    actionOptions: {
      onSuccess: reload_table,
      timeout: 15000,
    },
  });

  // inizializzazione datatables
  var user_table = $('#users-table').DataTable({
    language: {
      url: 'https://cdn.datatables.net/plug-ins/1.10.16/i18n/Italian.json',
    },
    ajax: {
      url: 'exportUsersListAsJson',
      dataSrc: '',
    },
    columns: [
      { data: 'email' },
      { data: 'creation_date' },
      { data: 'is_active' },
    ],
  });

  $('#users-table tbody').on('click', 'tr', function () {
    if ($(this).hasClass('selected')) {
      $(this).removeClass('selected');
    } else {
      user_table.$('tr.selected').removeClass('selected');
      $(this).addClass('selected');
    }
  });

  function reload_table($action, response, options) {
    var count = user_table.data().count();
    user_table.ajax.reload(function (json) {
      var num_users = json.length - count;
      if (num_users > 0) {
        if (num_users == 1) {
          render_info('Aggiunto ' + num_users + ' utente.');
        } else {
          render_info('Aggiunti ' + num_users + ' utenti.');
        }
      } else if (num_users < 0) {
        if (Math.abs(num_users) == 1) {
          render_info('Rimosso ' + Math.abs(num_users) + ' utente.');
        } else {
          render_info('Rimossi ' + Math.abs(num_users) + ' utenti.');
        }
      }
    });
    $action.$modal.trigger('destroy.plone-modal.patterns');
  }
});
