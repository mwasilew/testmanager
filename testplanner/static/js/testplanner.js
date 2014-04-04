function add_definition(step_number) {
    total_forms = $('#id_testplantestdefinition_set-TOTAL_FORMS').val();
    // update form count
    $('#id_testplantestdefinition_set-TOTAL_FORMS').attr('value', total_forms+1);
});
