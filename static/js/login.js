$(document).ready(function() {
  $("#login-form").validate({
    errorClass: "is-invalid",
    validClass: "is-valid",
    errorElement: "div",
    onfocusout: function(elem) { this.element(elem); },
    errorPlacement: function(error, element) {
      error.addClass("invalid-feedback");
      element.after(error);
    },
    rules: {
      login: { required: true },
      password: { required: true }
    },
    messages: {
      login: { required: "請輸入用戶名或電子郵件" },
      password: { required: "請輸入密碼" }
    },
    invalidHandler: function(event, validator) {
      if (validator.errorList.length) {
        $("#form-non-field-errors")
          .removeClass("d-none")
          .text("");
      } else {
        $("#form-non-field-errors").addClass("d-none").text("");
      }
    },
    success: function(label, element) {
      $("#form-non-field-errors").addClass("d-none").text("");
    },
  });
});

var serverErrors = $(".nonfield, .errorlist.nonfield, .errorlist li").text();
  if (serverErrors && serverErrors.length > 0) {
    $("#form-non-field-errors")
      .removeClass("d-none")
      .text(serverErrors);
  }