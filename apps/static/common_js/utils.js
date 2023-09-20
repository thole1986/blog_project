function showModal(modal_id){
    $("#"+modal_id).modal('show');
}

function hideModal(modal_id){
    $("#"+modal_id).modal('hide');
}

function showLoading(position = 'fixed') {
    const divLoading = document.querySelector('.content-loading');
    if (divLoading && !divLoading.classList.contains('show')) {
        divLoading.style.position = position;
        divLoading.classList.add('show');
    }
}

function hideLoading() {
    const divLoading = document.querySelector('.content-loading');
    if (divLoading) {
        divLoading.classList.remove('show');
        divLoading.removeAttribute('style');
    }
}

function reloadPage() {
    window.location.reload();
}

function getFormData(formID) {
    let serialized = [];
    const form = document.getElementById(formID);
    if (form) {
        // Loop through each field in the form
        for (let i = 0; i < form.elements.length; i++) {
            let field = form.elements[i];
            if (!field.name || field.disabled || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue;

            if ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked) {
                serialized.push({
                    field_name: field.name,
                    value: field.value
                });
            }
        }
    }
    return serialized;
}

function getCheckedBoxes(checkBoxName) {
    const checkboxes = document.getElementsByName(checkBoxName);
    const checkboxesChecked = [];
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked && checkboxes[i].value) {
            checkboxesChecked.push(checkboxes[i].value.toString());
        }
    }
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

const changeBackgroundSelected = function (inputChecked) {
    if (inputChecked.checked) {
        $(inputChecked).closest('a.list-group-item').addClass('selected-page');
    } else {
        $(inputChecked).closest('a.list-group-item').removeClass('selected-page');
    }
}

function isConfirm(title = 'Bạn có chắc muốn xóa?', icon = 'warning', buttons = ['Hủy', 'Đồng ý'], dangerMode = true) {
    return swal({
        title: `${title}`,
        icon: `${icon}`,
        buttons: buttons,
        dangerMode: dangerMode,
    });
}

function isConfirmInput(title = 'Bạn có chắc muốn xóa?', icon = 'warning', element, type, placeholder="", buttons = ['Hủy', 'Đồng ý'], dangerMode = true) {
    return swal(
      {
          title: `${title}`,
          icon: `${icon}`,
          content: {
              element: element,  // input html
              attributes: {
                  placeholder: placeholder,
                  type: type,  // password, text
              }
          },
          buttons: buttons,
          dangerMode: dangerMode
      }
    )
}

function isConfirmInputTextArea(title = 'Bạn có chắc muốn xóa?', icon = 'warning', element, placeholder="", buttons = ['Hủy', 'Đồng ý'], dangerMode = true) {
    return swal(
      {
          title: `${title}`,
          icon: `${icon}`,
          html: true,
          content: {
              element: element,  // textarea
              attributes: {
                  placeholder: placeholder,
              }
          },
          buttons: buttons,
          dangerMode: dangerMode
      }
    )
}


function showToastDefault(text, icon, heading='') {
    return $.toast({
        text: `${text}`,
        heading: heading,
        showHideTransition: 'fade',
        allowToastClose: true,
        icon: `${icon ? icon : 'success'}`,
        position: {
            top: 75,
            right: 5,
        },
        stack: false
    });
}

function showToast(text, icon, timeOut, heading) {
    return $.toast({
        heading: `${heading ? heading : ''}`,
        text: `${text}`,
        showHideTransition: 'fade',
        allowToastClose: true,
        hideAfter: `${timeOut ? timeOut : 3000}`,
        icon: `${icon ? icon : 'success'}`,
        position: {
            top: 75,
            right: 5,
        },
    });
}

function isVietnamPhoneNumber(number) {
    return /^(0|\+84)(\s|\.)?((3[2-9])|(5[689])|(7[06-9])|(8[1-689])|(9[0-46-9]))(\d)(\s|\.)?(\d{3})(\s|\.)?(\d{3})$/.test(number);
    // return /(03|05|07|08|09|01[2|6|8|9])+([0-9]{8})\b/.test(number);
}


function updateQueryStringParameter(uri, key, value) {
    let re = new RegExp('([?&])' + key + '=.*?(&|$)', 'i');
    let separator = uri.indexOf('?') !== -1 ? '&' : '?';
    if (uri.match(re)) {
        return uri.replace(re, '$1' + key + '=' + value + '$2');
    } else {
        return uri + separator + key + '=' + value;
    }
}

const getUrlParameter = function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

