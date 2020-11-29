var PicasaUrl = {
    noGalleries: 'No Picasa galleries found. Go to <a href="http://picasaweb.google.com/%user%">Picasa Web</a> and add one.',
    galleries: 'http://picasaweb.google.com/data/feed/api/user/%user%',
    gallery: 'http://picasaweb.google.com/data/feed/api/user/%user%/albumid/%albumid%',
    genGalleryUrl: function (id) {
        return this.gallery.replace('%albumid%', id);
    }
};

function makePicasaChoiceFields(input) {
    if ($(input)) {
        var inputs = [$(input)];
    } else {
        var inputs = $$(input);
    }

    inputs.each(function (input) {
        new PicasaChoiceField(input);
    });
};

var PicasaChoiceField = new Class({
    Implements: Options,
    options: {
        css: {
            trigger: 'picasa-trigger',
            back: 'picasa-back',
            wait: 'picasa-wait',
            gallery: 'gallery-holder',
            image: 'image-holder',
            window: 'picasa-window'
        }
    },

    initialize: function (input, options) {
        this.setOptions(options);

        this._input = input;
        this._trigger = new Element('a', {
            'class': this.options.css.trigger, 'text': 'from picasa'
        });
        this._trigger.inject(this._input, 'after');

        this._trigger.addEvent('click', this.open.bind(this));

        this._back = new Element('div', {'class': this.options.css.back, 'opacity': 0.5});
        this._window = new Element('div', {'class': this.options.css.window});

        this._back.addEvent('click', this.close.bind(this));
        window.document.addEvent('keydown', function (e) {
            if (e.key == 'esc') {
                this.close();
            }
        }.bind(this));
    },

    clear: function () {
        this._back.empty();
        this._window.empty();
    },

    close: function () {
        this._back.dispose();
        this._window.dispose();
    },

    wait: function () {
        this.clear();
        new Element('div', {'class': this.options.css.wait}).inject(this._window);
    },

    open: function() {
        this._back.inject(document.body);
        this._window.inject(document.body);
        this.getGalleries();
    },

    getGalleries: function () {
        this.wait();
        new Request.JSON({
            url: PicasaUrl.galleries,
            method: 'get',
            onSuccess: this.proccessGalleries.bind(this),
            onFailure: function () { }
        }).send();
    },

    proccessGalleries: function (json) {
        this.clear();
        var galleries = json.feed.entry;
        if (!galleries) {
            new Element('p', {'html': PicasaUrl.noGalleries}).inject(this._window);
            return;
        }
        galleries.each(function (item) {
            var wrapper = new Element('div', {
                'class': this.options.css.gallery});
            var numPhotos = item.gphoto$numphotos.$t;
            var title = item.gphoto$name.$t + ' (' + numPhotos + ')';
            var galId = item.gphoto$id.$t;
            var src = item.media$group.media$thumbnail[0].url;
            new Element('h2', {'text': title}).inject(wrapper);
            var img = new Element('img', {'alt': galId, 'src': src});
            img.inject(wrapper);
            wrapper.addEvent('click', function (e) {
                this.getGallery(galId);
            }.bind(this));
            wrapper.inject(this._window);
        }.bind(this));
    },

    getGallery: function (galId) {
        this.wait();
        new Request.JSON({
            url: PicasaUrl.genGalleryUrl(galId),
            method: 'get',
            onSuccess: this.proccessGallery.bind(this),
            onFailure: function () { }
        }).send();
    },

    proccessGallery: function (json) {
        this.clear();
        var photos = json.feed.entry;
        photos.each(function (item) {
            var title = item.title.$t;
            var url = item.content.src;
            var src = item.media$group.media$thumbnail[1].url;

            var wrapper = new Element('div', {
                'class': this.options.css.image});
            new Element('h3', {'text': title}).inject(wrapper);
            var img = new Element('img', {'alt': url, 'src': src});
            img.inject(wrapper);
            wrapper.addEvent('click', function (e) {
                this._input.set('value', url);
                this.close();
            }.bind(this));
            wrapper.inject(this._window);
        }.bind(this));
    }
});

