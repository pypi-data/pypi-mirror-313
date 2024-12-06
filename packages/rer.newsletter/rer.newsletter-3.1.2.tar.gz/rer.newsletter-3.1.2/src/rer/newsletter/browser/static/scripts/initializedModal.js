import $ from 'jquery';
import Modal from '@plone/mockup/src/pat/modal/modal';

function hide_element_modal() {
  $('.content_container').hide();
  $('.pattern-modal-buttons input').hide();
}

function init(modal) {
  var firstInput = null;
  var lastInput = null;
  var closeInput = null;

  portalMessage = $('.portalMessage.error');
  if (portalMessage.length > 0) {
    $('div.plone-modal-body')
      .find(portalMessage)
      .each(function () {
        if (portalMessage.text().indexOf('Error') > -1) {
          portalMessage.html(
            portalMessage.text().replace('Error', '<b>Attenzione</b>'),
          );
        }

        // trovare un metodo migliore
        if (
          $(portalMessage)
            .text()
            .indexOf(
              "Sei già iscritto a questa newsletter, oppure non hai ancora confermato l'iscrizione",
            ) > -1
        ) {
          hide_element_modal();

          var email = $('#form-widgets-email').val();
          var redirect = $('.redirect');
          var href = redirect.attr('href');
          redirect.attr('href', href + '?email=' + email);
          redirect.show();

          // modifica accessibilità
          firstInput = redirect;
          lastInput = redirect;
          closeInput = $('.button-plone-modal-close');
          firstInput.focus();
          // setTimeout(function(){ firstInput.focus(); }, 50);
        }
      });
  } else {
    // modifica accessibilità
    var inputs = $('.plone-modal-wrapper').find(
      'select, textarea, .redirect, button, input',
    );

    closeInput = $(inputs.splice(inputs.length - 1, 1)[0]);
    firstInput = inputs.first();
    lastInput = inputs.last();
    firstInput.focus();
  }

  $('.plone-modal-close').attr('title', 'chiudi');
  $('.pattern-modal-buttons').prepend($('.button-plone-modal-close'));

  if (lastInput && closeInput) {
    lastInput.on('keydown', function (e) {
      if (e.which === 9) {
        if (!e.shiftKey) {
          e.preventDefault();
          closeInput.focus();
        }
      }
    });
  }
  if (firstInput && closeInput) {
    firstInput.on('keydown', function (e) {
      if (e.which === 9) {
        if (e.shiftKey) {
          e.preventDefault();
          closeInput.focus();
        }
      }
    });
  }
  $('.button-plone-modal-close').on('click', function () {
    $('.plone-modal-close').click();
  });
  if (closeInput && lastInput && firstInput) {
    closeInput.on('keydown', function (e) {
      if (e.which === 9) {
        e.preventDefault();

        if (e.shiftKey) {
          lastInput.focus();
        } else {
          firstInput.focus();
        }
      }
    });
  }
  $('div.plone-modal-body')
    .find('.portalMessage.info')
    .each(function () {
      hide_element_modal();
    });
}

function render_modal(el) {
  modal = new Modal($(el), {
    backdropOptions: {
      closeOnEsc: true,
      closeOnClick: false,
    },
    content: '#content',
    loadLinksWithinModal: true,
    templateOptions: {
      classFooterName: 'plone-modal-footer subscribe_modal',
    },
    actionOptions: {
      timeout: 15000,
    },
  });
  modal.on('afterDraw', function () {
    init(modal);
  });
  modal.on('shown', function () {
    init(modal);
  });
  modal.on('linkActionSuccess', function () {
    init(modal);
  });
}

// aspetto che le tile all'interno della pagina siano caricate
$(document).ready(function () {
  if ($('body').hasClass('userrole-anonymous')) {
    $('.tileBody #channel-subscribe a').each(function (i, el) {
      render_modal(el);
    });
  } else {
    $('.tiles-management').on('rtTilesLoaded', function () {
      $('.tileBody #channel-subscribe a').each(function (i, el) {
        render_modal(el);
      });
    });
  }

  $('.portlet #channel-subscribe a').each(function (i, el) {
    render_modal(el);
  });
});
