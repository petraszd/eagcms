window.addEvent('domready', function () {
    var mooEditableOptions = {
        'actions': 'bold italic underline strikethrough | '
            + 'insertunorderedlist insertorderedlist indent outdent | '
            + 'undo redo | createlink unlink | urlimage | forecolor | '
            + 'toggleview | formatBlock justifyleft justifyright '
            + 'justifycenter justifyfull | '
            + 'tableadd tableedit tablerowadd tablerowedit tablerowspan '
            + 'tablerowsplit tablerowdelete tablecoladd tablecoledit '
            + 'tablecolspan tablecolsplit tablecoldelete ',
        'externalCSS': MEDIA_URL + 'eag-static/css/MooEditable/Editable.css'
    };

    function newMooWYSIWYG(textarea) {
        var mooEdit = new MooEditable(textarea, mooEditableOptions);
        new PicasaChoiceField(mooEdit.dialogs.urlimage.prompt.el.getElement('input'));
    };

    $('ContentInfo').getElements('textarea.semi-wysiwyg').each(function (textarea) {
        var button = new Element('a', {'text': 'to wysiwyg', 'class': 'to-wysiwyg'})
            .inject(textarea, 'after')
            .addEvent('click', function (e) {
                e.preventDefault();
                this.dispose();
                newMooWYSIWYG(textarea);
                textarea.focus();
            });
    });

    $('ContentInfo').getElements('textarea.wysiwyg').each(function (textarea) {
        newMooWYSIWYG(textarea);
    });

    makePicasaChoiceFields('input.picasa');
});

