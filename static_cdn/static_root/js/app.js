$(document).ready(function () {
    var step = 0;
    battery = 0
    wheel = 0
    tire = 0

    $('#wheelsForm').hide();
    $('#tiresForm').hide();
    $('#checkout').hide();

    $('.go_step_1').click(function () {
        battery = $(this).data('id');
        $('#wheelsForm').show();
        $('#tiresForm').hide();
        $('#batteriesForm').hide();
        $('#checkout').hide();

        step += 1
        content_wheelsForm = ""

        $.ajax({
            url: "/check_available_wheel_for_battery/" + battery,
            type: 'get',
            async: true,
            dataType: 'json',
            success: function (data) {
                // debugger;
                for (var x = 0; x < data.length; x++) {
                    console.log(data[x])
                    content_wheelsForm += "<div class='col-sm-4'>"
                    content_wheelsForm += "<div class='card'>"
                    content_wheelsForm += "<div class='card-header'>"
                    content_wheelsForm += data[x].name
                    content_wheelsForm += "</div>"
                    content_wheelsForm += "<div class='card-body'>"
                    content_wheelsForm += "<div class='card-text'>"
                    content_wheelsForm += data[x].title
                    content_wheelsForm += "</div>"
                    content_wheelsForm += "</div>"
                    content_wheelsForm += "<input type=\"button\" class=\"go_step_2 btn btn-primary\" data-id='" + data[x].id + "' value=\"Select\">"
                    content_wheelsForm += "</div>"
                    content_wheelsForm += "</div>"
                }
                $('#wheelsForm').prepend($(content_wheelsForm));
                $('input.go_step_2').each((i, elm) => {
                    $(elm).on("click", (e) => {
                        go_to_step_2($(elm))
                    })
                })
            },
            error: function (data) {
                alert(data.responseJSON.error); // the message
            }
        });
    });

    function go_to_step_2(el) {
        wheel = $(el).data('id')
        console.log(wheel)
        $('#tiresForm').show();
        $('#wheelsForm').hide();
        $('#batteriesForm').hide();
        $('#checkout').hide();

        step += 1
        content_tiresForm = ""

        $.ajax({
            url: '/check_available_tire_for_wheel/' + wheel,
            type: 'get',
            async: true,
            dataType: 'json',
            success: function (data) {
                // debugger;
                for (var x = 0; x < data.length; x++) {
                    console.log(data[x])
                    content_tiresForm += "<div class='col-sm-4'>"
                    content_tiresForm += "<div class='card'>"
                    content_tiresForm += "<div class='card-header'>"
                    content_tiresForm += data[x].name
                    content_tiresForm += "</div>"
                    content_tiresForm += "<div class='card-body'>"
                    content_tiresForm += "<div class='card-text'>"
                    content_tiresForm += data[x].title
                    content_tiresForm += "</div>"
                    content_tiresForm += "</div>"
                    content_tiresForm += "<input type=\"button\" class=\"go_step_3 btn btn-primary\" data-id='" + data[x].id + "' value=\"Select\">"
                    content_tiresForm += "</div>"
                    content_tiresForm += "</div>"
                }
                $('#tiresForm').prepend($(content_tiresForm));
                $('input.go_step_3').each((i, elm) => {
                    $(elm).on("click", (e) => {
                        go_to_step_3($(elm))
                    })
                })
            }
        });
    }

    function go_to_step_3(el) {
        tire = $(el).data('id')
        $('#tiresForm').hide();
        $('#wheelsForm').hide();
        $('#batteriesForm').hide();
        $('#checkout').show();

        $('#battery_id').val(battery)
        $('#wheel_id').val(wheel)
        $('#tire_id').val(tire)

        step += 1
        content_tiresForm = ""

        $.ajax({
            url: '/checkout/' + battery + '/' + wheel + '/' + tire,
            type: 'get',
            async: true,
            dataType: 'json',
            success: function (data) {
                // debugger;
                console.log(data)
                for (var x = 0; x < data.length; x++) {
                    console.log(data[x])
                    $('#basePrice').text(data[x].base_amount)
                    $('#batteryNumber').text(data[x].battery_amount)
                    $('#wheelNumber').text(data[x].wheel_amount)
                    $('#tierNumber').text(data[x].tire_amount)
                    $('#discountNumber').text(data[x].discount)
                    $('#totalAmount').text(data[x].total_amount)

                    $('#basePrice_').text(data[x].base_amount)
                    $('#batteryNumber_').text(data[x].battery_amount)
                    $('#wheelNumber_').text(data[x].wheel_amount)
                    $('#tierNumber_').text(data[x].tire_amount)
                    $('#discountNumber_').text(data[x].discount)
                    $('#totalAmount_').text(data[x].total_amount)
                }
            }
        });
    }
});
