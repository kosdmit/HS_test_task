let isAuthenticated

$(document).ready(function() {
  getProfile()
});

$('#phone-number-submit-button').click(function () {
  $.ajax({
    type: 'POST',
    // headers: {'X-CSRFToken': csrftoken},
    url: '/api/auth/',
    data: {
      'phone_number': $('#id_phone_number').val(),
      'auth_code': $('#id_auth_code').val(),
    },
    success: function (response) {
      console.log(response)
      if (response['auth_code_sending_status'] === 'success') {
        $('#id_auth_code').parent().show()
      } else if (response['auth_status'] === 'success') {
        isAuthenticated = true
        $('#phone-number-input-block').hide()
        getProfile()
      }


    }
  })
})


$('#referral-code-submit-button').click(function () {
  $.ajax({
    type: 'POST',
    // headers: {'X-CSRFToken': csrftoken},
    url: '/api/profile/',
    data: {
      'referral_code': $('#id_referrer_code').val(),
    },
    success: function (response) {
      console.log(response)
      if (response['message'] === 'success') {
        $('#referral-form').hide()
        getProfile()
      } else if (response['auth_status'] === 'success') {
        $('#phone-number-input-block').hide()
        getProfile()
      }


    }
  })
})


function getProfile () {
  $.ajax({
    type: 'GET',
    // headers: {'X-CSRFToken': csrftoken},
    url: '/api/profile/',
    dataType: 'json',
    success: function (response) {
      console.log(response)
      isAuthenticated = true
      $('#phone-number-value').text(response['phone_number'])
      $('#own-referral-code-value').text(response['own_referral_code'])
      if (response['activated_referral_code']) {
        $('#referral-form').hide()
        $('#activated-referral-code').show()
        $('#activated-referral-code-value').text(response['activated_referral_code'])
      }
      for (let i=0; i<response['referrals'].length; i++) {
        $('#referrals-list').append(
            '<li class="list-group-item">' + response['referrals'][i] + '</li>'
        )
      }
      $('#profile-block').show()
    },
    error: function (response) {
      console.log(response)
      if (response.status === 403) {
        isAuthenticated = false
        $('#phone-number-input-block').show()
      }
    },
  });
}

