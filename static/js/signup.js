$(function() {
  $("#register-form").validate({
    errorClass: "is-invalid",
    validClass: "is-valid",
    errorElement: "div",
    onfocusout: function(elem) { this.element(elem); },
    errorPlacement: function(error, element) {
      error.addClass("invalid-feedback");
      element.after(error);
    },
    rules: {
      username: {
        required: true,
        minlength: 6,
        maxlength: 20,
        pattern: /^[A-Za-z0-9]+$/
      },
      password1: {
        required: true,
        minlength: 8,
        notEqualToUsername: true
      },
      password2: {
        required: true,
        minlength: 6,
        equalTo: "#id_password1"
      }
    },
    messages: {
      username: {
        required: "請輸入用戶名稱",
        minlength: "至少 6 個字元",
        maxlength: "最多 20 個字元",
        pattern: "只能使用英數字"
      },
      password1: {
        required: "請輸入密碼",
        minlength: "密碼至少需 8 個字元",
        pwcheck: "密碼需包含英文字母與數字，且不可全為數字",
        notEqualToUsername: "密碼不可與用戶名相同"
      },
      password2: {
        required: "請確認密碼",
        minlength: "密碼至少需 6 個字元",
        equalTo: "兩次密碼輸入不一致"
      }
    }
  });

  var serverErrors = $(".nonfield, .errorlist.nonfield, .errorlist li").text();
  if (serverErrors && serverErrors.length > 0) {
    $("#form-non-field-errors")
      .removeClass("d-none")
      .text(serverErrors);
  }
});