$(document).ready(hideAllErrors)

function hideAllErrors() {
    var errors = $('.form-group #alert');
    errors.each($(this).removeClass("collapse"));
}





function isEmpty(data) {
    if (data.length == 0) {
      return false;
    } else {
      return true;
    }
}

function isLength(data, min, max) {
    if (data > max || data < min) {
      return false;
    } else {
      return true;
    }
}

function isAlphanumeric(data) {
    var letterNumber = /^[0-9a-zA-Z]+$/;
    if (data.match(letterNumber)) {
      return true;
    } else {
      return false;
    }
}

function isNumber() {
    var number = /^[0-9]+/
    if (data.match(number)) {
      return true;
    } else {
      return false;
    }
}


function validateForm() {

}
