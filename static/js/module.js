$(document).ready(function() {
    function fetchModules() {
        const showArchived = $('#archiveCheckbox').is(':checked');
        const nameQuery = $('#nameInput').val(); // Поле ввода имени модуля
        const statusQuery = $('#statusSelect').val(); // Селектор статуса модуля

        $.get('/view_modules', { 
            archived: showArchived,
            name: nameQuery,
            status: statusQuery 
        }, function(data) {
            $('#moduleList').empty();
            data.forEach(function(module) {
                $('#moduleList').append('<li>' + module.name + ' (' + module.status + ')</li>');
            });
        });
    }

    $('#archiveCheckbox').change(fetchModules);
    $('#nameInput').on('input', fetchModules); // Обновляем при вводе имени
    $('#statusSelect').change(fetchModules); // Обновляем при изменении статуса
    fetchModules(); // начальный вызов для загрузки данных
});
