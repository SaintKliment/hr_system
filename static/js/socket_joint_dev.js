const socket = io();

// Функция отправки сообщения в режиме реального времени
// function sendMessage() {
//   const msg = document.getElementById("module_name").value;
//   socket.emit("typing", msg); // Отправляем сообщение на сервер
// }

// socket.on("module_name", function (msg) {
//   console.log(msg); // Обновляем вывод в реальном времени
// });

function sendMessage() {
  const moduleName = document.getElementById("module_name").value;
  const moduleId = 1; // Замените на актуальный ID модуля
  socket.emit("update_module", {
    module_id: moduleId,
    module_name: moduleName,
  });
}

socket.on("module_name", function (data) {
  if (data.module_id === 1) {
    // Убедитесь, что обновление относится к нужному модулю
    document.getElementById("module_name").value = data.module_name;
  }
});
