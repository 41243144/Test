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
        }
    },
    messages: {
        username: {
        required: "請輸入用戶名稱",
        minlength: "至少 6 個字元",
        maxlength: "最多 20 個字元",
        pattern: "只能使用英數字"
        }
    },
    invalidHandler: function(event, validator) {
        if (validator.errorList.length) {
        $("#form-non-field-errors")
            .removeClass("d-none")
            .text(validator.errorList[0].message);
        } else {
        $("#form-non-field-errors").addClass("d-none").text("");
        }
    },
    success: function(label, element) {
        $("#form-non-field-errors").addClass("d-none").text("");
    },
    });
});