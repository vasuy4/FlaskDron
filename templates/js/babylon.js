document.addEventListener("DOMContentLoaded", function () {
  // Ваш код инициализации Babylon.js
  const canvas = document.getElementById("renderCanvas");

  const basicScene = new BasicScene(canvas);

  basicScene.engine.runRenderLoop(function () {
    basicScene.scene.render();
  });

  window.addEventListener("resize", function () {
    basicScene.engine.resize();
  });
});

class BasicScene {
  constructor(canvas) {
    this.engine = new BABYLON.Engine(canvas, true);
    this.scene = this.createScene();
    this.canvas = canvas;
  }

  createScene() {
    const scene = new BABYLON.Scene(this.engine);
    scene.clearColor = new BABYLON.Color3(0.12, 0.21, 0.41);
    const camera = new BABYLON.ArcRotateCamera(
      "camera1",
      Math.PI / 5,
      Math.PI / 3,
      15,
      BABYLON.Vector3.Zero(),
      scene
    );
    camera.attachControl(this.canvas, true);
    camera.radius = 100;
    const light = new BABYLON.HemisphericLight(
      "light1",
      new BABYLON.Vector3(1, 1, 0),
      scene
    );

    this.createOtherComponents();

    return scene;
  }

  createOtherComponents() {
    this.createGroundGrids();
    this.createModel();
  }

  createGroundGrids() {
    const ground = BABYLON.MeshBuilder.CreateGround("ground", {
      width: 350,
      height: 350,
    });

    // Создание материала для земли
    const groundMaterial = new BABYLON.StandardMaterial(
      "groundMaterial",
      this.scene
    );
    groundMaterial.diffuseColor = new BABYLON.Color3(0, 0.5, 0.8); // Зеленый цвет
    ground.material = groundMaterial;
    ground.material.alpha = 0.2;

    // Создание сетки
    this.createGrid(this.scene, 25, 50, "Z");
    this.createGrid(this.scene, 15, 30, "X", [0.1, 0.1, 0.3], 0.1);
  }

  createModel() {
    // Загрузка модели
    BABYLON.SceneLoader.ImportMesh(
      "",
      "models/",
      "model.gltf",
      this.scene,
      function (meshes) {
        // Модель загружена, можно выполнить дополнительные действия
        console.log("Model loaded:", meshes);

        // Масштабирование модели
        meshes.forEach((mesh) => {
          mesh.scaling.scaleInPlace(0.3); // Уменьшение размера модели в 2 раза
          mesh.rotate(BABYLON.Axis.X, -Math.PI / 4, BABYLON.Space.WORLD);
          mesh.position.z = 15;
        });

        // Сохранение модели для последующего использования
        this.scene.modelMeshes = meshes;
      }
    );
  }

  createGrid(
    scene,
    gridSize,
    gridSpacing,
    rotate = "Z",
    color = [0.5, 0.5, 0.5],
    alpha = 1
  ) {
    // Создаем массив точек для линий
    const points = [];

    // Добавляем точки для вертикальных линий
    for (let i = -gridSize; i <= gridSize; i += gridSpacing) {
      points.push(new BABYLON.Vector3(i, 0, -gridSize));
      points.push(new BABYLON.Vector3(i, 0, gridSize));
    }

    // Добавляем точки для горизонтальных линий
    for (let i = -gridSize; i <= gridSize; i += gridSpacing) {
      points.push(new BABYLON.Vector3(-gridSize, 0, i));
      points.push(new BABYLON.Vector3(gridSize, 0, i));
    }

    // Создаем LinesMesh из точек
    const grid = BABYLON.MeshBuilder.CreateLines(
      "grid",
      { points: points },
      scene
    );
    grid.color = new BABYLON.Color3(...color); // Цвет линий
    if (rotate == "Z")
      grid.rotate(BABYLON.Axis.Z, -Math.PI / 2, BABYLON.Space.WORLD);
    else if (rotate == "X")
      grid.rotate(BABYLON.Axis.X, -Math.PI / 2, BABYLON.Space.WORLD);
    else if (rotate == "Y")
      grid.rotate(BABYLON.Axis.Y, -Math.PI / 2, BABYLON.Space.WORLD);
    grid.alpha = alpha;
  }
}
