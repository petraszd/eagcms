window.addEvent('domready', function () {
    function slugify(str) {
        return str.toLowerCase().trim()
            .replace(/\s+/g, '-')
            .replace(/[^a-z0-9\-_]/g, '');
    };

    function toSlug () {
        $('id_slug').set('value', slugify(this.get('value')));
    };

    if ($('id_slug').get('value') == slugify($('id_title').get('value'))) {
        $('id_title').addEvent('keyup', toSlug);
    }

    $('id_slug').addEvent('change', function () {
        $('id_title').removeEvent('keyup', toSlug);
        this.set('value', slugify(this.get('value')));
    });
});
