const socket = io();

function sendMessage() {
  const moduleName = document.getElementById("module_name").value || null;
  const dataSource = document.getElementById("data_source").value || null;
  const duration = document.getElementById("duration").value || null;
  const responsible = document.getElementById("responsible").value || null;

  const path = window.location.pathname;
  const segments = path.split("/");
  const moduleId = segments.pop() || segments.pop();

  //   console.log("Отправляем данные:", {
  //     module_id: moduleId,
  //     module_name: moduleName,
  //     data_source: dataSource,
  //   }); // Лог для проверки

  socket.emit("update_module", {
    module_id: moduleId,
    module_name: moduleName,
    data_source: dataSource,
    duration: duration,
    responsible: responsible,
  });
}

socket.on("module_name", function (data) {
  document.getElementById("module_name").value = data.module_name;
  document.getElementById("data_source").value = data.data_source;
  document.getElementById("duration").value = data.duration;
  document.getElementById("responsible").value = data.responsible;
});
