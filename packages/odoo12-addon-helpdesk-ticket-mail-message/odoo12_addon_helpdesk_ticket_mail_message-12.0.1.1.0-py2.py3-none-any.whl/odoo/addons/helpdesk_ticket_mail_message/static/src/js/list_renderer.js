odoo.define('helpdesk_ticket_mail_message.ListRenderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var view_registry = require('web.view_registry');
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var fieldRegistry = require('web.field_registry');

    var ListRendererMailIcon = ListRenderer.extend({
        // We hide the value of a column in a list of a specific field.
        _renderHeaderCell: function (node) {
            var $th = this._super.apply(this, arguments);
            var name = node.attrs.name;
            if (name == "message_type_mail"){
                $th.html("");
            }
            return $th;
        },
        //We redesign how a particular field in the list will be displayed
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            var name = node.attrs.name;
            if (name == "message_type_mail"){
                var value = record.data[name];
                var $i = $('<i>');

                if (value == "email_sent"){
                    $i.addClass('fa fa-long-arrow-left color-red');
                    $i.attr('title','To: ' + record.data['origin_email_to']);
                } else if (value == "email_received"){
                    $i.addClass('fa fa-long-arrow-right color-black');
                    $i.attr('title','From: ' + record.data['email_from']);
                } else if (value == "note"){
                    $i.addClass('fa fa-file-text-o color-green');
                    $i.attr('title','User: ' + record.data['email_from']);
                }

                $td.html($i);

                $td.attr("style", "text-align: center;");
            } else if (name == "date_subject"){
                $td.attr('title',
                    moment.utc(record.data['date']).format("YYYY-MM-DD HH:MM:SS"));
            } else if ($td.find(".fa-reply").length == 1){
                $i = $td.find(".fa-reply");
                $i.attr('title',$i.parent().attr("help"));
            } else if ($td.find(".fa-share").length == 1){
                $i = $td.find(".fa-share");
                $i.attr('title',$i.parent().attr("help"));
            } else if ($td.find(".fa-reply-all").length == 1){
                $i = $td.find(".fa-reply-all");
                $i.attr('title',$i.parent().attr("help"));
            }


            return $td;
        },
    });

    view_registry.add('mail_icon', ListRendererMailIcon);

    var ListRendererMailIconFieldOne2Many = FieldOne2Many.extend({
        _getRenderer: function () {
            if (this.view.arch.tag === 'tree') {
                return ListRendererMailIcon;
            }
            return this._super.apply(this, arguments);
        },
    });

    fieldRegistry.add('list_mail_icon_one2many', ListRendererMailIconFieldOne2Many);

    return ListRendererMailIcon, ListRendererMailIconFieldOne2Many;
});
