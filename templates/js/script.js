$(document).ready(function () {
  function updateSlider(sliderId, sliderValueId, value) {
    $("#" + sliderId)
      .val(value)
      .trigger("input");
    $("#" + sliderValueId).text(value);
  }

  $("#slider_servo").on("input", function () {
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
});
