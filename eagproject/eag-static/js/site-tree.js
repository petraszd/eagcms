(function (postUrl) {
    function getLevel(item) {
        return item.get('class').toInt();
    }

    function setLevel(item, level) {
        item.set('class', level);
        item.setStyle('margin-left', (level - 1) * 3 + 'em');
    }

    function hideChilds(item) {
        var childs = item.getAllNext();
        var level = getLevel(item);
        for (var i = 0; i < childs.length; ++i) {
            if (level >= getLevel(childs[i]))
                break;
            childs[i].inject($('Holder'));
        }
    }

    function showChilds(item) {
        var curLevel = getLevel(item);
        var lis = $('Holder').getElements('li');
        if (!lis.length) {
            return;
        }
        var delta = curLevel - (getLevel(lis[0]) - 1);
        var last = item;
        lis.each(function(li) {
            setLevel(li, getLevel(li) + delta);
            li.inject(last, 'after');
            last = li;
        });
    }

    function checkOrder (elem, clone, pages) {
        var next = elem.getNext('li');
        if (next && getLevel(next) == 0)
            next = next.getNext('li');
        var prev = elem.getPrevious('li');
        if (prev && getLevel(prev) == 0)
            prev = prev.getPrevious('li');

        if (!prev) {
            setLevel(elem, 1);
            return;
        }

        if (!next) {
            var from = 1;
            var fx = pages[0].getPosition().x;
        } else {
            var from = getLevel(next);
            var fx = next.getPosition().x;
        }
        var tx = prev.getPosition().x;

        var to = getLevel(prev);
        var cx = clone.getPosition().x;

        if (from > to) {
            setLevel(elem, from);
            return;
        } else if (from == to) {
            if (cx > fx)
                setLevel(elem, from + 1);
            else
                setLevel(elem, from);
            return;
        }

        var stepLength = (tx - fx) / parseFloat(to - from);
        var relativePos = cx - fx;
        var newLevel = Math.max(from, Math.min(to + 1, parseInt(relativePos / stepLength)));
        setLevel(elem, parseInt(newLevel));
    }

    function startReordering () {
        var tree = $('Tree');
        var pages = tree.getChildren();
        pages.each(function(li) {
            setLevel(li, getLevel(li));
        });
        var sortable = new Sortables(tree, {
            clone: true,
            opacity: 0.5,
            onStart: function (elem, clone) {
                hideChilds(elem);
                setLevel(clone, 0);
                clone.addEvent('mousemove', function () {
                    checkOrder(elem, clone, pages);
                });
            },
            onSort: function (elem, clone) {
                checkOrder(elem, clone, pages);
            },
            onComplete: function (elem) {
                $('OrderButtons').setStyle('display', 'block');
                showChilds(elem);
            }
        });

        return sortable;
    };

    window.addEvent('domready', function () {
        $$('.reorder-button').addEvent('click', function (e) {
            $('Tree').addClass('ordering');
            $('Tree').highlight('#ababf8');
            var sortable = startReordering();
            e.preventDefault();
            $('SaveOrder').addEvent('click', function () {
                sortable.detach();
                $('Tree').getChildren().each(function (li) {
                    li.set('id', li.get('id') + ' ' + li.get('class'));
                });
                $('ReorderData').set('value', sortable.serialize().join('&'));
                $('ReorderForm').submit();
            });
        });

        $$('#Tree .delete').addEvent('click', function (e) {
            return confirm('Are You sure?');
        });
    });
}) ();

