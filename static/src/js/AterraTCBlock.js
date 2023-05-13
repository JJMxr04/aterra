odoo.define('aterra.aterra_card_template', function(require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');

    var CustomBlock = Widget.extend({
        template: 'aterra_card_template',
    });

    core.action_registry.add('aterra_card_template', CustomBlock);

    return CustomBlock;
});
