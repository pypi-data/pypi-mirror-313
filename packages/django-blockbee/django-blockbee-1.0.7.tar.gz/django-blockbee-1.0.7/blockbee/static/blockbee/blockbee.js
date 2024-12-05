function truncate(text, startChars, endChars, maxLength) {
    if (text.length > maxLength) {
        var start = text.substring(0, startChars);
        var end = text.substring(text.length - endChars, text.length);
        return start + '...' + end;
    }
    return text;
}

function check_status(id) {
    let is_paid = false;

    function status_loop() {
        if (is_paid) return;

        $.getJSON(window.location.protocol + "//" + window.location.host + '/blockbee/status/?request_id=' + id, function (data) {

            let waiting_payment = jQuery('.waiting_payment');
            let waiting_network = jQuery('.waiting_network');
            let payment_done = jQuery('.payment_done');

            jQuery('.blockbee_value').html(data.remaining);
            jQuery('.blockbee_fiat_total').html(data.fiat_remaining);
            jQuery('.blockbee_copy.blockbee_details_copy').attr('data-tocopy', data.remaining);

            if (data.data.is_pending === 1) {
                waiting_payment.addClass('done');
                waiting_network.addClass('done');
                jQuery('.blockbee_loader').remove();
                jQuery('.blockbee_payment_notification').remove();

                setTimeout(function () {
                    jQuery('.blockbee_payments_wrapper').slideUp('200');
                    jQuery('.blockbee_payment_processing').slideDown('200');
                }, 300);
            }

            if (data.data.is_paid === 1) {
                waiting_payment.addClass('done');
                waiting_network.addClass('done');
                payment_done.addClass('done');
                jQuery('.blockbee_loader').remove();
                jQuery('.blockbee_payment_notification').remove();

                setTimeout(function () {
                    jQuery('.blockbee_payments_wrapper').slideUp('200');
                    jQuery('.blockbee_payment_processing').slideUp('200');
                    jQuery('.blockbee_payment_confirmed').slideDown('200');
                }, 300);

                is_paid = true;
            }

            if (data.data.show_min_fee === 1) {
                jQuery('.blockbee_notification_remaining').show();
            } else {
                jQuery('.blockbee_notification_remaining').hide();
            }

            if (data.data.remaining !== data.crypto_total) {
                jQuery('.blockbee_notification_payment_received').show();
                jQuery('.blockbee_notification_cancel').remove();
                jQuery('.blockbee_notification_ammount').html(data.already_paid + ' ' + data.coin + ' (<strong>' + data.already_paid_fiat + ' ' + data.fiat_symbol + '<strong>)');
            }

            if (data.payments) {
                let history = data.payments;

                if (jQuery('.blockbee_history_fill tr').length < Object.entries(history).length + 1) {
                    jQuery('.blockbee_history').show();

                    jQuery('.blockbee_history_fill td:not(.blockbee_history_header)').remove();

                    Object.entries(history).forEach(([key, value]) => {
                        let time = new Date(value.timestamp * 1000).toLocaleTimeString(document.documentElement.lang);
                        let date = new Date(value.timestamp * 1000).toLocaleDateString(document.documentElement.lang);

                        jQuery('.blockbee_history_fill').append(
                            '<tr>' +
                            '<td>' + value.timestamp + '</td>' +
                            '<td>' + value.value_coin + '</td>' +
                            '</tr>'
                        )
                    });
                }
            }

            if (jQuery('.blockbee_time_refresh')[0]) {
                var timer = jQuery('.blockbee_time_seconds_count');

                if (timer.attr('data-seconds') <= 0) {
                    timer.attr('data-seconds', data.counter);
                }
            }
        });

        setTimeout(status_loop, 2000);
    }

    status_loop();
}


function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        return clipboardData.setData("Text", text);

    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

$(function () {
    $('.blockbee_show_qr').on('click', function (e) {
        e.preventDefault();

        let qr_code_close_text = $('.blockbee_show_qr_close');
        let qr_code_open_text = $('.blockbee_show_qr_open');

        if ($(this).hasClass('active')) {
            $('.blockbee_qrcode_wrapper').slideToggle(500);
            $(this).removeClass('active');
            qr_code_close_text.addClass('active');
            qr_code_open_text.removeClass('active');

        } else {
            $('.blockbee_qrcode_wrapper').slideToggle(500);
            $(this).addClass('active');
            qr_code_close_text.removeClass('active');
            qr_code_open_text.addClass('active');
        }
    });

    $('.blockbee_copy').on('click', function () {
        copyToClipboard($(this).attr('data-tocopy'));
        let tip = $(this).find('.blockbee_tooltip.tip');
        let success = $(this).find('.blockbee_tooltip.success');

        success.show();
        tip.hide();

        setTimeout(function () {
            success.hide();
            tip.show();
        }, 5000);
    })
})