function removeParam(key, sourceURL) {
    let rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        if (params_arr.length) rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function smoothScrollingTo(target) {
    $('html,body').animate({
        scrollTop: $(target).offset().top
    }, 500);

    return false;
}

function handleAjaxErrors(xhr, ajaxOptions, thrownError) {
    hideLoading();
    if (xhr.status === 400) {
        showToast('Vui lòng tải lại trang để thực hiện lại thao tác!', 'info');
    } else if (xhr.status === 401) {
        showToast(thrownError, 'warning');
    } else if (xhr.status === 405) {
        showToast(thrownError, 'warning');
    } else if (xhr.status === 404) {
        showToast(thrownError, 'warning');
    } else if (xhr.status === 406) {
        showToast(thrownError, 'warning');
    } else {
        showToast(thrownError, 'error');
    }
    console.log('Error:', thrownError);
}

function resetSelect2ToDefaultValue(selectInput, value='') {
    $(selectInput).val(value).trigger('change');
}


function _debounce(func, wait) {
  //  Wrapper function for run another function in specified of time;
  let timeout;
  return function() {
    let context = this,
        args = arguments;
    let executeFunction = function() {
      func.apply(context, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(executeFunction, wait);
  };
}

function throttled(delay, fn) {
  let lastCall = 0;
  return function (...args) {
    const now = (new Date).getTime();
    if (now - lastCall < delay) {
      return;
    }
    lastCall = now;
    return fn(...args);
  }
}

function fadeOutRemoveItemInTable(domTarget) {
    domTarget.closest('tr').find('td').fadeOut('fast', function () {
        domTarget.closest('tr').remove();
    })
}


function addNewOptionToSelect2Input(formContainer, nameSelectInputAttr, value='', label='') {
    const newOption = "<option value='" + value + "'>" + label + "</option>";
    formContainer.find(`select[name="${nameSelectInputAttr}"] option:last`).after(newOption);
    // Trigger for select2 change selected value.
    formContainer.find(`select[name="${nameSelectInputAttr}"]`).val(value).trigger('change');
}


function commonSearchSelect(url, placeHolder, multiple=false, addNew = false, classNameSearch='select2-search', btnAdd='btn-add--item') {
    let dataResponse = null;
    $('.' + classNameSearch).select2({
        minimumInputLength: 2,
        multiple: multiple,
        width: '100%',
        placeholder: placeHolder,
        allowClear: true,
        ajax: {
            url: url,
            dataType: 'json',
            delay: 500,  // Delay time until user stop typing to perform action.
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
            cache: true,
            data: function (params) {
                return JSON.stringify({
                    'query_str': params.term,
                    page: params.page || 1,
                });
            },
            success: function(response) {
                dataResponse = response;
            },
            processResults: function () {
                if (dataResponse != null
                    && Object.keys(dataResponse).length
                    && dataResponse['status_code'] === 200)
                {
                    const results = [];
                    for (let i = 0; i < dataResponse['data'].length; i++) {
                        const item = dataResponse['data'][i];
                        results.push(
                            {
                                text: item.text,
                                id: item.id
                            }
                        )
                    }
                    return {
                        results: results,
                        pagination: {
                            more: (parseInt(dataResponse['page']) * parseInt(dataResponse['limit'])) < parseInt(dataResponse['total'])
                        }
                    }
                } else {
                    console.log('The data response', dataResponse);
                    return { results: [] };
                }
            },
            error: function (jqXHR, status, error) {
                console.log('Has error:', error + ": " + jqXHR.responseText);
                return { results: [] };
            },
        },
        escapeMarkup: function (markup) {
            return markup;
        },
        language: {
            loadingMore: function() {
                return `<span class="text-warning">Đang tải thêm ...</span>`
            },
            noResults: function () {
                return `<div class="text-center">
                                        <span class="text-danger"><i class="fas fa-exclamation"></i> Không tìm thấy dữ liệu</span>
                                        ${addNew ? `<hr> <button type="button" class="btn btn-info btn-sm ${btnAdd}"><span><i class="fas fa-plus"></i> Thêm mới</span></button>` : ''}
                                    </div>`;
            },
            inputTooShort: function () {
                return `<span class="text-info">Nhập ít nhất 2 ký tự</span>`;
            },
            searching: function () {
                return `<span class="text-danger">Đang tìm ...</span>`
            },
            errorLoading: function () {
                console.log('error server', dataResponse)
                return `<span class="text-danger">Dữ liệu không load được tại thời điểm hiện tại!</span>`
            }
        },
    });
}

function renderTinymce(classOrIdTextarea, height=600) {
    if (classOrIdTextarea) {
            tinymce.init({
            selector: classOrIdTextarea,
            relative_urls : false,
            height: height,
            remove_script_host : false,
            convert_urls : false,
            paste_data_images: true,
            plugins: [
                'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons'
            ],
            menubar: 'file edit view insert format tools table',
            toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media link anchor codesample | ltr rtl',
            toolbar_sticky: true,
            toolbar_mode: 'sliding',
            contextmenu: 'link image imagetools table',
            autosave_ask_before_unload: false,
            fontsize_formats: '6pt 7pt 8pt 9pt 10pt 11pt 12pt 13pt 14pt 15pt 16pt 18pt 20pt 22pt 24pt 26pt 28pt 32pt 36pt 40pt 44pt 48pt 54pt',
            image_advtab: true,
            setup: function (editor) {
                editor.on('change', function () {
                    tinymce.triggerSave();
                });
            },
            file_picker_callback: function(callback, value, meta) {
                if (meta.filetype == 'image') {
                    $('.upload-image').trigger('click');
                    $('.upload-image').on('change', function() {
                        var file = this.files[0];
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            callback(e.target.result, {
                            alt: ''
                            });
                        };
                    reader.readAsDataURL(file);
                    });
                }
            },
        });
    }
}

function resetAllInputModalShow(modalIdOrClass, hasSelect2=false, classSelect2='.select2-search') {
    $(document).on('show.bs.modal', modalIdOrClass, function() {
        const modalContent = $(this);
        // Reset all input forms and errors.
        hasSelect2 && resetSelect2ToDefaultValue(classSelect2);
        modalContent.find('form input, select, textarea').val('');
        if (modalContent.find('ul.text-danger').length > 0) {
            modalContent.find('ul.text-danger').remove();
        }
    })
}

function handleFormErrors(formObject, data) {
    if (data['errors'] && Object.keys(data['errors']).length > 0) {
        for (let field_error of Object.keys(data['errors'])) {
            const li = data['errors'][field_error].map(itemError =>
                `<li><small>${itemError}</small></li>`
            ).join(' ');
            formObject.find(`#${field_error}`).after(
                `<ul class="navbar-nav text-danger">
                    ${li}
                </ul>`
            )
        }
    } else {
        showToast(data['msg'], 'error');
    }
}


function handleClientFormErrors(formObject, data) {
    if (data['errors'] && Object.keys(data['errors']).length > 0) {
        for (let field_error of Object.keys(data['errors'])) {
            const li = data['errors'][field_error].map(itemError =>
                `<li><small>${itemError}</small></li>`
            ).join(' ');
            formObject.find(`#${field_error}`).after(
                `<ul class="navbar-nav text-danger">
                    ${li}
                </ul>`
            )
        }
    } else {
        showToastDefault(data['msg'], 'error');
    }
}

function performAjaxSubmitFormWithFile(formObject, url, formData, func) {
    showLoading();
    try {
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                hideLoading();
                formObject.find('ul.text-danger').remove();
                if (data['status_code'] === 200) {
                    if (typeof func === 'function') {
                        func(data);
                    } else {
                        window.location.reload();
                    }
                } else {
                    handleFormErrors(formObject, data);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                handleAjaxErrors(xhr, ajaxOptions, thrownError);
            }
        })
    } catch (err) {
        hideLoading();
        showToast(err, 'error');
    }
}

