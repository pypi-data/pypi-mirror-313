odoo.define('helpdesk_automatic_stage_changes.RelativeDateFormatter', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.date_fields = '[]';
            if (typeof this.state.getContext().date_fields_from_now != 'undefined'){
                this.date_fields = this.state.getContext().date_fields_from_now;
            }

        },
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            if (node.attrs.name.includes(this.date_fields)){
                var $div = $('<div>');
                var date_value = $($td).html();   
                var display_str = moment(date_value).fromNow();

                $div.append(display_str);
                $td.html($div);
            }
            return $td;
        },
    });

    var FieldDate = require('web.basic_fields').FieldDate;
    var field_registry = require('web.field_registry');

    var RelativeDateWidget = FieldDate.extend({
        _render: function () {
            var date_value = this.value;
            var display_str = moment(date_value).fromNow();

            this.$el.text(display_str);
        },
    });

    field_registry.add('relative_date', RelativeDateWidget);

    return RelativeDateWidget, ListRenderer;
});