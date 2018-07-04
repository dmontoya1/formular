(function($) {
    $(document).ready(function(){
        if ($('#id_question_type').val() == 'SE'){
            $("#related_question_choices-group").show();
        } 
        else {
            $("#related_question_choices-group").hide();
        }

        $('#id_question_type').change(function(){
            if($(this).val() == 'SE'){
                $("#related_question_choices-group").show();
            }
            else{
                $("#related_question_choices-group").hide();
            }
        })
    });
})(django.jQuery);