function performAjaxSubmitJson(url, data={}, func, showHideLoading=false) {
    showHideLoading && showLoading();
    try {
        $.ajax({
            url: url,
            dataType: 'JSON',
            method: 'POST',
            contentType: "application/json",
            data: JSON.stringify({
                ...data,
            }),
            success: function (data) {
                showHideLoading && hideLoading();
                if (data['status_code'] !== 200) {
                    showToast(data['msg'], 'error');
                    data['error'] && console.log('Has error', data['error']);
                } else {
                    if (typeof func === 'function') {
                        func(data);
                    } else {
                        window.location.reload();
                    }
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                handleAjaxErrors(xhr, ajaxOptions, thrownError);
            }
        })
    } catch (err) {
        showHideLoading && hideLoading();
        showToast(err, 'error');
    }
}


function performAjaxSubmitFormOnModal(formObject, url, func) {
    showLoading();
    try {
        $.ajax({
            type: 'POST',
            url: url,
            data: formObject.serialize(),
            success: function (data) {
                hideLoading();
                formObject.find('ul.text-danger').remove();
                if (data['status_code'] === 200) {
                    if (typeof func === 'function') {
                        func(data);
                    } else {
                        window.location.reload();
                    }
                } else {
                    handleFormErrors(formObject, data);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                handleAjaxErrors(xhr, ajaxOptions, thrownError);
            }
        })
    } catch (err) {
        hideLoading();
        showToast(err, 'error');
    }
}

function renderSummernote(idOrClassSelector, height=250) {
    $(idOrClassSelector).summernote({
        dialogsInBody: true,
        minHeight: height,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'hr']],
            ['help', ['help']]
        ],
    });
}

function resetDefaultOption(targetSelectId) {
    let null_option = "<option value=''>Chọn</option>";
    $(`#${targetSelectId} option`).remove();
    $(`#${targetSelectId}`).append(null_option);
}

function renderOptions(resp, targetID) {
    resetDefaultOption(targetID);
    $.each(resp['data'], function (i, item) {
        let new_option = "<option value='" + item.id + "'>" + item.value + "</option>";
        $(`#${targetID}`).append(new_option);
    });
}

function commonPopulate(ajxUrl, data = {},callback){
    performAjaxSubmitJson(ajxUrl, data, (resp) => {
        callback(resp);
    });
}