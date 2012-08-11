
App = App || {}

App.showErrorMessage =  (heading, description) ->
    $('#alert-errors-heading').text(heading)
    $('#alert-errors-description').text(description)
    $('#alert-errors').fadeIn()

jQuery ->

    $('.nav-tabs a').on 'click', (event) ->
        $('.nav-tabs li').removeClass 'active'
        $('.tab-content').hide()
        
        link = $(@)
        $('#' + link.attr('data-tab-id')).show()
        link.parent().addClass 'active'

        false

    $('#submit-form').live 'submit', (event) ->

        form = $(@)
        url = form.attr 'action'
        params = form.serialize()

        callback  = (data) ->

            $('#priorities').html data.html

            if not data.success
                App.showErrorMessage 'Your form contains errors', 'Please correct the errors and carry on'


        $.post url, params, callback
    
        false
  
