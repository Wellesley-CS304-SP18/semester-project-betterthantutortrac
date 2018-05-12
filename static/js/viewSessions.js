$(document).ready(function() {
  $("#sessions-table").DataTable();

  $("button").click(function() {
    alert($(this).val());         
    console.log($(this).val());
  });
});
