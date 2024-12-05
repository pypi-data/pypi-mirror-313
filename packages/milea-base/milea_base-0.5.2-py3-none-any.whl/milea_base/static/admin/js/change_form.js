// Django Default
'use strict';
{
    const inputTags = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
    const modelName = document.getElementById('django-admin-form-add-constants').dataset.modelName;
    if (modelName) {
        const form = document.getElementById(modelName + '_form');
        for (const element of form.elements) {
            // HTMLElement.offsetParent returns null when the element is not
            // rendered.
            if (inputTags.includes(element.tagName) && !element.disabled && element.offsetParent) {
                element.focus();
                break;
            }
        }
    }
}

// Tom Select - Multiple
document.querySelectorAll('.form-select').forEach((el)=>{
    let settings = {
        copyClassesToDropdown: false,
        dropdownParent: 'body',
        controlInput: '<input>',
        render:{
            item: function(data,escape) {
                if( data.customProperties ){
                    return '<div><span class="dropdown-item-indicator">' + data.customProperties + '</span>' + escape(data.text) + '</div>';
                }
                return '<div>' + escape(data.text) + '</div>';
            },
            option: function(data,escape){
                if( data.customProperties ){
                    return '<div><span class="dropdown-item-indicator">' + data.customProperties + '</span>' + escape(data.text) + '</div>';
                }
                return '<div>' + escape(data.text) + '</div>';
            },
        },
    };
    new TomSelect(el, settings);
});

// Systemdaten als letztens im Main Container anzeigen
document.addEventListener("DOMContentLoaded", function() {
    var mileaSystemData = document.querySelector('.milea-system-data');
    if (mileaSystemData != null) {
        var contentMain = document.querySelector('#content-main');
        contentMain.appendChild(mileaSystemData);
    }
});

// Add warning when input is changed
document.addEventListener('DOMContentLoaded', function() {
    var inputs = document.querySelectorAll('form input, form select, form textarea');

    inputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var card = this.closest('.card');
            console.log(card)

            if (card) {
                var cardStatusTop = card.querySelector('.card-status-top');
                
                if (cardStatusTop) {
                    cardStatusTop.classList.add('bg-warning');

                    var ribbon = cardStatusTop.querySelector('.ribbon');
                    if (ribbon && ribbon.classList.contains('d-none')) {
                        ribbon.classList.remove('d-none');
                    }
                }
            }
        });
    });
});
