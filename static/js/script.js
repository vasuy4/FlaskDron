import BasicScene from "./babylon.js";
import $ from 'jquery';

$(document).ready(function () {
  let isProgrammingChange = false;  // Флаг для отслеживания программного изменения

  // Загрузка сцены с дроном из BabylonJS
  const canvas = document.getElementById("renderCanvas");
  const basicScene = new BasicScene(canvas);
  basicScene.engine.runRenderLoop(function () {
    basicScene.scene.render();
  });
  window.addEventListener("resize", function () {
    basicScene.engine.resize();
  });

  let oldValueServo = 0;
  let oldValueDirection = 0;
  function toRadians(degr) {
    return degr * Math.PI / 180;
  }

  function updateSlider(sliderId, sliderValueId, value) {
    isProgrammingChange = true;
    $("#" + sliderId)
      .val(value)
      .trigger("input");
    $("#" + sliderValueId).text(value);
    isProgrammingChange = false;
  }


  function updateSensorData() {
    $.ajax({
      url: "/get_sensor_data",
      type: "POST",
      success: function (response) {
        $("#temperature").text(response.temperature);
        $("#pressure").text(response.pressure);
        $("#depth").text(response.depth);
      },
    });
  }
  setInterval(updateSensorData, 2000);


  $("#slider_servo").on("input", function () {
    if (isProgrammingChange) return;
    var sliderValue = $(this).val();

    let mesh;
    if (basicScene.scene.modelMeshes) {
      basicScene.scene.modelMeshes.forEach(meshh => {
          mesh = meshh;
      });
    } else mesh = null;
    if (mesh) {
      mesh.rotate(BABYLON.Axis.X, toRadians(sliderValue - oldValueServo)/2, BABYLON.Space.WORLD);
    } else {
      console.log("Not loaded");
    }
    oldValueServo = sliderValue;
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
        anchor_value: "slider_engine_left",
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
        anchor_value: "slider_engine_right",
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
        anchor_value: "slider_speed",
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
    var sliderValue = $(this).val();
    var sliderValueSpeed = $("#slider_speed").val();

    let mesh;
    if (basicScene.scene.modelMeshes) {
      basicScene.scene.modelMeshes.forEach(meshh => {
          mesh = meshh;
      });
    } else mesh = null;
    if (mesh) {
      mesh.rotate(BABYLON.Axis.Y, toRadians(sliderValue - oldValueDirection)/2, BABYLON.Space.WORLD);
    } else {
      console.log("Not loaded");
    }
    oldValueDirection = sliderValue;

    if (isProgrammingChange) return;
    $.ajax({
      url: "/update_slider",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        slider_direction: sliderValue,
        slider_speed_secondary: sliderValueSpeed,
        anchor_value: "slider_direction",
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