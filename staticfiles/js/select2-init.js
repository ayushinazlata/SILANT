$(document).ready(function() {
    $('select').select2({
      placeholder: "Выберите...",
      allowClear: true,
      width: 'style',
      dropdownPosition: 'below',
      language: {
        noResults: function () {
          return "Ничего не найдено";
        },
        searching: function () {
          return "Поиск...";
        }
      }
    });
  });
  