(function($) {
    $(document).ready(function(){
        console.log("Load")
        if ($('#id_question_type').val() == 'SE'){
            console.log("If")
            $("#related_question_choices-group").show();
        } 
        else {
            console.log("else")
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