$(document).ready(function () {
    let isProgrammingChange = false;  // Флаг для отслеживания программного изменения
  function updateSlider(sliderId, sliderValueId, value) {
    isProgrammingChange = true;
    $("#" + sliderId)
      .val(value)
      .trigger("input");
    $("#" + sliderValueId).text(value);
    isProgrammingChange = false;
  }

  $("#slider_servo").on("input", function () {
    if (isProgrammingChange) return;

    var sliderValue = $(this).val();
    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ slider_servo: sliderValue }),
      success: function (response) {
        $("#slider_value_servo").text(response.slider_value_servo);
      },
    });
  });

  $("#slider_engine_left").on("input", function () {
    if (isProgrammingChange) return;

    var sliderValue = $(this).val();
    var sliderValueRight = $("#slider_engine_right").val();
    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        slider_engine_left: sliderValue,
        slider_engine_right_secondary: sliderValueRight,
      }),
      success: function (response) {
        $("#slider_value_engine_left").text(response.slider_value_engine_left);
        updateSlider(
          "slider_speed",
          "slider_value_speed",
          response.slider_value_speed
        );
        updateSlider(
          "slider_direction",
          "slider_value_direction",
          response.slider_value_direction
        );
      },
    });
  });

  $("#slider_engine_right").on("input", function () {
    if (isProgrammingChange) return;

    var sliderValue = $(this).val();
    var sliderValueLeft = $("#slider_engine_left").val();

    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        slider_engine_right: sliderValue,
        slider_engine_left_secondary: sliderValueLeft,
      }),
      success: function (response) {
        $("#slider_value_engine_right").text(
          response.slider_value_engine_right
        );
        updateSlider(
          "slider_speed",
          "slider_value_speed",
          response.slider_value_speed
        );
        updateSlider(
          "slider_direction",
          "slider_value_direction",
          response.slider_value_direction
        );
      },
    });
  });

  $("#slider_speed").on("input", function () {
    if (isProgrammingChange) return;

    var sliderValue = $(this).val();
    var sliderValueDirection = $("#slider_direction").val();

    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        slider_speed: sliderValue,
        slider_direction_secondary: sliderValueDirection,
      }),
      success: function (response) {
        $("#slider_value_speed").text(response.slider_value_speed);
        updateSlider(
          "slider_engine_left",
          "slider_value_engine_left",
          response.slider_value_engine_left
        );
        updateSlider(
          "slider_engine_right",
          "slider_value_engine_right",
          response.slider_value_engine_right
        );
        updateSlider(
            "slider_direction",
            "slider_value_direction",
            response.slider_value_direction
        );
      },
    });
  });

  $("#slider_direction").on("input", function () {
    if (isProgrammingChange) return;

    var sliderValue = $(this).val();
    var sliderValueSpeed = $("#slider_speed").val();

    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        slider_direction: sliderValue,
        slider_speed_secondary: sliderValueSpeed,
      }),
      success: function (response) {
        $("#slider_value_direction").text(response.slider_value_direction);
        updateSlider(
            "slider_engine_left",
            "slider_value_engine_left",
            response.slider_value_engine_left
          );
        updateSlider(
            "slider_engine_right",
            "slider_value_engine_right",
            response.slider_value_engine_right
        );
        updateSlider(
            "slider_speed",
            "slider_value_speed",
            response.slider_value_speed
        );
      },
    });
  });
});
