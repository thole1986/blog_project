"use strict";

// $("select").selectric();
$.uploadPreview({
  input_field: "#image",   // Default: .image-upload
  preview_box: "#image-preview",  // Default: .image-preview
  label_field: ".form-label[for='image']",    // Default: .image-label
  label_default: "Chọn hình",   // Default: Choose File
  label_selected: "Thay đổi",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null,
});
// $(".inputtags").tagsinput('items');
