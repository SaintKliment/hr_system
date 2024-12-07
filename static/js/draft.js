let activityCount = 1;

// Загрузка данных из localStorage
window.onload = function () {
  if (localStorage.getItem("module_name")) {
    document.getElementById("module_name").value =
      localStorage.getItem("module_name");
  }
  if (localStorage.getItem("positions")) {
    document.getElementById("positions").value =
      localStorage.getItem("positions");
  }
  if (localStorage.getItem("data_source")) {
    document.getElementById("data_source").value =
      localStorage.getItem("data_source");
  }
  if (localStorage.getItem("duration")) {
    document.getElementById("duration").value =
      localStorage.getItem("duration");
  }
  if (localStorage.getItem("responsible")) {
    document.getElementById("responsible").value =
      localStorage.getItem("responsible");
  }

  // Восстановление мероприятий
  if (localStorage.getItem("activities")) {
    const activities = JSON.parse(localStorage.getItem("activities"));
    activities.forEach((activity, index) => {
      if (index > 0) {
        addActivity();
      }
      document.getElementById(`activity_name_${index + 1}`).value =
        activity.name;
      document.getElementById(`activity_type_${index + 1}`).value =
        activity.type;
      document.getElementById(`activity_content_${index + 1}`).value =
        activity.content;
    });
  }
};

// Сохранение данных в localStorage
function saveData() {
  localStorage.setItem(
    "module_name",
    document.getElementById("module_name").value
  );
  localStorage.setItem("positions", document.getElementById("positions").value);
  localStorage.setItem(
    "data_source",
    document.getElementById("data_source").value
  );
  localStorage.setItem("duration", document.getElementById("duration").value);
  localStorage.setItem(
    "responsible",
    document.getElementById("responsible").value
  );

  let activities = [];
  for (let i = 1; i <= activityCount; i++) {
    if (document.getElementById(`activity_name_${i}`)) {
      activities.push({
        name: document.getElementById(`activity_name_${i}`).value,
        type: document.getElementById(`activity_type_${i}`).value,
        content: document.getElementById(`activity_content_${i}`).value,
      });
    }
  }
  localStorage.setItem("activities", JSON.stringify(activities));
}

// Добавление мероприятия
function addActivity() {
  activityCount++;
  const activitiesDiv = document.getElementById("activities");
  const newActivity = document.createElement("div");
  newActivity.classList.add("activity");
  newActivity.setAttribute("id", "activity_" + activityCount);

  newActivity.innerHTML = `
    <label for="activity_name_${activityCount}">Наименование мероприятия:</label>
    <input type="text" id="activity_name_${activityCount}" name="activity_name[]" required />
    <label for="activity_type_${activityCount}">Тип мероприятия:</label>
    <select name="activity_type[]" id="activity_type_${activityCount}" required>
      <option value="theory">Теория</option>
      <option value="practice">Практика</option>
    </select>
    <label for="activity_content_${activityCount}">Содержание мероприятия:</label>
    <textarea name="activity_content[]" id="activity_content_${activityCount}" rows="4" required></textarea>
  `;

  activitiesDiv.appendChild(newActivity);
}

// Удаление мероприятия
function removeActivity() {
  if (activityCount > 1) {
    const activityDiv = document.getElementById("activity_" + activityCount);
    activityDiv.remove();
    activityCount--;
  }
}

// Сохранение данных на каждом изменении
document.getElementById("moduleForm").addEventListener("input", saveData);

let fileInputCount = 1;

document
  .getElementById("add-file-input")
  .addEventListener("click", function () {
    fileInputCount++;
    const container = document.getElementById("file-inputs-container");

    // Создаем новый инпут для файла
    const newInputDiv = document.createElement("div");
    newInputDiv.classList.add("file-input");
    newInputDiv.setAttribute("id", `file_input_${fileInputCount}`);

    newInputDiv.innerHTML = `
<input
type="file"
id="materials_${fileInputCount}"
name="materials[]"
accept=".pdf,.pptx,.xlsx,.docx,.jpg,.mkv,.avi,.mp,.url"
/>
`;

    container.appendChild(newInputDiv);
  });
document
  .getElementById("file-inputs-container")
  .addEventListener("change", function () {
    let files = [];
    for (let i = 1; i <= fileInputCount; i++) {
      const input = document.getElementById(`materials_${i}`);
      if (input && input.files.length > 0) {
        files.push(input.files[0].name);
      }
    }
    localStorage.setItem("uploaded_files", JSON.stringify(files));
  });
